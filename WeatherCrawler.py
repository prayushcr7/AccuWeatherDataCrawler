#Author : Prayush Shrestha

#General Imports
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

options = Options()

#Mapping Month to Month Number
month_to_number = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}
month=''
year = ''
fullDate = ''
# options.add_argument("--headless=new")

#Using Driver for chrome ( Selenium)
driver = webdriver.Chrome(options = options)
#Array for years to crawl add more years depending upon the availabitly in site
yearsToCrawl = ['2023']
#customize months to crawl
monthToCrawl = ['january','february','march','april','may','june','july','august','september','october','november','december']
fileWeather = open('Weather.txt','w')
#Change your region
region = 'kathmandu'
#Creating headings
fileWeather.write('date,temperature\n')


#Function to transform date extracted, date in the website is in the form Jan 11; Changing that
#Date to 2023-01-11
def getFullDate(date, year, month):

    fullDate = f'{year}-{month_to_number.get(month.capitalize())}-{date}'
    return fullDate

#Main function to extract the data, uses base url
def extractData(year,month,baseUrl):
    print(baseUrl)
    driver.get(url=baseUrl)
    time.sleep(5)
    # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'monthly-component')))
    #Extracting the class of date
    dateElements = driver.find_elements(By.CLASS_NAME,'monthly-daypanel')
    count = 0
    ##lopping through dateelements to extract data
    for dateElement in dateElements:
        #extracting the data
        date = dateElement.find_element(By.CLASS_NAME,'date').text

        if count <= 7 and len(date) > 1:
            continue
        elif count > (25) and len(date)<=1:
            continue
        else:
            if(len(date)<2):
                date = f'0{date}'
            fullDate = getFullDate(date,year,month)
            highTemp = dateElement.find_element(By.CLASS_NAME, 'high').text
            lowTemp = dateElement.find_element(By.CLASS_NAME, 'low').text
            averageTemp = (int(highTemp[:-1]) + int(lowTemp[:-1])) / 2
            fileWeather.write(fullDate+','+ str(averageTemp)+'\n')

        count = count+1
    # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'page-content')))

for years in yearsToCrawl:
    year = years
    for months in monthToCrawl:
        month = months
        print(month,year)
        baseUrl = f'https://www.accuweather.com/en/np/{region}/241809/{month}-weather/241809?year={year}'
        extractData(year,month,baseUrl)


driver.close()