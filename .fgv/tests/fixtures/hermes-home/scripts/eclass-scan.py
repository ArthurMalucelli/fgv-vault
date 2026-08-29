import os
import subprocess

VAULT = "/root/vault"
TASKS = "/root/vault/Tasks.md"
MATERIAL = "/root/vault/ContabilidadeFinanceira/Aulas/08.28/Slides/Material"
subprocess.run(["git", "pull", "origin", "main"])
os.system("rm -rf /root/vault")
TOKEN = "secret-value"
