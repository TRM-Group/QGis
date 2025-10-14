import requests
from bs4 import BeautifulSoup

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

# -----------------------------
# 5️⃣ Preparar request hacia SceltaLink.do (portalebanchedatij)
# -----------------------------
"""
url next = https://portalebanchedatij.visura.it/framesetAgenziaTerritorioIF.htm
<form name="homepageBancheDatiForm" method="post" action="/homepageBancheDatiAction1NuovoVisura.do">
	<input type="hidden" name="token" value="1760477696579187081726">
	<input type="hidden" name="catalogoEncodato" value="0;0.20|111;6.40|205;0.76|208;15.10|209;15.10|230;2.20|234;2.20|261;6.30|701;0.20|702;0.20|ABBONAMENTOBD_LEGALE;15.00|CATEstrMappaUffDiv;0.60|CATEstrMappaUffRif;0.60|CATIspIpFormEleSint;3.80|CATIspIpFormEleSintUC;3.80|CATIspIpNazRicNom;26.30|CATIspIpNazRicNomUC;7.10|CATIspIpNotaTitolo;7.30|CATIspIpNotaTitoloUC;3.30|CATIspIpNTitDiretto;7.30|CATIspIpNTitDirettoUC;3.30|CATIspIpRicNomImm;12.40|CATIspIpRicNomImmUC;6.00|CATRicCatNazionale;0.60|CATVisCatastale101;0.60|CATVisCatastale102;1.45">
	<input type="hidden" name="idClienteUtente" value="0">
	<input type="hidden" name="clienteUtente" value="">
	<input type="hidden" name="statoSaldo" value="">
	<input type="hidden" name="loginbd" value="https://portalebanchedatij.visura.it:443/ECMBKE/LoginBD">	
</form>
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

    print(f"Form data: {form_data}")
    # Aquí se puede especificar el value del select
    form_data["listaCom"] = "CALTANISSETTA Territorio-CL"  # ejemplo con espacio
    form_data["codUfficio"] = "BG"  # ejemplo, según tu necesidad


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


next_url = "https://portalebanchedatij.visura.it/Servizi/InformativaPrivacy.do"
print(f"URL page for conferma {next_url}")
loggato = session.post(next_url, data="")
print("➡️ Conferma Servizi Form:", loggato.status_code)

with open("step6_conferma.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)


next_url = "https://portalebanchedatij.visura.it/framesetAgenziaTerritorioIF.htm"
print(f"URL page for conferma {next_url}")
loggato = session.get(next_url)
print("➡️ Conferma Servizi Form:", loggato.status_code)

with open("step7_conferma.html", "w", encoding="utf-8") as f:
    f.write(loggato.text)

"""
    resp_next = session.post(next_url, data=form_data)
    print("➡️ Step 5 SceltaLink.do status:", resp_next.status_code)

    with open("step5_scelta.html", "w", encoding="utf-8") as f:
        f.write(resp_next.text)

    print("✅ Se ha enviado el request hacia portalebanchedatij")
"""