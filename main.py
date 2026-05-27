import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdg-irtyPcjn_oV7B1WOngT7PExdHzvbKMS4HsVD9hJz2JN9w/viewform?usp=header"


driver = webdriver.Chrome()
driver.maximize_window()
driver.get(FORM_LINK)
WebDriverWait(driver, 2)

response = requests.get(url= "https://appbrewery.github.io/Zillow-Clone/")
soup = BeautifulSoup(response.text, "html.parser")

all_links = [link.get('href') for link in soup.find_all(name= "a", class_ = "property-card-link")]

all_prices = [price.getText().split('+')[0].split('/')[0]
              for price in soup.find_all(name = "span", class_ = "PropertyCardWrapper__StyledPriceLine")
              ]

all_address = [address.getText().strip().replace(' |', '')
               for address in soup.find_all(name ="address", attrs ={"data-test": "property-card-addr"})
               ]

all_info = zip(all_links, all_prices, all_address)
for info in all_info:
    text_input = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    text_input[0].send_keys(info[2])
    text_input[1].send_keys(info[1])
    text_input[2].send_keys(info[0])

    driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a").click()
    sleep(1)
    print(f"Successfully submitted entry {info[2]}")

print("All done successfully!")
