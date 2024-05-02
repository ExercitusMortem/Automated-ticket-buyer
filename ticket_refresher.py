import selenium
import requests
import pygetwindow as gw
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from win10toast import ToastNotifier

print('Ticket refresher v0.1, by Giovani van Dorland')

toast = ToastNotifier()
driver = webdriver.Chrome()

# URL of the webpage
# url = "https://atleta.cc/e/zRLhVgiDSdOK/resale"

url = 'https://atleta.cc/e/zRLhVgiDSdOK/resale'
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver=webdriver.Chrome(options=options)
driver.get(url)


# GraphQL API endpoint URL
url = "https://atleta.cc/api/graphql"

payload = {'operationName': 'GetRegistrationsForSale', 
           "variables":{"id":"zRLhVgiDSdOK","tickets":None,"limit":10}, 
           'query' : 'query GetRegistrationsForSale($id: ID!, $tickets: [String!], $limit: Int!) {  event(id: $id) {    id    registrations_for_sale_count    filtered_registrations_for_sale_count: registrations_for_sale_count(      tickets: $tickets    )    sold_registrations_count    tickets_for_resale {      id      title      __typename    }    registrations_for_sale(tickets: $tickets, limit: $limit) {      id      ticket {        id        title        __typename      }      ticket {        id        title        __typename      }      time_slot {        id        start_date        start_time        title        multi_date        __typename      }      promotion {        id        title        __typename      }      upgrades {        id        product {          id          title          is_ticket_fee          __typename        }        product_variant {          id          title          __typename        }        __typename      }      resale {        id        available        total_amount        fee        public_url        public_token        __typename      }      __typename    }    __typename  }}'}

def bring_chrome_to_front():
    chrome_windows = gw.getWindowsWithTitle('Google Chrome')
    if chrome_windows:
        # Get the first Chrome window
        chrome_window = chrome_windows[0]
        # Activate the Chrome window
        chrome_window.activate()
    else:
        print("Google Chrome is not open.")


def check_amount_of_tickets():
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        responsejson = response.json()
        registrations_for_sale = responsejson['data']['event']['registrations_for_sale']
        print(len(registrations_for_sale))
        if len(registrations_for_sale)>0:
            for registration in registrations_for_sale:
                if registration['resale']['available']:
                    toast.show_toast(
                        "Kaartje",
                        "Een kaartje is beschikbaar!",
                        duration = 10,
                        icon_path = "icon.ico",
                        threaded = True,
                    )
                    button = driver.find_element(By.LINK_TEXT, "Vernieuwen")
                    bring_chrome_to_front()
                    button.click()


while True:
    check_amount_of_tickets()  
    sleep(11)
    

