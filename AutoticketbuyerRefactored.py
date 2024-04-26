import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

class AtletaScraper:
    def __init__(self, event_url):
        self.event_url = event_url
        self.graphql_url = "https://atleta.cc/api/graphql"
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=options)

    def _get_registrations_for_sale(self):
        payload = {
            'operationName': 'GetRegistrationsForSale',
            'variables': {"id": "zRLhVgiDSdOK", "tickets": None, "limit": 10},
            'query': 'query GetRegistrationsForSale($id: ID!, $tickets: [String!], $limit: Int!) {  event(id: $id) {    id    registrations_for_sale_count    filtered_registrations_for_sale_count: registrations_for_sale_count(      tickets: $tickets    )    sold_registrations_count    tickets_for_resale {      id      title      __typename    }    registrations_for_sale(tickets: $tickets, limit: $limit) {      id      ticket {        id        title        __typename      }      ticket {        id        title        __typename      }      time_slot {        id        start_date        start_time        title        multi_date        __typename      }      promotion {        id        title        __typename      }      upgrades {        id        product {          id          title          is_ticket_fee          __typename        }        product_variant {          id          title          __typename        }        __typename      }      resale {        id        available        total_amount        fee        public_url        public_token        __typename      }      __typename    }    __typename  }}'}

        response = requests.post(self.graphql_url, json=payload)
        if response.status_code == 200:
            return response.json()['data']['event']['registrations_for_sale']
        else:
            return None

    def scrape(self):
        self.driver.get(self.event_url)
        while True:
            registrations_for_sale = self._get_registrations_for_sale()
            if registrations_for_sale:
                for registration in registrations_for_sale:
                    if registration['resale']['available']:
                        public_url = registration['resale']['public_url']
                        print("Registrations for sale count:", len(registrations_for_sale))
                        print('Public link:', public_url)
                        button = self.driver.find_element(By.TAG_NAME, "BUTTON")
                        button.click()
                        self.driver.get(public_url)
                        sleep(4)
                        button = self.driver.find_element(By.TAG_NAME, "BUTTON")
                        button.click()
                        sleep(10)  # Wait for a while before checking again
                        break  # Break the loop if found
                else:
                    # If no available registrations found, wait and retry
                    sleep(10)
            else:
                print("No registrations for sale. Retrying...")
                sleep(10)

if __name__ == "__main__":
    event_url = 'https://atleta.cc/e/zRLhVgiDSdOK/resale'
    scraper = AtletaScraper(event_url)
    scraper.scrape()
