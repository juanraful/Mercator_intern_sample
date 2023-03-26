import pandas as pd
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
options = webdriver.ChromeOptions()
options.add_argument("""--enable-javascript""")
driver = webdriver.Chrome()
driver.maximize_window()
time.sleep(5)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver.get('https://secure.toronto.ca/ApplicationStatus/setup.do?action=init')

address_box=driver.find_elements(By.ID,"address")[0]
address_box.send_keys("33 Isabella St")

send_button=driver.find_elements(By.ID,"submitButton")[0]
send_button.click()
time.sleep(35)

results_link=driver.find_elements(By.ID,"showResultsLink")[0]
driver.execute_script("arguments[0].click();", results_link)
time.sleep(3)

data=pd.DataFrame(columns=['Application#', 'Application Type', 'Date', 'Status', 'ProjectName'])
for page_num in range(77):
    result_table=driver.find_elements(By.TAG_NAME,'table')[0]
    result_rows=result_table.find_elements(By.TAG_NAME,'tr')
    for project in result_rows[1:]:
        project_element=project.find_elements(By.TAG_NAME,'td')
        if len(project_element)>0:
            project_name=project_element[0].text
            driver.execute_script("arguments[0].click();", project)
            time.sleep(2)
            updated_result_table=driver.find_elements(By.TAG_NAME,'table')[0]
            soup=bs(updated_result_table.get_attribute('innerHTML'),'html.parser')
            project_history=pd.read_html(str(soup))[0]
            project_history['ProjectName']=project_name
            driver.execute_script("arguments[0].click();", project)
            data=pd.concat([data, project_history],axis=0)
    next_button=driver.find_elements(By.ID,"DataTables_Table_0_next")[0]
    driver.execute_script("arguments[0].click();", next_button)
    time.sleep(1)
        

data.to_csv('Toronto_building_permit_info.csv')

# Analysis