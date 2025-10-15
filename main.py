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

next_url = "https://portalebanchedatij.visura.it/Visure/DataRichiesta.do"
print(f"URL page for selecting 'Provincia' {next_url}")
data_form = {
    "listacom": "BERGAMO Territorio-BG"
}
loggato = session.post(next_url, data=data_form)
print("➡️ Conferma Data Richiesta Form:", loggato.status_code)

with open("step8_provincia.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)

# <li><a href="/Visure/SceltaLink.do?lista=IMM&amp;codUfficio=BG">Immobile</a></li>	

next_url = "https://portalebanchedatij.visura.it/Visure/SceltaLink.do?lista=IMM&codUfficio=BG"
print(f"URL page for selecting 'IMMOBILE' {next_url}")
data_form = {
    "listacom": "BERGAMO Territorio-BG"
}
loggato = session.get(next_url)
print("➡️ Conferma Data Richiesta Form:", loggato.status_code)

with open("step9_IMMOBILE.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)


# STEP 9B

next_url = "https://portalebanchedatij.visura.it/Visure/vimm/RicercaIMM.do"
print(f"URL page for selecting 'IMMOBILE' {next_url}")
data_form = {
    "tipoCatasto": "T",
    "denomComune" : "C894#COLOGNO AL SERIO#0#0",
    "selSezione" : "",
    "sezione": "",
    "tipoIdentificativo": "d",
    "sezUrb": "",
    "foglio": "09",
    "particella1": "5731",
    "particella2": "",
    "subalterno1" : "",
    "tipoDenuncia" : "",
    "numero1": "",
    "anno" : "",
    "richiedente": "",
    "motivoText" : "",
    "scelta": "Ricerca"
}
loggato = session.post(next_url, data=data_form)
print("➡️ Conferma Data Richiesta Form:", loggato.status_code)

with open("step9B_IMMOBILE.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)



# value="C894#COLOGNO AL SERIO#0#0"
"""
action="/Visure/vimm/AssenzaSubalterno.do"
"""

next_url = "https://portalebanchedatij.visura.it/Visure/vimm/AssenzaSubalterno.do"
print(f"URL page for selecting 'IMMOBILE' {next_url}")
data_form = {
    "confAssSub": "Conferma",
    "denomComune" : "C894#COLOGNO AL SERIO#0#0",
    "nomeComune": "COLOGNO AL SERIO",
    "codiceComune": "C894",
    "tipoCatasto": "T",
    "sezione" : "",
    "tipoIdentificativo": "d",
    "sezUrb": "",
    "foglio": "09",
    "particella1": "5731",
    "particella2": "",
    "subalterno1" : "",
    "subalterno2" : "",
    "tipoDenuncia" : "",
    "numero1": "",
    "anno" : "",
    "scelta": "Ricerca"
}
loggato = session.post(next_url, data=data_form)
print("➡️ Conferma Data Richiesta Form:", loggato.status_code)

with open("step10_RICHIESTA.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)


# SceltaVisuraImmSoggForm
# /Visure/vimm/SceltaVisuraImmSoggIMM.do

soup = BeautifulSoup(loggato.text, "html.parser")
form = soup.find("form", attrs={"action":"/Visure/vimm/SceltaVisuraImmSoggIMM.do"})

if not form:
    print("⚠️ Form from VISURE CATASTALI not found")
else:
    next_url = "https://portalebanchedatij.visura.it/" + form["action"]
    form_data = {}
    for inp in form.find_all("input"):
        name = inp.get("name")
        value = inp.get("value", "")
        if name:
            form_data[name] = value
    
    print(f"✅ Form data got it from portalebanchedatij.\n {form_data}")
    visImmSel_value = soup.find("input", {"property": "visImmSel"}).get("value")
    print(f"visImmSel from Form and property {visImmSel_value}")

next_url = "https://portalebanchedatij.visura.it/Visure/vimm/SceltaVisuraImmSoggIMM.do"
print(f"INTESTATI {next_url}")
print(f"visImmSel: {form_data["visImmSel"]}")
texto = form_data["visImmSel"]
# "388326#388326#T#9#5731#C894#0002121## #COLOGNO AL SERIO"
# 388326#388326#T#9#5731#C894#0002121## #COLOGNO AL SERIO
# https://portalebanchedatij.visura.it/Visure/vimm/SceltaVisuraImmSoggIMM.do
data_form = {
    "visImmSel": visImmSel_value,
    "intestati": "Intestati"
}

headers = {
    "Referer": "https://portalebanchedatij.visura.it/Visure/vimm/AssenzaSubalterno.do",
    "Origin": "https://portalebanchedatij.visura.it",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
}

loggato = session.post(next_url, data=data_form, headers=headers)
print("➡️ Conferma INTESTATI Form:", loggato.status_code)

with open("step11_INTESTATI.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)


# tal vez un indietro


# Close Session ❌
close_session_url = "https://portalebanchedatij.visura.it/ECMBKE/Session/Terminate"
print(f"URL Page for closing session {close_session_url}")
close_session_form = {
    "funzione": "chiudi"
}
loggato = session.post(close_session_url, data=close_session_form)
print("➡️ Session close status:", loggato.status_code)

with open("last_step_close.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)


session.close()# Cerrar la sesión de requests

"""
    resp_next = session.post(next_url, data=form_data)
    print("➡️ Step 5 SceltaLink.do status:", resp_next.status_code)

    with open("step5_scelta.html", "w", encoding="utf-8") as f:
        f.write(resp_next.text)

    print("✅ Se ha enviado el request hacia portalebanchedatij")
"""