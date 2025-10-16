import requests
from bs4 import BeautifulSoup

# importing Login data from config file for security and privacy
from config import login_data

FOGLIO = "09"
PARTICELLA = "5731"

# Functions
def writeHTMLfromResponse(response, fileName="response"):
    with open(f"{fileName}.html", "w", encoding="utf-8") as f:
        f.write(response.text)


def requestResponse(session, url, data="", headers="", method="POST"):
    if method in ["GET", "get"]:
        response = session.get(url, headers=headers)
    else:
        response = session.post(url, data=data, headers=headers)
    print("status: ", response.status_code)

    with open("step1_login.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    return response


def main():
    # 🔧 Crear sesión persistente
    session = requests.Session()

    # 1 Login in https://portaleingmonza.visura.it/

    url = "https://portaleingmonza.visura.it/authenticateNuovoVisura.do"

    response = requestResponse(session, url, login_data)
    writeHTMLfromResponse(response, "step_1")

    # 2 CLICK on accessoRapido('agenziadelterritorioIF', 0) in https://portaleingmonza.visura.it/homepageAccessoRapidoActionNuovoVisura.do

    url = "https://portaleingmonza.visura.it/homepageAccessoRapidoActionNuovoVisura.do"
    data = {
        "numBancaDati": "",
        "disabilitaAccessoRapido": "0",
        "codiceGrpServBke": "agenziadelterritorioIF",
        "idAreaTematica": ""
    }

    response = session.post(url, data=data)
    print("status:", response.status_code)

    with open("step2_accessoRapido.html", "w", encoding="utf-8") as f:
        f.write(response.text)


    # 3 CLICK on accedi

    url = "https://portaleingmonza.visura.it/homepageBancheDatiAction1NuovoVisura.do"
    data = {
        "azione": "entra",
        "numBancaDati": "1",
        "codiceGrpSrv": "agenziadelterritorioIF",
        "numLink": ""
    }

    response = session.post(url, data=data)
    print("status:", response.status_code)

    with open("step3_submit.html", "w", encoding="utf-8") as f:
        f.write(response.text)


    # 4 Getting Payload for https://portalebanchedatij.visura.it/homepageBancheDatiAction1NuovoVisura.do Form


    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form", attrs={"action":"/homepageBancheDatiAction1NuovoVisura.do"})

    if not form:
        print("⚠️ Redirecting Form to portalebanchedatij NOT FOUND")
    else:
        url = "https://portalebanchedatij.visura.it/" + form["action"]
        data = {}
        for inp in form.find_all("input"):
            name = inp.get("name")
            value = inp.get("value", "")
            if name:
                data[name] = value
        
        print(f"✅ Form data collected from {response.next}")

    # 5 Setting payload for submitting form 
    url = data["loginbd"]
    response = session.post(url, data=data)
    print("status:", response.status_code)

    with open("step5_redirect.html", "w", encoding="utf-8") as f:
        f.write(response.text)


    # 6 Getting HTML of "Servizi" from portalebanchedatij.visura.it

    url = "https://portalebanchedatij.visura.it/Servizi/"
    response = session.get(url)
    print("➡️ servizi Form:", response.status_code)

    with open("step6_framset.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    # 7 Selecting "Visure Castatali" link

    url = "https://portalebanchedatij.visura.it/Visure/Informativa.do?tipo=/T/TM/VCVC_"
    response = session.post(url, data="")
    print("status:", response.status_code)

    with open("step7_conferma.html", "w", encoding="utf-8") as f:
        f.write(response.text)


    # 8 Selecting searching for "inmmobile" and getting HTML
    url = "https://portalebanchedatij.visura.it/Visure/SceltaServizio.do?tipo=/T/TM/VCVC_"
    print(f"URL page for conferma {url}")
    response = session.get(url)
    print("status", response.status_code)

    with open("step8_conferma.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    # 9 Setting "Provincia" in this example is BERGAMO

    url = "https://portalebanchedatij.visura.it/Visure/DataRichiesta.do"
    data = {
        "listacom": "BERGAMO Territorio-BG"
    }
    response = session.post(url, data=data)
    print("status:", response.status_code)

    with open("step9_provincia.html", "w", encoding="utf-8") as f:
        f.write(response.text)


    # 10 Click on confirmation button
    # <li><a href="/Visure/SceltaLink.do?lista=IMM&amp;codUfficio=BG">Immobile</a></li>	

    url = "https://portalebanchedatij.visura.it/Visure/SceltaLink.do?lista=IMM&codUfficio=BG"
    data = {
        "listacom": "BERGAMO Territorio-BG"
    }
    response = session.get(url)
    print("status", response.status_code)

    with open("step10_IMMOBILE.html", "w", encoding="utf-8") as f:
        f.write(response.text)


    # 11 Searching for "Immobile" 

    url = "https://portalebanchedatij.visura.it/Visure/vimm/RicercaIMM.do"
    data = {
        "tipoCatasto": "T",
        "denomComune" : "C894#COLOGNO AL SERIO#0#0",
        "selSezione" : "",
        "sezione": "",
        "tipoIdentificativo": "d",
        "sezUrb": "",
        "foglio": FOGLIO,
        "particella1": PARTICELLA,
        "particella2": "",
        "subalterno1" : "",
        "tipoDenuncia" : "",
        "numero1": "",
        "anno" : "",
        "richiedente": "",
        "motivoText" : "",
        "scelta": "Ricerca"
    }
    response = session.post(url, data=data)
    print("status:", response.status_code)

    with open("step11_IMMOBILE.html", "w", encoding="utf-8") as f:
        f.write(response.text)


    # 12 Confirm "Assenza di subalterno" for forwarding requests
    # value="C894#COLOGNO AL SERIO#0#0"

    url = "https://portalebanchedatij.visura.it/Visure/vimm/AssenzaSubalterno.do"
    print(f"URL page for selecting 'IMMOBILE' {url}")
    data = {
        "confAssSub": "Conferma",
        "denomComune" : "C894#COLOGNO AL SERIO#0#0",
        "nomeComune": "COLOGNO AL SERIO",
        "codiceComune": "C894",
        "tipoCatasto": "T",
        "sezione" : "",
        "tipoIdentificativo": "d",
        "sezUrb": "",
        "foglio": FOGLIO,
        "particella1": PARTICELLA,
        "particella2": "",
        "subalterno1" : "",
        "subalterno2" : "",
        "tipoDenuncia" : "",
        "numero1": "",
        "anno" : "",
        "scelta": "Ricerca"
    }
    response = session.post(url, data=data)
    print("status:", response.status_code)

    with open("step12_RICHIESTA.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    from html2image import Html2Image

    soup = BeautifulSoup(response.text, "html.parser")
    pagina = soup.select_one("div.pagina")


    import os

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    print("Ruta del script:", script_path)
    print("Directorio del script:", script_dir)

    ABSOLUTE_PATH = script_dir

    html_fragment = f"""
        <html>
        <head>
        
		<link media="screen" rel="stylesheet" href="{ABSOLUTE_PATH}/css_sister/sister.css" type="text/css">
		<link media="screen" rel="stylesheet" href="{ABSOLUTE_PATH}/css_sister/style_new.css" type="text/css">
        <!-- 		<link media="print" rel="stylesheet" href="/css_sister/print.css" type="text/css"> -->
		<!--[if IE 6]><link rel="stylesheet" type="text/css" href="/css_sister/ie6.css"><![endif]-->
		<!--[if IE 7]><link rel="stylesheet" type="text/css" href="/css_sister/ie7.css"><![endif]-->
		<!--[if IE 8]><link rel="stylesheet" type="text/css" href="/css_sister/ie8.css"><![endif]-->
		<!--[if IE 9]><link rel="stylesheet" type="text/css" href="/css_sister/ie9.css"><![endif]-->

		<!-- CSS per importare Bootstrap -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/bootstrap.min.css" />
		<!-- CSS per importare FontAwesome -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/font-awesome.min.css" />
		<!-- CSS per importare il font Titillium -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/titillium.css" />
		<!-- CSS comune per tutte le applicazioni -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/common.css" />
		<!-- CSS comune per l'header e il footer -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/header-footer.css" />
		<!-- CSS comune per i menu -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/menu.css" />
		<!-- CSS specifico per l'Agenzia -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/agenzia-entrate.css" />
		<!-- CSS specifico di ogni applicazione (l'unico da modificare) -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/app.css" />
		
		<link media="print" rel="stylesheet" href="{ABSOLUTE_PATH}/css/print_new.css" type="text/css">
        </head>
        <body style="padding: 20px;">
        {pagina}
        </body>
        </html>
        """

    hti = Html2Image(browser='chrome', size=(1280, 1024))
    hti.screenshot(html_str=html_fragment, save_as="fragment.png")

    print("✅ Imagen generada: fragment.png")

    # 13 Getting form information from SceltaVisuraImmSoggForm in response before
    # /Visure/vimm/SceltaVisuraImmSoggIMM.do

    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form", attrs={"action":"/Visure/vimm/SceltaVisuraImmSoggIMM.do"})

    if not form:
        print("⚠️ Form from VISURE CATASTALI not found")
    else:
        url = "https://portalebanchedatij.visura.it/" + form["action"]
        form_data = {}
        for inp in form.find_all("input"):
            name = inp.get("name")
            value = inp.get("value", "")
            if name:
                form_data[name] = value
        
        visImmSel_value = soup.find("input", {"property": "visImmSel"}).get("value")

    print(f"Step 13 getting visImmSel from response {visImmSel_value}")
    # 14 Looking in "Intestati"

    url = "https://portalebanchedatij.visura.it/Visure/vimm/SceltaVisuraImmSoggIMM.do"
    # "388326#388326#T#9#5731#C894#0002121## #COLOGNO AL SERIO"
    # 388326#388326#T#9#5731#C894#0002121## #COLOGNO AL SERIO
    # https://portalebanchedatij.visura.it/Visure/vimm/SceltaVisuraImmSoggIMM.do
    data = {
        "visImmSel": visImmSel_value,
        "intestati": "Intestati"
    }

    headers = {
        "Referer": "https://portalebanchedatij.visura.it/Visure/vimm/AssenzaSubalterno.do",
        "Origin": "https://portalebanchedatij.visura.it",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
    }

    response = session.post(url, data=data, headers=headers)
    print("status:", response.status_code)

    with open("step14_INTESTATI.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    
    soup = BeautifulSoup(response.text, "html.parser")
    pagina = soup.select_one("div.pagina")

    print(pagina)
    with open("pagina.html", "w", encoding="utf-8") as paginaHTML:
        paginaHTML.write(pagina.contents[0])


    html_fragment = f"""
        <html>
        <head>
        
		<link media="screen" rel="stylesheet" href="{ABSOLUTE_PATH}/css_sister/sister.css" type="text/css">
		<link media="screen" rel="stylesheet" href="{ABSOLUTE_PATH}/css_sister/style_new.css" type="text/css">
        <!-- 		<link media="print" rel="stylesheet" href="/css_sister/print.css" type="text/css"> -->
		<!--[if IE 6]><link rel="stylesheet" type="text/css" href="/css_sister/ie6.css"><![endif]-->
		<!--[if IE 7]><link rel="stylesheet" type="text/css" href="/css_sister/ie7.css"><![endif]-->
		<!--[if IE 8]><link rel="stylesheet" type="text/css" href="/css_sister/ie8.css"><![endif]-->
		<!--[if IE 9]><link rel="stylesheet" type="text/css" href="/css_sister/ie9.css"><![endif]-->

		<!-- CSS per importare Bootstrap -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/bootstrap.min.css" />
		<!-- CSS per importare FontAwesome -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/font-awesome.min.css" />
		<!-- CSS per importare il font Titillium -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/titillium.css" />
		<!-- CSS comune per tutte le applicazioni -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/common.css" />
		<!-- CSS comune per l'header e il footer -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/header-footer.css" />
		<!-- CSS comune per i menu -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/menu.css" />
		<!-- CSS specifico per l'Agenzia -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/agenzia-entrate.css" />
		<!-- CSS specifico di ogni applicazione (l'unico da modificare) -->
		<link rel="stylesheet" href="{ABSOLUTE_PATH}/resources/css/app/app.css" />
		
		<link media="print" rel="stylesheet" href="{ABSOLUTE_PATH}/css/print_new.css" type="text/css">
        </head>
        <body style="padding: 20px;">
        {pagina}
        </body>
        </html>
        """

    hti = Html2Image(browser='chrome', size=(1280, 1024))
    hti.screenshot(html_str=html_fragment, save_as="intestati.png")


    # 15 Getting list of "nominativi"
    soup = BeautifulSoup(response.text, "html.parser")
    nominativi = soup.find_all("td", headers="nominativo")
    print(f"Nominativi found: {[content.contents[0] for content in nominativi]}")


    # tal vez un indietro


    # Close Session ❌
    url = "https://portalebanchedatij.visura.it/ECMBKE/Session/Terminate"
    print(f"URL Page for closing session {url}")
    data = {
        "funzione": "chiudi"
    }
    response = session.post(url, data=data)
    print("➡️ Session close status:", response.status_code)

    with open("last_step_close.html", "w", encoding="utf-8") as f:
        f.write(response.text)


    session.close()


if __name__ == '__main__':
    main()