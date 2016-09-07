import client, time
from concurrent.futures import ThreadPoolExecutor


keyword = "software -senior -lead"
target_countries = [
        "fi",
        "de",
        "se"
]

cl = client.getClient();


#periodic job:
with ThreadPoolExecutor(max_workers=len(target_countries)) as executor:
        futures = {executor.submit(cl.queryAll, keyword, "", country) for country
                in target_countries}

        #wait for 2 hours:
        #time.sleep(60*60*2)
        #busywait?
        while(not any(futures)):
            pass
'''
import cProfile
cProfile.run("cl.queryAll(keyword, \"\", \"fi\")")
'''
