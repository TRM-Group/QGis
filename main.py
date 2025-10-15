import requests
from bs4 import BeautifulSoup

# importing Login data from config file
from config import login_data

# 🔧 Crear sesión persistente
session = requests.Session()

# -----------------------------
# 1️⃣ LOGIN PAGE
# -----------------------------
login_url = "https://portaleingmonza.visura.it/authenticateNuovoVisura.do"

resp_login = session.post(login_url, data=login_data)
print("🔐 Login status:", resp_login.status_code)

with open("step1_login.html", "w", encoding="utf-8") as f:
    f.write(resp_login.text)

# -----------------------------
# 2️⃣ CLICK on accessoRapido('agenziadelterritorioIF', 0)
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

# -----------------------------
# 5️⃣ Preparar request hacia SceltaLink.do (portalebanchedatij)
# -----------------------------
"""
url next = https://portalebanchedatij.visura.it/framesetAgenziaTerritorioIF.htm
"""
soup = BeautifulSoup(resp_submit.text, "html.parser")
form = soup.find("form", attrs={"action":"/homepageBancheDatiAction1NuovoVisura.do"})

if not form:
    print("⚠️ Form hacia portalebanchedatij no encontrado.")
else:
    next_url = "https://portalebanchedatij.visura.it/" + form["action"]
    form_data = {}
    for inp in form.find_all("input"):
        name = inp.get("name")
        value = inp.get("value", "")
        if name:
            form_data[name] = value
    
    print("✅ Form data got it from portalebanchedatij.")


next_url = form_data["loginbd"]
print(f"URL page for loggato {next_url}")
loggato = session.post(next_url, data=form_data)
print("➡️ Redirect Form:", loggato.status_code)

with open("step4_redirect.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)

next_url = "https://portalebanchedatij.visura.it/Servizi/"
print(f"URL page for loggato {next_url}")
loggato = session.get(next_url)
print("➡️ servizi Form:", loggato.status_code)

with open("step5_framset.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)


next_url = "https://portalebanchedatij.visura.it/Visure/Informativa.do?tipo=/T/TM/VCVC_"
print(f"URL page for conferma {next_url}")
loggato = session.post(next_url, data="")
print("➡️ Conferma Servizi Form:", loggato.status_code)

with open("step6_conferma.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)


next_url = "https://portalebanchedatij.visura.it/Visure/SceltaServizio.do?tipo=/T/TM/VCVC_"
print(f"URL page for conferma {next_url}")
loggato = session.get(next_url)
print("➡️ Conferma Servizi Form:", loggato.status_code)

with open("step7_conferma.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)

# Space for searching form and getting data


# Close Session ❌
close_session_url = "https://portalebanchedatij.visura.it/ECMBKE/Session/Terminate"
print(f"URL Page for closing session {close_session_url}")
close_session_form = {
    "funzione": "chiudi"
}
loggato = session.post(close_session_url, data=close_session_form)
print("➡️ Session close status:", loggato.status_code)

with open("step8_close.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)


session.close()# Cerrar la sesión de requests

"""
"https://portaleingmonza.visura.it/homepageAreeTematicheAction.do"
    resp_next = session.post(next_url, data=form_data)
    print("➡️ Step 5 SceltaLink.do status:", resp_next.status_code)

    with open("step5_scelta.html", "w", encoding="utf-8") as f:
        f.write(resp_next.text)

    print("✅ Se ha enviado el request hacia portalebanchedatij")
"""