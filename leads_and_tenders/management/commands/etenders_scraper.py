# yourapp/management/commands/scrape_etenders.py
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
from leads_and_tenders.models import Tender  # Replace 'yourapp' with the actual name of your Django app
import time


class Command(BaseCommand):
    help = 'Scrape eTenders website and save data to the database'

    def handle(self, *args, **options):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.page_load_strategy = 'normal'
        driver = webdriver.Chrome(options=options)

        try:
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
                    time.sleep(1)

                    # Use BeautifulSoup to parse the updated HTML content of the page
                    soup = BeautifulSoup(driver.page_source, "html.parser")

                    # Use the updated_row variable to find the desired elements
                    updated_row = soup.find(id='tendeList').find('tbody').find_all("tr", attrs={'role': 'row'})[i].find_next('tr')


                    gravy = BeautifulSoup(f'"""{updated_row}"""', "html.parser")

                    # Find the row containing the "Closing Date:" information
                    tender_ref = gravy.find('td', string='Tender Number:').find_next('td')
                    print(tender_ref)

                    # Find the row containing the "Closing Date:" information
                    closing_date_row = gravy.find('td', string='Closing Date:').find_next('td')

                    # Find the row containing the "Briefing Date and Time:" information
                    briefing_date_row = gravy.find('td', string='Briefing Date and Time:').find_next('td')

                    # Extract the text content from the found rows
                    closing_date = closing_date_row.get_text(strip=True)
                    briefing_date = briefing_date_row.get_text(strip=True)

                    closing_date_object = ''
                    briefing_date_object = ''

                    if closing_date != '':
                        closing_date_object = datetime.strptime(closing_date, "%A, %d %B %Y - %H:%M")
                        
                    if briefing_date != '':
                        briefing_date_object = datetime.strptime(briefing_date, "%A, %d %B %Y - %H:%M")

                    if closing_date_object != '' and briefing_date_object != '':
                        tender = Tender(
                            refNum=tender_ref.get_text(strip=True),
                            summary=tender_summary,
                            siteInspectionDate=briefing_date_object,
                            closingDate=closing_date_object,
                            description = updated_row.prettify()
                            # Add other fields as needed
                        )
                        tender.save()
                    else:
                        tender = Tender(
                            refNum=tender_ref.get_text(strip=True),
                            summary=tender_summary,
                            closingDate=closing_date_object,
                            description = updated_row.prettify()
                            # Add other fields as needed
                        )
                        tender.save()
                        
                    # Print or manipulate the updated row's HTML content
                    if updated_row:
                        pass
                        # print(updated_row.prettify())

                except Exception as e:
                    print(f"Error clicking button in row {i}: {e}")

        finally:
            driver.quit()

        self.stdout.write(self.style.SUCCESS('Scraping completed successfully.'))
