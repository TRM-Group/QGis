import requests

# 🔧 Crear sesión persistente
session = requests.Session()

# -----------------------------
# 1️⃣ LOGIN
# -----------------------------
login_url = "https://portaleingmonza.visura.it/authenticateNuovoVisura.do"
login_data = {
    "userName": "",
    "password": ""
}

resp_login = session.post(login_url, data=login_data)
print("🔐 Login status:", resp_login.status_code)

with open("step1_login.html", "w", encoding="utf-8") as f:
    f.write(resp_login.text)

# -----------------------------
# 2️⃣ CLICK accessoRapido('agenziadelterritorioIF', 0)
# -----------------------------
accesso_url = "https://portaleingmonza.visura.it/homepageAccessoRapidoActionNuovoVisura.do"
accesso_data = {
    "numBancaDati": "",
    "disabilitaAccessoRapido": "0",
    "codiceGrpServBke": "agenziadelterritorioIF",
    "idAreaTematica": ""
}

resp_accesso = session.post(accesso_url, data=accesso_data)
print("➡️ AccessoRapido status:", resp_accesso.status_code)

with open("step2_accessoRapido.html", "w", encoding="utf-8") as f:
    f.write(resp_accesso.text)

# -----------------------------
# 3️⃣ CLICK en el anchor 'Accedi'
# -----------------------------
submit_url = "https://portaleingmonza.visura.it/homepageBancheDatiAction1NuovoVisura.do"
submit_data = {
    "azione": "entra",
    "numBancaDati": "1",
    "codiceGrpSrv": "agenziadelterritorioIF",
    "numLink": ""
}

resp_submit = session.post(submit_url, data=submit_data)
print("➡️ Submit Accedi status:", resp_submit.status_code)

with open("step3_submit.html", "w", encoding="utf-8") as f:
    f.write(resp_submit.text)

# -----------------------------
# 4️⃣ (Opcional) Detectar referencia a portalebanchedatij
# -----------------------------
if "portalebanchedatij.visura.it" in resp_submit.text:
    print("✅ Redirección a portalebanchedatij detectada.")
else:
    print("⚠️ No se detecta redirección. Revisa step3_submit.html")
