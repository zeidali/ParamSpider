import requests
import random
import time

def connector(url):
    result = False
    user_agent_list = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        # Firefox / Trident
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'
    ]
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}

    retry = False
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.text
    except requests.exceptions.ConnectionError:
        print("\u001b[31;1m[!] Connection error. Check your internet.\u001b[0m")
    except requests.exceptions.Timeout:
        print("\u001b[31;1m[!] Timeout. Retrying in 2 seconds...\u001b[0m")
        retry = True
        time.sleep(2)
    except requests.exceptions.HTTPError as err:
        print(f"\u001b[31;1m[!] HTTP Error: {err}. Retrying in 2 seconds...\u001b[0m")
        retry = True
        time.sleep(2)
    except requests.exceptions.RequestException as e:
        print(f"\u001b[31;1m[!] Request failed: {e}\u001b[0m")
        print("\u001b[31;1mReport bugs here: https://github.com/0xKayala/ParamSpider/issues\u001b[0m")
        retry = True
    except KeyboardInterrupt:
        print("\u001b[31;1m[!] Interrupted by user\u001b[0m")
        raise SystemExit

    return result, retry
