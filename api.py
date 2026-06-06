import requests

while True:
    try:
        country = input("Enter a country name: ")
        response = requests.get(
            "https://restcountries.com/v3.1/name/" + country)
        data = response.json()
        country_data = data[0]
        print("Country: " + country_data["name"]["common"])
        print("Capital: " + country_data["capital"][0])
        print("Population: " + str(country_data["population"]))
        print("Region: " + country_data["region"])
        currencies = country_data["currencies"]
        currency_code = list(currencies.keys())[0]
        print("Currency: " + currencies[currency_code]["name"])
        print("Symbol: " + currencies[currency_code]["symbol"])
        break
    except:
        print("Country not found! Please try again.")
