#filename: Salomon_XAPro3D_Reviews

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import math


driver = webdriver.Chrome(r'C:\Users\19175\Desktop\sel\chromedriver.exe')

# Go to the page that we want to scrape
driver.get("https://www.zappos.com/product/review/7156453")

#total pages: (use regular expression to get number by itself)
find_total_items = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div[1]/div/div/div[1]/div[1]/span').text
total_items = int(re.findall('\d+',find_total_items)[0])


find_total_pages = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div[2]/div[2]/div/span/a[4]').text
total_pages = int(re.findall('\d+',find_total_items)[0])
#total_pages=1

#open csv file
csv_file = open('Salomon_XAPro3D_Reviews.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
#data layout: style, brand, model, Price, overallRating, heartLikes, TrueToSize, TrueToWidth, ArchSupport, NumberOfReviews

#currently static, need to make this dynamic and change to a while loop for when the last page is scraped
reviews_on_page = 25


#initialize an empty dicitonary
review_dict = {}

#loop through total pages (index_1)
for i in range(total_pages):
    #wait unitl last show loads, or 10 seconds, whichever comes first 

    time.sleep(3)
    
    #try:
    if i==0:
        dismiss_button = driver.find_element_by_xpath('//*[@id="root"]/div[1]/aside/div[3]/form/button[1]')
        dismiss_button.click()
    #except:
     #   continue
    # wait_review = WebDriverWait(driver, 10)
    # reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="searchPage"]/div[2]')))


    for j in range(reviews_on_page):

    #First get information for shoe(i): brand, model, Price, avgRating, heartLikes

    #driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div[2]/div[1]/div[2]/div[24]/div/div/div/div[4]/div/div').text
    #driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div[2]/div[1]/div[2]/div[25]/div/div/div/div[4]/div/div').text

        try:
            review = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div[2]/div[1]/div[2]/div[' + str(j+1) + ']/div/div/div/div[4]/div/div').text
            review_dict['review'] = review
            writer.writerow(review_dict.values())
        except:
            continue


    # click the next page
    next_page_button = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div[2]/div[2]/div/a[2]')
    next_page_button.click()


#print(e)
csv_file.close()
driver.close()
#break