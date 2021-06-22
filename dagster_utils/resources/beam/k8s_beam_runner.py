from dataclasses import dataclass, field
from typing import List, Any, Optional
from uuid import uuid4

import kubernetes
from dagster import DagsterLogManager, Field, IntSource, resource, StringSource
from dagster.core.execution.context.init import InitResourceContext
from dagster_k8s.client import DagsterKubernetesClient
from kubernetes.client.models.v1_job import V1Job

from dagster_utils.resources.beam.beam_runner import BeamRunner


# separating out config for the cloud dataflow pipeline to make
# the giant mess of parameters here a little easier to parse
@dataclass
class K8sDataflowCloudConfig:
    project: str
    service_account: str
    subnet_name: str
    region: str
    worker_machine_type: str
    starting_workers: int
    max_workers: int

    # fields computed from provided params
    subnetwork: str = field(init=False)

    def __post_init__(self) -> None:
        self.subnetwork = '/'.join([
            'regions',
            self.region,
            'subnetworks',
            self.subnet_name,
        ])


@dataclass
class K8sDataflowBeamRunner(BeamRunner):
    cloud_config: K8sDataflowCloudConfig
    kubernetes_service_account: str
    temp_bucket: str
    image_name: str
    image_version: str
    namespace: str
    logger: DagsterLogManager

    def run(
        self,
        run_arg_dict: dict[str, Any],
        target_class: str,
        scala_project: str,
        job_name: Optional[str] = None
    ) -> None:
        args_dict = {
            'runner': 'dataflow',
            'project': self.cloud_config.project,
            'region': self.cloud_config.region,
            'tempLocation': f'gs://{self.temp_bucket}/dataflow',
            'subnetwork': self.cloud_config.subnetwork,
            'serviceAccount': self.cloud_config.service_account,
            'workerMachineType': self.cloud_config.worker_machine_type,
            'autoscalingAlgorithm': 'THROUGHPUT_BASED',
            'numWorkers': str(self.cloud_config.starting_workers),
            'maxNumWorkers': str(self.cloud_config.max_workers),
            'experiments': 'shuffle_mode=service',
        }
        args_dict = {**args_dict, **run_arg_dict}

        # process the args dict into dataflow flags
        args = [
            f'--{field_name}={value}'
            for field_name, value
            in args_dict.items()
        ]

        image_name = f"{self.image_name}:{self.image_version}"  # {context.solid_config['version']}"
        job = self.dispatch_k8s_job(image_name, job_name, args)
        self.logger.info("Dataflow job started")

        client = DagsterKubernetesClient.production_client()
        client.wait_for_job_success(job.metadata.name, self.namespace)

    def dispatch_k8s_job(
            self,
            image_name: str,
            job_name_prefix: Optional[str],
            args: List[str],
            load_incluster_config: bool = True
    ) -> V1Job:
        # we will need to poll the pod/job status on creation
        if load_incluster_config:
            kubernetes.config.load_incluster_config()
        else:
            kubernetes.config.load_kube_config()

        if job_name_prefix:
            job_name = f"{job_name_prefix}-{uuid4()}"
        else:
            job_name = f"{uuid4()}"

        pod_name = f"{job_name}-pod"
        job_container = kubernetes.client.V1Container(
            name=job_name,
            image=image_name,
            args=args,
        )

        template = kubernetes.client.V1PodTemplateSpec(
            metadata=kubernetes.client.V1ObjectMeta(name=pod_name),
            spec=kubernetes.client.V1PodSpec(
                restart_policy="Never",
                containers=[job_container],
                service_account_name=self.kubernetes_service_account,
            ),
        )

        job = kubernetes.client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=kubernetes.client.V1ObjectMeta(
                name=job_name,
            ),
            spec=kubernetes.client.V1JobSpec(
                template=template,
                backoff_limit=2,
                ttl_seconds_after_finished=86400,  # one day
            ),
        )
        batch_v1 = kubernetes.client.BatchV1Api()
        api_response = batch_v1.create_namespaced_job(
            body=job,
            namespace=self.namespace,
        )
        self.logger.info(f"Job created. status='{str(api_response.status)}'")

        return api_response


@resource({
    "project": Field(StringSource),
    "subnet_name": Field(StringSource),
    "region": Field(StringSource),
    "worker_machine_type": Field(StringSource),
    "starting_workers": Field(IntSource),
    "max_workers": Field(IntSource),
    "service_account": Field(StringSource),
    "kubernetes_service_account": Field(StringSource),
    "temp_bucket": Field(StringSource),
    "image_name": Field(StringSource),
    "image_version": Field(StringSource),
    "namespace": Field(StringSource),
})
def k8s_dataflow_beam_runner(init_context: InitResourceContext) -> K8sDataflowBeamRunner:
    cloud_config = K8sDataflowCloudConfig(
        project=init_context.resource_config['project'],
        service_account=init_context.resource_config['service_account'],
        subnet_name=init_context.resource_config['subnet_name'],
        region=init_context.resource_config['region'],
        worker_machine_type=init_context.resource_config['worker_machine_type'],
        starting_workers=init_context.resource_config['starting_workers'],
        max_workers=init_context.resource_config['max_workers'],
    )
    return K8sDataflowBeamRunner(
        cloud_config=cloud_config,
        kubernetes_service_account=init_context.resource_config['kubernetes_service_account'],
        temp_bucket=init_context.resource_config['temp_bucket'],
        image_name=init_context.resource_config['image_name'],
        image_version=init_context.resource_config['image_version'],
        namespace=init_context.resource_config['namespace'],
        logger=init_context.log_manager,
    )
