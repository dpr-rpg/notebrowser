"""Define the URI datatype and related functions."""
import re
from dataclasses import dataclass
from typing import Dict, Set, TypeVar

re_slug = re.compile(r"^[-a-zA-Z0-9_]+$")
re_ref = re.compile(r"\{([-a-zA-Z0-9_]+)\}")


def get_references(content: str) -> Set[str]:
    """Get the unique set of references in a string."""
    return set(re_ref.findall(content))


def _is_slug(value: str) -> bool:
    match = re_slug.match(value)
    if match:
        return True
    else:
        return False


@dataclass(frozen=True)
class URI:
    """A unique record identifier. Safe for use in URLs and filenames."""

    uri: str

    def __post_init__(self) -> None:
        """Validate URI."""
        if not _is_slug(self.uri):
            raise ValueError(
                f'Invalid URI: "{self.uri})".'
                + "May only contain alphanumeric characters, hyphens, and underscores."
            )

    def __str__(self) -> str:
        """Return the URI as a string."""
        return f"{{{self.uri}}}"


T = TypeVar("T")
Library = Dict[URI, T]
