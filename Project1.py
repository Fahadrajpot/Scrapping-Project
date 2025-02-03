import os 
import sys
import csv
import time
import random
import pandas as pd
from Algorithms import *

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox,QDialog
 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Worker(QThread):
    
    finished = pyqtSignal(str)
    progress=pyqtSignal(list)
    def __init__(self, scrap_function):
        super().__init__()
        self.scrap_function = scrap_function 
        self.IsPaused=False
        self.IsRunning=False
    def run(self):
        self.scrap_function() 
        self.finished.emit("Task Completed!")
        
    def pause(self):
        self.IsPaused = True
    def stop(self):
        self.IsRunning = False
    def resume(self):
        self.IsPaused=False
        
class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow,self).__init__()
        loadUi("Project1.ui",self)
        self.setWindowTitle('Project 1')
        self.search_bar_1.setPlaceholderText('Search in Title')
        self.search_bar_2.setPlaceholderText('Search in Sec. Info')
        self.search_bar_3.setPlaceholderText('Search in Price')
        self.search_bar_4.setPlaceholderText('Search in Shipping Price')
        self.search_bar_5.setPlaceholderText('Search in Country')
        self.search_bar_6.setPlaceholderText('Search in Views')
        self.search_bar_7.setPlaceholderText('Search in Sales')
        self.search_bar_8.setPlaceholderText('Search in Seller Info')
        self.load_table()
        self.selected_numbers = []
        self.search_field = []
        self.row_count=0
        self.load_from_csv_button.clicked.connect(self.load_table_from_csv)
        self.clear_table_button.clicked.connect(self.clear_table)
        self.sort_button.clicked.connect(self.sort)
        self.columns_selection_button.clicked.connect(self.multi_columns_selection)
        self.search_field_function()
        self.search_button.clicked.connect(self.search)
        self.scrap_data_button.clicked.connect(self.start_scrapping)
        self.pause_button.clicked.connect(self.pause_scrapping)
        self.resume_button.clicked.connect(self.resume_scrapping)
        self.stop_button.clicked.connect(self.stop_scrapping)
        self.worker = None
        
    def clear_table(self):
        self.runtime_label.setText("Run Time: "+str(0.0))
        self.table.clearContents()
        self.table.setRowCount(0)
        list=[]
        self.increase_progress(list)
    def load_table(self):
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['Title','Sec. Info','Price','Shipping Price','Country','Views','Sales','Seller Info'])
         
    def load_table_from_csv(self):
        
        df=raed_from_csv('Headphones.csv')
        
        rows=df.to_numpy()
        list=[]
        for row in rows:
            list.append(row)
        lists=[]
        for number in list:
            lists.append(number)
        self.table.setRowCount(len(list))
        roww=0
        for row in list:
            row[0]=str(row[0])
            row[1]=str(row[1])
            row[2]=str(row[2])
            row[3]=str(row[3])
            row[4]=str(row[4])
            row[5]=str(row[5])
            row[6]=str(row[6])
            row[7]=str(row[7])
            self.table.setItem(roww, 0 , QtWidgets.QTableWidgetItem((row[0])))
            self.table.setItem(roww, 1 , QtWidgets.QTableWidgetItem((row[1])))
            self.table.setItem(roww, 2 , QtWidgets.QTableWidgetItem((row[2])))
            self.table.setItem(roww, 3 , QtWidgets.QTableWidgetItem((row[3])))
            self.table.setItem(roww, 4 , QtWidgets.QTableWidgetItem((row[4])))
            self.table.setItem(roww, 5 , QtWidgets.QTableWidgetItem((row[5])))
            self.table.setItem(roww, 6 , QtWidgets.QTableWidgetItem((row[6])))
            self.table.setItem(roww, 7 , QtWidgets.QTableWidgetItem((row[7])))
            roww +=1
        return lists 
    def TextFromCombobox(self):
        selected_option = self.combobox_for_algos.currentText()
        return selected_option
    def sort(self):
        flag =True
        if self.selected_numbers:
            Text=self.TextFromCombobox()
            list=self.data_from_table()
            for row in list:
                row[2]=float(row[2])
                row[3]=float(row[3])
                row[5]=int(row[5])
                row[6]=int(row[6])
            start_time=time.time()
            if len(list)>0:
                if Text=="Bubble Sort":
                    bubble_sort(list, self.selected_numbers)
                elif Text=="Selection Sort":
                    selection_sort(list, self.selected_numbers)
                elif Text=="Insertion Sort":
                    insertion_sort(list, self.selected_numbers)
                elif Text=="Merge Sort":
                    merge_sort(list, self.selected_numbers)
                elif Text=="Quick Sort":
                    list=quick_sort(list, self.selected_numbers)
                elif Text =="Counting Sort":
                    if 0  in self.selected_numbers or 1 in self.selected_numbers or 2 in self.selected_numbers or 3 in self.selected_numbers or 4 in self.selected_numbers or 7 in self.selected_numbers:
                        flag=False
                        self.ShowMessageBox("Wrong Column Selected.", "Infromation")
                        self.selected_numbers=[]
                    else:
                        list=counting_sort(list,self.selected_numbers)
                elif Text =="Radix Sort":
                    if 0  in self.selected_numbers or 1 in self.selected_numbers or 2 in self.selected_numbers or 3 in self.selected_numbers or 4 in self.selected_numbers or 7 in self.selected_numbers:
                        flag=False
                        self.ShowMessageBox("Wrong Column Selected.", "Infromation")
                        self.selected_numbers=[]
                    else:
                        list=radix_sort(list,self.selected_numbers)
                elif Text =="Bucket Sort":
                    list=bucket_sort(list,self.selected_numbers)
                elif Text =="Bead Sort":
                    if 0  in self.selected_numbers or 1 in self.selected_numbers or 2 in self.selected_numbers or 3 in self.selected_numbers or 4 in self.selected_numbers or 7 in self.selected_numbers:
                        flag=False
                        self.ShowMessageBox("Wrong Column Selected.", "Infromation")
                        self.selected_numbers=[]
                    else:
                        list=bead_sort(list,self.selected_numbers)
                elif Text =="Pancake Sort":
                    if 0  in self.selected_numbers or 1 in self.selected_numbers  or 4 in self.selected_numbers or 7 in self.selected_numbers:
                        flag=False
                        self.ShowMessageBox("Wrong Column Selected.", "Infromation")
                        self.selected_numbers=[]
                    else:
                        list=pancake_sort(list,self.selected_numbers)
                end_time=time.time()
                if list:
                    
                    self.update_table(list)
                run_time=((end_time-start_time)*1000)
                if flag  :
                    self.runtime_label.setText("Run Time: "+str(run_time))
                    flag=True
                self.selected_numbers=[]
            else:
                self.ShowMessageBox("Data Empty.", "Infromation")
        else:
            self.ShowMessageBox("Select the columns.","Information")
    def update_table(self, List):
        self.table.clearContents
        self.table.setRowCount(0)
        self.table.setRowCount(len(List))
        roww=0
        for row in List:
            
            row[0]=str(row[0])
            row[1]=str(row[1])
            row[2]=str(row[2])
            row[3]=str(row[3])
            row[4]=str(row[4])
            row[5]=str(row[5])
            row[6]=str(row[6])
            row[7]=str(row[7])
            self.table.setItem(roww, 0 , QtWidgets.QTableWidgetItem((row[0])))
            self.table.setItem(roww, 1 , QtWidgets.QTableWidgetItem((row[1])))
            self.table.setItem(roww, 2 , QtWidgets.QTableWidgetItem((row[2])))
            self.table.setItem(roww, 3 , QtWidgets.QTableWidgetItem((row[3])))
            self.table.setItem(roww, 4 , QtWidgets.QTableWidgetItem((row[4])))
            self.table.setItem(roww, 5 , QtWidgets.QTableWidgetItem((row[5])))
            self.table.setItem(roww, 6 , QtWidgets.QTableWidgetItem((row[6])))
            self.table.setItem(roww, 7 , QtWidgets.QTableWidgetItem((row[7])))
            roww +=1
    def data_from_table(self):
        
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()
        data = []
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.table.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')  
            data.append(row_data)
        return data
    
    def multi_columns_selection(self):
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Columns")
        

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget(dialog)
        list_widget.setSelectionMode(QListWidget.MultiSelection)

    
        list_widget.addItem(QListWidgetItem("Title"))
        list_widget.addItem(QListWidgetItem("Sec. Info"))
        list_widget.addItem(QListWidgetItem("Price"))
        list_widget.addItem(QListWidgetItem("Shipping Price"))
        list_widget.addItem(QListWidgetItem("Country"))
        list_widget.addItem(QListWidgetItem("Views"))
        list_widget.addItem(QListWidgetItem("Sales"))
        list_widget.addItem(QListWidgetItem("Seller Info"))
        layout.addWidget(list_widget)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            selected_items = list_widget.selectedItems()
            self.selected_numbers = [list_widget.row(item) for item in selected_items]     
         
    def ShowMessageBox(self, Message, Title):
     
       msg_box = QMessageBox()
      
       msg_box.setWindowTitle(Title)
       msg_box.setText(Message)
       msg_box.setIcon(QMessageBox.Information) 
       msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
       response = msg_box.exec_()
       
    def searching(self):
       
        
        list=[]
        list.append(self.search_bar_1.text())
        list.append(self.search_bar_2.text())
        list.append(self.search_bar_3.text())
        list.append(self.search_bar_4.text())
        list.append(self.search_bar_5.text())
        list.append(self.search_bar_6.text())
        list.append(self.search_bar_7.text())
        list.append(self.search_bar_8.text())
    
    def search_field_function(self):
        
        self.search_field.append(self.search_bar_1)
        self.search_field.append(self.search_bar_2)
        self.search_field.append(self.search_bar_3)
        self.search_field.append(self.search_bar_4)
        self.search_field.append(self.search_bar_5)
        self.search_field.append(self.search_bar_6)
        self.search_field.append(self.search_bar_7)
        self.search_field.append(self.search_bar_8)
        
    def search(self):
        search_type = self.combobox_for_searching.currentText().strip()

        condition_type = self.combobox_for_searching_condition.currentText().strip()  
        search_values = [field.text().strip().lower() for field in self.search_field]

        for row in range(self.table.rowCount()):
            if condition_type == 'AND':
                show_row = True 
            elif condition_type == 'OR':
                show_row = False 
            elif condition_type == 'NOT':
                show_row = True  
                
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                search_value = search_values[col]

                if item is not None:
                    item_text = item.text().lower()

                    if search_type == 'Equal to':  
                        condition_met = search_value and item_text == search_value
                    elif search_type == 'Contains':
                        condition_met = search_value and search_value in item_text
                    elif search_type == 'Starts with':
                        condition_met = search_value and item_text.startswith(search_value)
                    elif search_type == 'Ends with':
                        condition_met = search_value and item_text.endswith(search_value)

                    if condition_type == 'AND':
                        if search_value and not condition_met:
                            show_row = False
                            break 
                    elif condition_type == 'OR':
                        if search_value and condition_met:
                            show_row = True
                            break 
                    elif condition_type == 'NOT':
                       
                        if search_value and condition_met:
                            show_row = False
                            break 
                else:
                    if search_value:
                        if condition_type == 'AND':
                            show_row = False
                            break
                        elif condition_type == 'NOT':
                            continue  
            self.table.setRowHidden(row, not show_row)
    def scrap_into_table(self,row_data):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        for column, data in enumerate(row_data):
            self.table.setItem(row_position, column, QTableWidgetItem(str(data)))


    def start_scrapping(self):
        self.worker = Worker(self.scrapping_function)
        self.worker.IsRunning=True
        if self.worker.IsRunning==True:
            self.worker.start()
            
    def pause_scrapping(self):
        if self.worker:
            self.worker.pause()
            
    def resume_scrapping(self):
        if self.worker:
            self.worker.resume()
            
    def stop_scrapping(self):
        if self.worker:
            self.worker.stop()
            
    def increase_progress(self, value):
        completed_tasks = len(value)  
        total_tasks = 25000 

        if total_tasks > 0:
            percentage = (completed_tasks / total_tasks) * 100  
        if percentage < 100: 
            self.progress_bar.setValue(percentage)
        elif percentage == 100:
            self.progress_bar.setValue(percentage)
            self.stop_scrapping()
            
    def scrapping_function(self):
        self.clear_table()
        service = Service('D:\\Semester 3\\DSA Lab\\chromedriver-win64\\chromedriver.exe')
        driver = webdriver.Chrome(service=service)
        page_number = 1
        output_file = 'Headphones.csv'
        
        

        if not os.path.exists(output_file):
            pd.DataFrame(columns=['Title','Sec. Info', 'Price', 'Shipping Price','Country','Views','Sales', 'Seller Info']).to_csv(output_file, index=False)
        headphones_list=[]

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
                    
                    
                    self.worker.progress.emit(headphones_list)
                    self.increase_progress(headphones_list)
                    
                    while self.worker.IsPaused:
                        time.sleep(0.1)
                    if not self.worker.IsRunning:
                        driver.quit()
                    self.scrap_into_table([title, sec_info, price, shipping_price, country, views, sales, seller_info])

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
        
app = QApplication(sys.argv)
window = Mainwindow()
window.show()
sys.exit(app.exec_())