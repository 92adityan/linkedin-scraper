from bs4 import BeautifulSoup
import requests
import re
import os

'''
parse the csv file and create a dictionary with company as key and list of 
companies as values . (usage of pandas is ignored as the column size is minimal(Company, employeeCount))
'''

input_file = os.listdir('inputs')[0]
file_obj= open('inputs/' + input_file)

file_data = file_obj.readlines()

input_file_dict = []
company_dict = {'Company':  [], 'EmployeeCount': []}
company_list = []

#parse compant details and store it under the key - company
for company in file_data:
    company_list.append(company.replace('\n', ''))


company_urls = []

print('Please wait as the data is being fetched......')

for company in company_list:
    
    #construct the url with company name and get the HTML response
    url = "https://google.com/search?q="+company
    res = requests.get(url)          
    soup = BeautifulSoup(res.text, 'html.parser')


    '''
        Exeptions were handled for companies where linkedIn URl was not available
        under exception block - enhanced search with company name along with 'linkedin' keyword is passed
                                and searched again to get the profile link
    '''
    try:
        links = soup.find('a', href=re.compile("linkedin.com/company/")).get('href')
       
        # get the exact linkedin url from the result
        company_url = links.split('q=')[1].split('&')[0]
        company_urls.append(company_url)
   
    except Exception as e:
        url = "https://google.com/search?q=" +company+"-linkedin"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        try:
            links = soup.find('a', href=re.compile("linkedin.com/company/")).get('href')
            company_url = links.split('q=')[1].split('&')[0]
            company_urls.append(company_url)

        except Exception as ex:
            print('no data for: ' + company[0])
            company_urls.append("No Data")

#  creating a company_urls file
if os.path.isfile("./output/company-urls.txt"):
    os.remove("./output/company-urls.txt")

file_obj = open('./output/company-urls.txt', "w")
file_obj.write('\n'.join(company_urls))
file_obj.close()

print("company urls written successfully!")
print("Employee count is fetching from the company urls.....")