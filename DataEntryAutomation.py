import bs4
from selenium import webdriver
import requests
import time


# Initial Setup


class Data_entry:
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
        }
        self.edge_driver_path = "C:\Development\msedgedriver.exe"
        self.URL_rents = "https://www.zillow.com/new-york-ny/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D" \
                         "%2C%22usersSearchTerm%22%3A%22New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74" \
                         ".07514694889933%2C%22east%22%3A-73.87430313786417%2C%22south%22%3A40.67299705638982%2C%22north%22" \
                         "%3A40.777331772787704%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22" \
                         "%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C" \
                         "%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B" \
                         "%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse" \
                         "%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22" \
                         "%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22" \
                         "%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah" \
                         "%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D "
        self.URL_form = "https://forms.gle/a3kkWGtaGSVAt7qF6"

    def scrape(self):
        # Scraping the info
        response = requests.get(url=self.URL_rents, headers=self.header)  # Getting the HTML code
        html_code = response.text
        soup = bs4.BeautifulSoup(html_code, "html.parser")  # Parsing it

        # Extracting the data for the price, address and link and convert them to list
        price_tag_list = soup.find_all(name="div", class_="list-card-price")
        price_list = [price_tag.getText() for price_tag in price_tag_list]
        address_tag_list = soup.find_all(name="address", class_="list-card-addr")
        address_list = [link_tag.getText() for link_tag in address_tag_list]
        link_tag_list = soup.find_all(name="a", class_="list-card-link list-card-link-top-margin", href=True)
        link_list = [linkcard_tag["href"] for linkcard_tag in link_tag_list]

        return address_list, price_list, link_list

    def navigate_form(self, addresses, prices, links):
        driver = webdriver.Edge(executable_path=self.edge_driver_path)

        for rental in range(len(addresses)):
            driver.get(url=self.URL_form)
            location = driver.find_element_by_css_selector("#mG61Hd > div.freebirdFormviewerViewFormCard"
                                                           ".exportFormCard > div > "
                                                           "div.freebirdFormviewerViewItemList > div:nth-child(1) > "
                                                           "div > div > "
                                                           "div.freebirdFormviewerComponentsQuestionTextRoot > div > "
                                                           "div.quantumWizTextinputPaperinputMainContent.exportContent > div > div.quantumWizTextinputPaperinputInputArea > input")
            price = driver.find_element_by_css_selector("#mG61Hd > div.freebirdFormviewerViewFormCard.exportFormCard "
                                                        "> div > div.freebirdFormviewerViewItemList > div:nth-child("
                                                        "2) > div > div > "
                                                        "div.freebirdFormviewerComponentsQuestionTextRoot > div > "
                                                        "div.quantumWizTextinputPaperinputMainContent.exportContent > "
                                                        "div > div.quantumWizTextinputPaperinputInputArea > input")
            link_input = driver.find_element_by_css_selector("#mG61Hd > div.freebirdFormviewerViewFormCard.exportFormCard > "
                                                      "div > div.freebirdFormviewerViewItemList > div:nth-child(3) > "
                                                      "div > div > div.freebirdFormviewerComponentsQuestionTextRoot > "
                                                      "div > "
                                                      "div.quantumWizTextinputPaperinputMainContent.exportContent > "
                                                      "div > div.quantumWizTextinputPaperinputInputArea > input")
            send_button = driver.find_element_by_css_selector("#mG61Hd > div.freebirdFormviewerViewFormCard"
                                                              ".exportFormCard > div > "
                                                              "div.freebirdFormviewerViewNavigationNavControls > "
                                                              "div.freebirdFormviewerViewNavigationButtonsAndProgress > "
                                                              "div > div > span > span")
            time.sleep(1)
            location.send_keys(f"{address_list[rental]}")
            time.sleep(0.5)
            price.send_keys(f"{prices[rental]}")
            time.sleep(0.5)
            link_input.send_keys(f"{links[rental]}")
            send_button.click()
            time.sleep(1)

        driver.quit()


data = Data_entry()
address_list, price_list, link_list = data.scrape()
data.navigate_form(address_list, price_list, link_list)
