from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import pprint
import csv

# load the linkedin credentials from env file
load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')


#parse company urls
obj = open('output/company-urls.txt', 'r')
company_urls = obj.readlines()
obj.close()

# create output file
obj = open('output/output.csv', 'w')

# set the driver executable path
cwd_path = os.getcwd() 
os.chdir('driver')
cwd_path_path = os.getcwd() 
driver_path = os.path.join(cwd_path, 'chromedriver')

# create a selenium driver and service
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# login url
login_url = "https://www.linkedin.com/login"

#login to linkedin
driver.get(login_url)
driver.find_element(By.XPATH, '''//input[@name="session_key"]''').send_keys(username)
driver.find_element(By.XPATH, '''//input[@name="session_password"]''').send_keys(password)

button_obj = driver.find_element(By.XPATH, '''//button[@type="submit"]''')
button_obj.click()


'''
Navigation to the company URLS 
'''

# populate company_dict with employeeCount

company_count_details = {'CompanyUrl': [], 'EmployeeCount': []}

for company_url in company_urls:
    driver.get(company_url)
    driver.implicitly_wait(3000)
    try:
        employee_count = driver.find_element(By.XPATH, '''//div[@class="inline-block"]/a/span''').text
        count = employee_count.split(' ')[0]
        company_count_details['CompanyUrl'].append(company_url)  # remove newline from url and store the company name
        company_count_details['EmployeeCount'].append(count)
    except Exception as e:
        print('employee count details not found for: ' + company_url.split('/')[-1])
        company_count_details['CompanyUrl'].append(company_url)
        company_count_details['EmployeeCount'].append(0)

driver.close()
driver.quit()

# debug purpose
pprint.pprint(company_count_details)

# Write the CSV file with companyURLs and EmployeeCounts
field_names = ['CompanyUrl', 'EmployeeCount']

writer = csv.writer(obj)
writer.writerow(company_count_details.keys())
writer.writerows(zip(*company_count_details.values()))

# closing the resources
obj.close()

print('employee count details written successfully!!')






