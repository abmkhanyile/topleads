from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime
from leads_and_tenders.models import Tender

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)

driver.get("https://www.etenders.gov.za/Home/opportunities?id=1")

table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "tendeList"))
)

tbody = table.find_element(By.TAG_NAME, "tbody")

rows = WebDriverWait(tbody, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
)

for i, row in enumerate(rows):
    cells = row.find_elements(By.TAG_NAME, "td")
    tender_summary = cells[2].get_attribute("innerHTML")
    published_date = cells[3].get_attribute("innerHTML")

    # Use a relative XPath starting from the current row
    try:
        # Wait for the element to be clickable
        button = WebDriverWait(row, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'details-control'))
        )
        
        button.click()

        # Wait for the new content to load (you may need to adjust the waiting time)
        time.sleep(3)

        # Use BeautifulSoup to parse the updated HTML content of the page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Use the updated_row variable to find the desired elements
        updated_row = soup.find(id='tendeList').find('tbody').find_all("tr", attrs={'role': 'row'})[i].find_next('tr')


        gravy = BeautifulSoup(f'"""{updated_row}"""', "html.parser")

        # Find the row containing the "Closing Date:" information
        closing_date_row = gravy.find('td', string='Closing Date:').find_next('td')

        # Find the row containing the "Briefing Date and Time:" information
        briefing_date_row = gravy.find('td', string='Briefing Date and Time:').find_next('td')

        # Extract the text content from the found rows
        closing_date = closing_date_row.get_text(strip=True)
        briefing_date = briefing_date_row.get_text(strip=True)

        # print(f'Closing Date: {closing_date}')
        # print(f'Briefing Date and Time: {briefing_date}')
        if closing_date != '':
            closing_date_object = datetime.strptime(closing_date, "%A, %d %B %Y - %H:%M")
            print(closing_date_object)


        if briefing_date != '':
            briefing_date_object = datetime.strptime(briefing_date, "%A, %d %B %Y - %H:%M")
            print(briefing_date_object)
        else:
            print("its empty")




        # Print or manipulate the updated row's HTML content
        if updated_row:
            pass
            # print(updated_row.prettify())

    except Exception as e:
        print(f"Error clicking button in row {i}: {e}")

# Quit the webdriver when done
driver.quit()
