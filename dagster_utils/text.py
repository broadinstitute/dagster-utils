"""
Utilities to process text and strings.
"""

import re


def camel_to_snake(camel: str) -> str:
    return re.sub(r'((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', camel).lower()
