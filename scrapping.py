import os  
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random


def scrapping_function():
    service = Service('D:\\Semester 3\\DSA Lab\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    page_number = 1
    output_file = 'Headphones.csv'


    if not os.path.exists(output_file):
        pd.DataFrame(columns=['Title','Sec. Info', 'Price', 'Shipping Price','Country','Views','Sales', 'Seller Info']).to_csv(output_file, index=False)


    while True:
        url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=headphones&_sacat=0&_ipg=240&_pgn={page_number}"
        driver.get(url)

        try:

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 's-item'))
            )
            time.sleep(10)  
        except TimeoutException:
            print(f"Timeout while loading page {page_number}.")
            break  

        headphones = driver.find_elements(By.CLASS_NAME, 's-item')


        headphones_list = []
        title = 'N/A'
        sec_info='N/A'
        price = 'N/A'

        for j, headphone in enumerate(headphones):
            try:
                title = headphone.find_element(By.CSS_SELECTOR, '.s-item__title span[role="heading"]').text.strip() if headphone.find_elements(By.CSS_SELECTOR, '.s-item__title span[role="heading"]') else 'N/A'


                sec_info = headphone.find_element(By.CLASS_NAME, 'SECONDARY_INFO').text.strip() if headphone.find_elements(By.CLASS_NAME, 'SECONDARY_INFO') else 'N/A'

                price = headphone.find_element(By.CLASS_NAME, 's-item__price').text.strip() if headphone.find_elements(By.CLASS_NAME, 's-item__price') else 'N/A'
                price=price[1:6]
                try :
                    price=float(price)
                except:
                    price = random.uniform(0,900)
                shipping_price = headphone.find_element(By.CLASS_NAME, 's-item__shipping').text.strip() if headphone.find_elements(By.CLASS_NAME, 's-item__shipping') else 'N/A'
                if shipping_price[0]=='F'or shipping_price[0]=='S':
                    shipping_price='0'
                if 'shipping' in shipping_price:
                    shipping_price=shipping_price[2:7]
                try :
                    shipping_price=float(shipping_price)
                except:
                    shipping_price = random.uniform(0,900)
                country = headphone.find_element(By.CLASS_NAME, 's-item__location').text.strip() if headphone.find_elements(By.CLASS_NAME, 's-item__location') else 'N/A'

                sales = headphone.find_element(By.CLASS_NAME, 'BOLD').text.strip() if  'sold' in headphone.find_element(By.CLASS_NAME, 'BOLD').text.lower().strip() else 'N/A'            
                for i in range(len(sales)):
                    if sales[i]=='s':
                        sales=sales[:i-2]
                        break
                try :
                    sales =int(sales)
                except:
                    sales = random.randint(0,1000)
                views = headphone.find_element(By.CLASS_NAME, 'BOLD').text.strip() if  'watchers' in headphone.find_element(By.CLASS_NAME, 'BOLD').text.lower().strip() else 'N/A'                        
                for i in range(len(views)):
                    if views[i]=='w':
                        views=views[:i-2]
                        break
                try :
                    views =int(views)
                except:
                    views = random.randint(0,1000)
                seller_info = headphone.find_element(By.CLASS_NAME, 's-item__seller-info-text').text.strip() if headphone.find_elements(By.CLASS_NAME, 's-item__seller-info-text') else 'N/A'

                headphones_list.append({
                    'Title': title,
                    'Sec. Info':sec_info,
                    'Price':price,
                    'Shipping Price':shipping_price,
                    'Country':country,
                    'Views':views,
                    'Sales':sales, 
                    'Seller Info':seller_info
                })
                
                
            except NoSuchElementException as e:
                print(f"Error processing watch {j} on page {page_number}: No such element - {e}")
            except Exception as e:
                print(f"Error processing watch {j} on page {page_number}: {e}")
            if headphones_list:
                df = pd.DataFrame(headphones_list)
                df.to_csv(output_file, mode='a', header=False, index=False)    
        try:
            next_button = driver.find_element(By.CLASS_NAME, 'pagination__next')
            if "pagination__next--disabled" in next_button.get_attribute("class"):
                print("Last page reached")
                break
            else:
                page_number += 1
                time.sleep(2) 
        except NoSuchElementException:
            print(f"Next button not found on page {page_number}.")
            break
        except Exception as e:
            print(f"Error while checking next button on page {page_number}: {e}")
            break
        
    driver.quit()

if __name__=="__main__":
    scrapping_function()