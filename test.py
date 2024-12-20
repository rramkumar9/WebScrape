from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def saveText(file, para):
    with open(file, 'w', encoding='utf-8') as f:
        for type, p in para:
            print(p)
            if type == 'Title' or type == 'Note':
                f.write(f"\n---------------------------\n")
                f.write(f"{type}: {p.strip()}\n")
                f.write("\n")  # Add extra newline for separation
            else:
                f.write(f"{type}: {p.strip()}\n")
                f.write("\n") 


def extractType(soup):
    grouped = []

    exclude = {
        "Home", "Products", "Community", "Resources", "Get Support", "More",
        "All", "Documentation", "Articles", "Videos", "Contents",
        "Collapse All", "Expand All", "New and Enhanced Features",
        "Announcements", "Fixed", "API", "Integrations",
        "Docusign eSignature for Outlook﻿", "Revision History", ""
    }




    for element in soup.find_all(['h2', 'div', 'p', 'ph', 'li', 'span']):
        text = element.get_text(strip=True)
        if text in exclude:
            continue


        if element.name == 'h2' or (element.name == 'div' and 'title' in (element.get('class') or [])):
            text = element.get_text(strip=True)
            grouped.append(('Title', text))

        elif element.name in ['p', 'ph']:
            text = element.get_text(strip=True)
            grouped.append(('Paragraph', text))

        elif element.name == 'li':
            text = element.get_text(strip=True)
            grouped.append(('Bullet', text))

        
        elif 'note' in (element.get('class') or []):
            text = element.get_text(strip=True)
            if text:
                grouped.append(('Note', text))
            
    return grouped


def getMostRecentLink(driver):

    ret = None
    name = ""
    driver.get('https://support.docusign.com/s/releasenotes?language=en_US&labelKey=Release_Note&page=1')

    try:
        target_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'row_item-title'))
        )
        
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        target_div = soup.find('div', class_='row_item-title')
        if target_div:
            link = target_div.find('a')
            
            if link and link.has_attr('href'):
                name = link.get_text(strip=True)
                href_value = link['href']
                print("Href found:", href_value)
                ret = href_value




        else:
            print("Target div not found!")

    except Exception as e:
        print(f"An error occurred: {e}")
    return ret, name


driver = webdriver.Chrome()
link, name = getMostRecentLink(driver)
name = name.replace(" ", "")

if link:

    driver.get(link)

    
    try:
        target_div = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'BundleContentComponent'))
        )
        time.sleep(10)
        
        html = driver.page_source


        soup = BeautifulSoup(html, 'html.parser')
        grouped = extractType(soup)
        print(grouped)
        saveText(f'{name}.txt', grouped)

        print("Finished")


    except Exception as e:
        print(f"An error occurred: {e}")


driver.quit()

