import copy
import importlib
import json
from pathlib import Path
import unittest


try:
    migration_baseline = importlib.import_module("fgv_migration.baseline")
except ModuleNotFoundError:
    migration_baseline = None


ROOT = Path(__file__).resolve().parents[2]
REAL_BASELINE = ROOT / "30 Sistema/Estado/migration-baseline.json"


class BaselineSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline = json.loads(REAL_BASELINE.read_bytes())

    def require_validator(self):
        self.assertIsNotNone(
            migration_baseline,
            "migration baseline validator is missing",
        )
        return migration_baseline.validate_baseline

    def mutated(self, *path: str, value) -> dict[str, object]:
        baseline = copy.deepcopy(self.baseline)
        target = baseline
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        return baseline

    def with_extra(self, *path: str) -> dict[str, object]:
        baseline = copy.deepcopy(self.baseline)
        target = baseline
        for key in path:
            target = target[key]
        target["unexpected"] = True
        return baseline

    def test_real_baseline_has_the_closed_valid_schema(self) -> None:
        validator = self.require_validator()

        validator(self.baseline)

    def test_invalid_types_keys_hashes_methods_counts_and_ranges_are_rejected(self) -> None:
        validator = self.require_validator()
        invalid_baselines = {
            "top-level type": [],
            "top-level extra": self.with_extra(),
            "schema bool": self.mutated("schema_version", value=True),
            "schema range": self.mutated("schema_version", value=2),
            "base type": self.mutated("base", value=[]),
            "base extra": self.with_extra("base"),
            "commit oid": self.mutated("base", "commit", value="A" * 40),
            "tree oid": self.mutated("base", "tree", value="bad"),
            "manifest extra": self.with_extra("manifest"),
            "manifest path type": self.mutated("manifest", "path", value=1),
            "manifest path absolute": self.mutated(
                "manifest", "path", value="/absolute/manifest.json"
            ),
            "manifest sha": self.mutated("manifest", "sha256", value="A" * 64),
            "serialization": self.mutated(
                "manifest", "serialization", value="other"
            ),
            "inventory extra": self.with_extra("inventory"),
            "records bool": self.mutated("inventory", "records", value=True),
            "records negative": self.mutated("inventory", "records", value=-1),
            "unique sources mismatch": self.mutated(
                "inventory", "unique_sources", value=1058
            ),
            "unique destinations mismatch": self.mutated(
                "inventory", "unique_destinations", value=1058
            ),
            "categories extra": self.with_extra("inventory", "category_counts"),
            "category bool": self.mutated(
                "inventory", "category_counts", "home", value=True
            ),
            "category sum": self.mutated(
                "inventory", "category_counts", "home", value=8
            ),
            "binary extra": self.with_extra("inventory", "binary"),
            "binary method": self.mutated(
                "inventory", "binary", "method", value="other"
            ),
            "extensions type": self.mutated(
                "inventory", "binary", "extensions", value=(".pdf",)
            ),
            "extensions unsorted": self.mutated(
                "inventory", "binary", "extensions", value=[".pdf", ".docx"]
            ),
            "extensions duplicate": self.mutated(
                "inventory", "binary", "extensions", value=[".pdf", ".pdf"]
            ),
            "extensions uppercase": self.mutated(
                "inventory", "binary", "extensions", value=[".PDF"]
            ),
            "binary count bool": self.mutated(
                "inventory", "binary", "count", value=True
            ),
            "binary count range": self.mutated(
                "inventory", "binary", "count", value=1060
            ),
            "aggregate extra": self.with_extra("inventory", "aggregate"),
            "aggregate method": self.mutated(
                "inventory", "aggregate", "method", value="other"
            ),
            "aggregate sha": self.mutated(
                "inventory", "aggregate", "sha256", value="not-a-sha"
            ),
            "wikilinks extra": self.with_extra("wikilinks"),
            "wikilinks method": self.mutated(
                "wikilinks", "method", value="other"
            ),
            "wikilink total bool": self.mutated(
                "wikilinks", "total", value=True
            ),
            "wikilink range": self.mutated(
                "wikilinks", "unresolved", value=-1
            ),
            "wikilink sum": self.mutated("wikilinks", "resolved", value=4990),
        }

        for label, baseline in invalid_baselines.items():
            with self.subTest(case=label):
                with self.assertRaises(ValueError, msg=label):
                    validator(baseline)


if __name__ == "__main__":
    unittest.main()
