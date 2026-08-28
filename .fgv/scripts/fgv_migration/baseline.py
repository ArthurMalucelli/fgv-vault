"""Validate the closed, deterministic migration integrity baseline schema."""

import re
import unicodedata

from .inventory import InventoryError, normalize_relative_path


MAX_COUNT = 2**64 - 1
OID_PATTERN = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
CATEGORIES = frozenset({"archive", "home", "knowledge", "subject", "system"})
MANIFEST_SERIALIZATION = "json-utf8-nfc-indent-2-lf-v1"
BINARY_METHOD = "casefolded-filename-ending-extension-allowlist-v1"
AGGREGATE_METHOD = (
    "sha256-source-utf8-nul-content-sha256-bytes-size-u64be-v1"
)
WIKILINK_METHOD = "manifest-source-git-wikilink-audit-v2"


class BaselineError(ValueError):
    """The migration baseline does not satisfy its closed schema."""


def _closed_object(
    value: object, keys: frozenset[str], field: str
) -> dict[str, object]:
    if type(value) is not dict:
        raise BaselineError(f"baseline {field} must be an object")
    if set(value) != keys:
        raise BaselineError(f"baseline {field} has invalid keys")
    return value


def _count(value: object, field: str) -> int:
    if type(value) is not int or value < 0 or value > MAX_COUNT:
        raise BaselineError(f"baseline {field} has invalid count")
    return value


def _exact_string(value: object, expected: str, field: str) -> None:
    if type(value) is not str or value != expected:
        raise BaselineError(f"baseline {field} has invalid value")


def _hash(value: object, pattern: re.Pattern[str], field: str) -> None:
    if type(value) is not str or pattern.fullmatch(value) is None:
        raise BaselineError(f"baseline {field} has invalid hash")


def _relative_path(value: object, field: str) -> None:
    if type(value) is not str:
        raise BaselineError(f"baseline {field} must be a string")
    try:
        normalized = normalize_relative_path(value)
    except InventoryError as error:
        raise BaselineError(f"baseline {field} has unsafe path") from error
    if normalized != value:
        raise BaselineError(f"baseline {field} must be NFC canonical")


def _validate_extensions(value: object) -> None:
    if type(value) is not list:
        raise BaselineError("baseline binary extensions must be an array")
    for extension in value:
        if (
            type(extension) is not str
            or len(extension) < 2
            or not extension.startswith(".")
            or extension != extension.casefold()
            or any(
                unicodedata.category(character) in {"Cc", "Cf"}
                or character in "/\\"
                for character in extension
            )
        ):
            raise BaselineError("baseline binary extension is invalid")
    if value != sorted(value) or len(value) != len(set(value)):
        raise BaselineError(
            "baseline binary extensions must be sorted and unique"
        )


def validate_baseline(value: object) -> None:
    """Reject any baseline value outside the versioned integrity schema."""
    baseline = _closed_object(
        value,
        frozenset({"schema_version", "base", "manifest", "inventory", "wikilinks"}),
        "root",
    )
    if type(baseline["schema_version"]) is not int or baseline["schema_version"] != 1:
        raise BaselineError("baseline schema_version must be integer 1")

    base = _closed_object(
        baseline["base"], frozenset({"commit", "tree"}), "base"
    )
    _hash(base["commit"], OID_PATTERN, "base.commit")
    _hash(base["tree"], OID_PATTERN, "base.tree")

    manifest = _closed_object(
        baseline["manifest"],
        frozenset({"path", "sha256", "serialization"}),
        "manifest",
    )
    _relative_path(manifest["path"], "manifest.path")
    _hash(manifest["sha256"], SHA256_PATTERN, "manifest.sha256")
    _exact_string(
        manifest["serialization"],
        MANIFEST_SERIALIZATION,
        "manifest.serialization",
    )

    inventory = _closed_object(
        baseline["inventory"],
        frozenset(
            {
                "records",
                "unique_sources",
                "unique_destinations",
                "category_counts",
                "binary",
                "aggregate",
            }
        ),
        "inventory",
    )
    records = _count(inventory["records"], "inventory.records")
    unique_sources = _count(
        inventory["unique_sources"], "inventory.unique_sources"
    )
    unique_destinations = _count(
        inventory["unique_destinations"], "inventory.unique_destinations"
    )
    if unique_sources != records or unique_destinations != records:
        raise BaselineError("baseline inventory uniqueness counts must equal records")

    category_counts = _closed_object(
        inventory["category_counts"], CATEGORIES, "inventory.category_counts"
    )
    counted_categories = sum(
        _count(category_counts[category], f"inventory.category_counts.{category}")
        for category in CATEGORIES
    )
    if counted_categories != records:
        raise BaselineError("baseline category counts must sum to records")

    binary = _closed_object(
        inventory["binary"],
        frozenset({"method", "extensions", "count"}),
        "inventory.binary",
    )
    _exact_string(binary["method"], BINARY_METHOD, "inventory.binary.method")
    _validate_extensions(binary["extensions"])
    binary_count = _count(binary["count"], "inventory.binary.count")
    if binary_count > records:
        raise BaselineError("baseline binary count cannot exceed records")

    aggregate = _closed_object(
        inventory["aggregate"],
        frozenset({"method", "sha256"}),
        "inventory.aggregate",
    )
    _exact_string(
        aggregate["method"], AGGREGATE_METHOD, "inventory.aggregate.method"
    )
    _hash(aggregate["sha256"], SHA256_PATTERN, "inventory.aggregate.sha256")

    wikilinks = _closed_object(
        baseline["wikilinks"],
        frozenset({"method", "total", "resolved", "unresolved", "ambiguous"}),
        "wikilinks",
    )
    _exact_string(wikilinks["method"], WIKILINK_METHOD, "wikilinks.method")
    total = _count(wikilinks["total"], "wikilinks.total")
    resolved = _count(wikilinks["resolved"], "wikilinks.resolved")
    unresolved = _count(wikilinks["unresolved"], "wikilinks.unresolved")
    ambiguous = _count(wikilinks["ambiguous"], "wikilinks.ambiguous")
    if total != resolved + unresolved + ambiguous:
        raise BaselineError("baseline wikilink counts must sum to total")
