import os
import subprocess

VAULT = os.environ["FGV_VAULT_ROOT"]
MATERIALS = "10 Matérias/{materia}/Aulas/{data}/Material/"
SYNC = ["fgv-sync", "publish"]
CATALOG_QUERY = ["python3", ".fgv/scripts/hermes_catalog_query.py"]


def bounded_catalog_query_probe():
    return subprocess.run(
        [
            "python3",
            ".fgv/scripts/hermes_catalog_query.py",
            "--vault",
            "/root/vault",
            "--query-type",
            "eclass_material",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
