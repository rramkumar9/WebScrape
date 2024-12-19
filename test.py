from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup



def getMostRecentLink(driver):

    ret = None
    driver.get('https://support.docusign.com/s/releasenotes?language=en_US&labelKey=Release_Note&page=1')

    try:
        target_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'row_item-title'))
        )
        
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        target_div = soup.find('div', class_='row_item-title')
        if target_div:
            #print("Target div found!")
            #print(target_div)
            link = target_div.find('a')
            
            if link and link.has_attr('href'):
                href_value = link['href']
                print("Href found:", href_value)
                ret = href_value




        else:
            print("Target div not found!")

    except Exception as e:
        print(f"An error occurred: {e}")
    return ret


driver = webdriver.Chrome()
link = getMostRecentLink(driver)

if link:

    driver.get(link)

    """
    Need to flix where the bs is checking. Update content is contaited within 
    BundleContentComponent Class but is under other sub classes (maybe why bs is
    unable to see). Could also be to not enough time waiting
    """
    
    try:
        target_div = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'BundleContentComponent'))
        )
        
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        target_div = soup.find('div', class_='BundleContentComponent')
        print(target_div.prettify())
        if target_div:
            paragraphs = target_div.find_all(['p', 'ph'])
            for para in paragraphs:
                print("\nParagraph text:", para.get_text(strip=True))



        else:
            print("Target div not found!")

    except Exception as e:
        print(f"An error occurred: {e}")
    

else:
    print("error")

driver.quit()

