import base64
import hashlib
import json
import os
import subprocess
import sys

VAULT = os.environ["FGV_VAULT_ROOT"]
SYNC = ["fgv-sync", "status"]
CATALOG_QUERY = ["python3", ".fgv/scripts/hermes_catalog_query.py"]


def main():
    if sys.argv[1:] != ["--hermes-channel-smoke"]:
        raise SystemExit("unsupported invocation")
    result = subprocess.run(
        [
            "python3",
            ".fgv/scripts/hermes_catalog_query.py",
            "--vault",
            VAULT,
            "--query-type",
            os.environ["FGV_HERMES_QUERY_TYPE"],
            "--subject-id",
            os.environ["FGV_HERMES_SUBJECT_ID"],
            "--expected-catalog-sha256",
            os.environ["FGV_HERMES_EXPECTED_CATALOG_SHA256"],
        ],
        check=True,
        capture_output=True,
    )
    consumed_sha256 = hashlib.sha256(result.stdout).hexdigest()
    print(json.dumps({
        "challenge": os.environ["FGV_HERMES_CHANNEL_CHALLENGE"],
        "consumed_stdout_sha256": consumed_sha256,
        "query_stdout_b64": base64.b64encode(result.stdout).decode("ascii"),
        "schema_version": 1,
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
