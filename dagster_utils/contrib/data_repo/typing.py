"""
Types and annotations useful for interaction with TDR
"""


# Aliases to add some type safety when calling the jade API client and make juggling the (many) string
# parameters easier

class JobId(str):
    pass


class ProfileId(str):
    pass


class DatasetName(str):
    pass


class DatasetId(str):
    pass
