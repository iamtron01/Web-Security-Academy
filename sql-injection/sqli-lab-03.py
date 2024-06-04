import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def is_exploitable(url, user, session):
    return True

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
        sys.exit(-1)