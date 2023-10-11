import argparse
import requests
import json


class CountryLookup:
    def __init__(self, use_file=False):
        self.use_file = use_file
        self.data = self.load_data()

    def load_data(self):
        if self.use_file:
            try:
                with open("data.json", "r") as file:
                    return json.load(file)
            except FileNotFoundError:
                print("Error: 'data.json' file not found. Please fetch data using '--fetch' option first.")
                return {}
        else:
            response = requests.get("https://www.travel-advisory.info/api")
            if response.status_code != 200:
                print("Error fetching data from the API.")
                return {}
            return response.json().get("data", {})

    def lookup_country_name(self, country_code):
        country_info = self.data.get(country_code, {})
        country_name = country_info.get("name", "Country not found")
        return country_name

    def fetch_and_save_data(self):
        response = requests.get("https://www.travel-advisory.info/api")
        if response.status_code != 200:
            print("Error fetching data from the API.")
            return

        data = response.json()

        with open("data.json", "w") as file:
            json.dump(data, file)
        print("Data saved to 'data.json'.")

def main():
    parser = argparse.ArgumentParser(description="Country code lookup service.")
    parser.add_argument("--countryCode", nargs="+", help="Country code(s) to lookup", required=True)
    parser.add_argument("--fetch", action="store_true", help="Fetch and save data from API")

    args = parser.parse_args()

    country_lookup = CountryLookup(use_file=args.fetch)

    if args.fetch:
        country_lookup.fetch_and_save_data()

    for country_code in args.countryCode:
        country_name = country_lookup.lookup_country_name(country_code)
        print("{0}: {1}".format(country_code, country_name))

if __name__ == "__main__":
    main()
