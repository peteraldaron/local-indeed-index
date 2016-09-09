import client, time
from concurrent.futures import ThreadPoolExecutor


keyword = "software -senior -lead"
target_countries = [
        "fi",
        "de",
        "se"
]

target_country_names = [
        "Finland",
        "Germany",
        "Sweden"
]

cl = client.getClient();


#periodic job:
with ThreadPoolExecutor(max_workers=len(target_countries)) as executor:
        futures = {executor.submit(cl.queryAll, keyword, city, country) for country
                in target_countries for country_name in target_country_names for city
                in client.readCitiesOfCountryFromJSON(country_name)}

        #wait for 2 hours:
        #time.sleep(60*60*2)
        #busywait?
        while(not any(futures)):
            pass
'''
a = {cl.queryAll(keyword, city, country) for country
                in target_countries for country_name in target_country_names for city
                in client.readCitiesOfCountryFromJSON(country_name)}
'''

'''
    futures = {executor.submit(cl.queryAll, keyword,
        client.readCitiesOfCountryFromJSON(city), country) for country
in target_countries for city in target_country_names}
'''
