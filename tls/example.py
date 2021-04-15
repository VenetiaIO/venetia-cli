import ghttp as client, random
import time, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

hh =  [['Host', "collector-pxu6b0qd2s.px-cloud.net"], ['sec-ch-ua', '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"'], ['sec-ch-ua-mobile', '?0'], [ 'user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'], ['content-type', 'application/x-www-form-urlencoded'], [ 'accept', '*/*'], ['origin', 'https://www.walmart.com'], [ 'sec-fetch-site', 'cross-site'], [ 'sec-fetch-mode', 'cors'], ['sec-fetch-dest', 'empty'], ['referer', 'https://www.walmart.com/'], ['accept-language', 'en-US,en;q=0.9'], [":path", ""], [":scheme", ""], [":authority", ""], [":method", ""]]

def lol():
    try:
        s = client.Session("", client.JA3Fingerprint("k"), timeout=2)
        for _ in range(MULTIPLES):
            y = s.get("https://http2.golang.org/reqinfo", headers=hh)
            #print(y.status)
    except Exception as e:
        print("     exception:", e)
        pass
MULTIPLES = 5
with ThreadPoolExecutor(max_workers=200) as ex:
    NUM_TASKS = 1
    tasks = (ex.submit(lol) for _ in range(NUM_TASKS))
    start = time.time()
    for i, _ in enumerate(as_completed(tasks)):
        i = (i+1)*MULTIPLES
        sys.stderr.write(f"\r\r\r {i}")
    print()
    print(NUM_TASKS*MULTIPLES, "took", time.time() - start, "seconds")

# lol()