import requests


LOGIN_URL = "https://portaleingmonza.visura.it/homepageBancheDatiAction.do"
URL_AUTH = "https://portaleingmonza.visura.it/authenticateNuovoVisura.do"
TARGET_URL = "https://portalebanchedatij.visura.it/framesetAgenziaTerritorioIF.htm"

payload = {
    "userName": "****",
    "password": "****",
    "otp": "",        # si no es obligatorio, lo dejamos vacío
    "forward": "",    # hidden
}


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Content-Type": "application/x-www-form-urlencoded",
}

def main():
    session = requests.Session()
    # 1. Hacer login
    resp = session.post(LOGIN_URL, data=payload, headers=headers)

    print("Login status:", resp.status_code)
    cookies = session.cookies.get_dict()
    print("Cookies después del login:", cookies)
    # 2. Acceder a la página protegida
    protected_url = "https://portalebanchedatij.visura.it/framesetAgenziaTerritorioIF.htm"
    resp2 = requests.get(protected_url, headers=headers, cookies=cookies)

    print("Protegida status:", resp2.status_code)
    print(resp2.text[:1000])  # primeras 1000 líneas de HTML



if __name__ == "__main__":
    main()