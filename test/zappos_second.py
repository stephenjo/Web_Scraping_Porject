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
driver.get("https://www.zappos.com/men-running-shoes/CK_XARC81wEY0O4BwAEC4gIEAQIDGA.zso?s=recentSalesStyle%2Fdesc%2F&p=13")

#total pages: (use regular expression to get number by itself)
find_total_items = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/div[2]/div/span').text
total_items = int(re.findall('\d+',find_total_items)[0])
total_pages = math.ceil(total_items/100)-1


#open csv file
csv_file = open('reviews_zappos.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
#data layout: style, brand, model, Price, overallRating, heartLikes, TrueToSize, TrueToWidth, ArchSupport, NumberOfReviews

#currently static, need to make this dynamic and change to a while loop for when the last page is scraped
shoes_on_page = 100


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


    #loop through total shoes on page(i)
    for j in range(shoes_on_page):

    #First get information for shoe(i): brand, model, Price, avgRating, heartLikes


        brand = driver.find_element_by_xpath('//*[@id="searchPage"]/div[2]/article[' + str(j+1) + ']/div/p[1]').text
        model = driver.find_element_by_xpath('//*[@id="searchPage"]/div[2]/article[' + str(j+1) + ']/div/p[2]').text
        price = driver.find_element_by_xpath('//*[@id="searchPage"]/div[2]/article[' + str(j+1) + ']/div/p[3]/span[1]').text
        price_value = re.findall('\d+',price)[0]

        clicks = driver.find_element_by_xpath('//*[@id="searchPage"]/div[2]/article[' + str(j+1) + ']/div/button').text

        try:
            avg_rating = driver.find_element_by_xpath('//*[@id="searchPage"]/div[2]/article[' + str(j+1) + ']/div/p[4]').text
            avg_rating_value = re.findall('\d+',avg_rating)[0]
        except:
            avg_rating_value=0
            review_dict['style'] = 0
            review_dict['brand'] = brand
            review_dict['model'] = model
            review_dict['price'] = price_value
            review_dict['avg_rating'] = 0
            review_dict['heartLikes'] = clicks
            review_dict['true_to_size'] = 0
            review_dict['true_to_width'] = 0
            review_dict['arch_support'] = 0
            review_dict['number_of_reviews'] = 0

            #write current review dict data row to csv
            writer.writerow(review_dict.values())
            continue
        

        #Click on shoe(j) 
        shoe_detail_button = driver.find_element_by_xpath('//*[@id="searchPage"]/div[2]/article[' + str(j+1) + ']/a/div')
        shoe_detail_button.click()
        time.sleep(3)
        
        # wait_review = WebDriverWait(driver, 10)
        # reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="root"]')))


        #Second get information: style, TrueToSize, TrueToWidth, ArchSupport, NumberOfReviews
        style = driver.find_element_by_xpath('//*[@id="breadcrumbs"]/div[1]/a[3]').text

        number_of_reviews = driver.find_element_by_xpath('//*[@id="overview"]/span/div[2]/div/a/span/span[2]/span[1]').text

        try:
            t_to_size= driver.find_element_by_xpath('//*[@id="productRecap"]/div[3]/div/div[1]/div[2]/strong').text
            true_to_size_value = re.findall('\d+',t_to_size)[0]

            t_to_width= driver.find_element_by_xpath('//*[@id="productRecap"]/div[3]/div/div[2]/div[2]/strong').text
            true_to_width_value = re.findall('\d+',t_to_width)[0]

            arch_support= driver.find_element_by_xpath('//*[@id="productRecap"]/div[3]/div/div[3]/div[2]/strong').text
            arch_support_value = re.findall('\d+',arch_support)[0]

            review_dict['style'] = style
            review_dict['brand'] = brand
            review_dict['model'] = model
            review_dict['price'] = price_value
            review_dict['avg_rating'] = avg_rating_value
            review_dict['heartLikes'] = clicks
            review_dict['true_to_size'] = true_to_size_value
            review_dict['true_to_width'] = true_to_width_value
            review_dict['arch_support'] = arch_support_value
            review_dict['number_of_reviews'] = number_of_reviews

            #write current review dict data row to csv
            writer.writerow(review_dict.values())

            #click back button
            back_button = driver.find_element_by_xpath('//*[@id="breadcrumbs"]/div[1]/a[1]')
            back_button.click()
            time.sleep(3)
        except:
            review_dict['style'] = style
            review_dict['brand'] = brand
            review_dict['model'] = model
            review_dict['price'] = price_value
            review_dict['avg_rating'] = avg_rating_value
            review_dict['heartLikes'] = clicks
            review_dict['true_to_size'] = true_to_size_value
            review_dict['true_to_width'] = true_to_width_value
            review_dict['arch_support'] = arch_support_value
            review_dict['number_of_reviews'] = number_of_reviews

            #write current review dict data row to csv
            writer.writerow(review_dict.values())

            #click back button
            back_button = driver.find_element_by_xpath('//*[@id="breadcrumbs"]/div[1]/a[1]')
            back_button.click()
            time.sleep(3)
            continue

        #data layout: style, brand, model, Price, avgRating, heartLikes, TrueToSize, TrueToWidth, ArchSupport, NumberOfReviews




    # click the next page
    next_page_button = driver.find_element_by_xpath('//*[@id="searchPagination"]/div[3]/a[2]')
    next_page_button.click()


#print(e)
csv_file.close()
driver.close()
#break