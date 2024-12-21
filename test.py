from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re



def saveText(file, para):
    with open(file, 'w', encoding='utf-8') as f:
        for type, p in para:
            p_up = p.replace("\t", "").replace("\n", "")
            p_ups = re.sub(r"\s+", " ", p_up).strip()
            if type == 'Title' or type == 'Note':
                f.write(f"\n---------------------------\n")
                f.write(f"{type}: {p_ups.strip()}\n")
                
            else:
                f.write(f"{type}: {p_ups.strip()}\n")



def extractType(soup):
    grouped = []

    exclude = {
        "Home", "Products", "Community", "Resources", "Get Support", "More",
        "All", "Documentation", "Articles", "Videos", "Contents",
        "Collapse All", "Expand All", "New and Enhanced Features",
        "Announcements", "Fixed", "API", "Integrations",
        "Docusign eSignature for Outlook﻿", "Revision History", "",
        "Admin Release Notes", "Prev", "Next", "Share this page",
        "Send us your feedback", "Thank you", "Your Privacy Choices",
        "These cookies are necessary for the website to function and cannot be switched off in our systems. They "+
        "are usually only set in response to actions made by you which amount to a request for services, such "+
        "as setting your privacy preferences, logging in or filling in forms.    You can set your browser to block "+
        "or alert you about these cookies, but some parts of the site will not then work. These cookies do not store "+
        "any personally identifiable information."
    }




    for element in soup.find_all(['h1', 'h2', 'div', 'p', 'ph', 'li', 'span', 'img', 'dd', 'dt']):
        
        if element.name != "img":
            text = element.get_text(strip=True)
            if text in exclude:
                continue

        if element.name in ['h1', 'h2'] or (element.name == 'div' and 'title' in (element.get('class') or [])):
            text = element.get_text(strip=True)
            grouped.append(('Title', text))

        elif element.name in ['p', 'ph']:
            text = element.get_text(strip=True)
            grouped.append(('Paragraph', text))

        elif element.name == 'li':
            text = element.get_text(strip=True)
            grouped.append(('Bullet', text))
        
        elif element.name == 'dd':
            text = element.get_text(strip=True)
            grouped.append(('Sub Title', text))
        
        elif element.name == 'dt':
            text = element.get_text(strip=True)
            grouped.append(('Sub Bullet', text))
        
        elif element.name == 'img' and 'image' in (element.get('class') or []):
            link = element.get('src', 'No link')
            title = element.get('alt', 'No title')
            text = f'{title} , Link: {link}'
            grouped.append(('Image', text))


        
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
name = name.replace(" ", "_")
name = name.replace(".", "_")
name = name.replace("/", "_")
name = name.replace(":", "_")
name = name.replace("?", "_")
name = name.replace("*", "_")
name = name.replace("<", "_")
name = name.replace(">", "_")
name = name.replace("|", "_")


if link:

    #driver.get(link)

    '''
    For Testing using this update
    https://support.docusign.com/s/document-item?language=en_US&bundleId=oqn1730308722576&topicId=kzc1730309303090.html&_LANG=enus
    '''

    driver.get('https://support.docusign.com/s/document-item?language=en_US&bundleId=oqn1730308722576&topicId=kzc1730309303090.html&_LANG=enus')

    
    try:
        target_div = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'BundleContentComponent'))
        )
        time.sleep(10)
        
        html = driver.page_source


        soup = BeautifulSoup(html, 'html.parser')
        #print(soup.prettify())
        grouped = extractType(soup)
        print(grouped)

        #saveText(f'{name}.txt', grouped)
        '''
        Also for testing
        '''
        saveText(f'Docusign_eSignature_24_4_00_00_Release_Notes__December_2024.txt', grouped)
        print("Finished")


    except Exception as e:
        print(f"An error occurred: {e}")


driver.quit()

