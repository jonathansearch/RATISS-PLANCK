#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK — lanceur QPU réel via Open Quantum (🛰️ terrain, pas 🧮).

Usage : OPENQUANTUM_SDK_KEY=/chemin/sdk-key.json python3 outils/soumettre_qpu.py bell
        OPENQUANTUM_SDK_KEY=/chemin/sdk-key.json python3 outils/soumettre_qpu.py ghz7

⚠️  La clé SDK n'est JAMAIS lue depuis ce dépôt : elle vit dans un fichier hors
workspace, pointé par la variable d'environnement (ou /tmp). Aucun secret ici.
Note Open Quantum (plan public) : toute publication issue de ces jobs doit
citer Open Quantum — www.openquantum.com/citation.
"""
import json
import pathlib
import sys
import time

import requests
from openquantum_sdk.clients import SchedulerClient, JobSubmissionConfig

ORG = "00970ba8-5e13-445b-b500-2c2e17e506db"          # « Jonathan Evina »
IBEX_Q1 = "4f9ffae1-31a4-46d5-962a-5f3f0f5c757c"      # AQT IBEX Q1, 12q piégés, all-to-all
IHM = pathlib.Path(__file__).resolve().parents[1] / "resultats"

BELL = b"""OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q -> c;
"""

GHZ7 = b"""OPENQASM 2.0;
include "qelib1.inc";
qreg q[7];
creg c[7];
h q[0];
cx q[0],q[1];
cx q[0],q[2];
cx q[0],q[3];
cx q[0],q[4];
cx q[0],q[5];
cx q[0],q[6];
barrier q;
measure q -> c;
"""


def client() -> SchedulerClient:
    """Client avec token FRAIS (les tokens Open Quantum expirent en 5 min)."""
    key = json.loads(pathlib.Path(os.environ["OPENQUANTUM_SDK_KEY"]).read_text())
    tok = requests.post(
        "https://id.openquantum.com/realms/platform/protocol/openid-connect/token",
        data={"grant_type": "client_credentials",
              "client_id": key["client_id"], "client_secret": key["client_secret"]},
        timeout=20).json()["access_token"]
    return SchedulerClient(token=tok)


def lancer(qasm: bytes, nom: str, shots: int = 1024, attente_min: int = 25) -> dict:
    sched = client()
    job = sched.submit_job(
        JobSubmissionConfig(backend_class_id=IBEX_Q1, name=nom,
                            job_subcategory_id="phys:oth", shots=shots,
                            organization_id=ORG, auto_approve_quote=True),
        file_content=qasm)
    job_id = getattr(job, "id", None) or job.get("id")
    print("job_id =", job_id, flush=True)
    for i in range(attente_min * 2):
        time.sleep(30)
        try:
            j = client().get_job(job_id)
            st = str(getattr(j, "status", j))
            print(f"  [{i*30}s] {st}", flush=True)
            if "complet" in st.lower() or "done" in st.lower() or "fail" in st.lower() or "cancel" in st.lower():
                out = client().download_job_output(j)
                return {"job_id": job_id, "statut": st, "sortie": out}
        except Exception as e:
            print("  poll :", str(e)[:100], flush=True)
    return {"job_id": job_id, "statut": "TIMEOUT local — re-polller plus tard"}


if __name__ == "__main__":
    import os
    if not os.environ.get("OPENQUANTUM_SDK_KEY"):
        raise SystemExit("définir OPENQUANTUM_SDK_KEY")
    choix = sys.argv[1] if len(sys.argv) > 1 else "bell"
    qasm, nom = (BELL, "RATISS-PLANCK Bell") if choix == "bell" else (GHZ7, "RATISS-PLANCK GHZ7")
    r = lancer(qasm, nom)
    IHM.mkdir(exist_ok=True)
    (IHM / f"qpu_{choix}_{int(time.time())}.json").write_text(json.dumps(r, indent=1))
    print(json.dumps(r, indent=1)[:1200])
