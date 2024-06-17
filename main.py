import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Define functions to extract emails, phone numbers, and addresses using regex
def extract_emails(text):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.findall(email_regex, text)

def extract_phone_numbers(text):
    phone_regex = r'(\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\b\d{3}[-.\s]??\d{4}\b)'
    return re.findall(phone_regex, text)

def extract_addresses(text):
    # A simple regex for finding addresses, this can be improved
    address_regex = r'\d{1,5}\s\w+\s\w+.*'
    return re.findall(address_regex, text)

# Read the product URLs from CSV
products_df = pd.read_csv('input_urls_list.csv')
product_urls = products_df['URLs'].tolist()

# Set up Selenium WebDriver with Chrome
options = Options()
options.headless = True  # Run headless Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# List to store the extracted data
data = []

# Iterate over each URL
for url in product_urls:
    driver.get(url)
    
    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    # Extract page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Combine all text from the page
    page_text = soup.get_text(separator=' ')
    
    # Extract contact details
    emails = extract_emails(page_text)
    phone_numbers = extract_phone_numbers(page_text)
    addresses = extract_addresses(page_text)
    
    # Use only unique values
    emails = ', '.join(set(emails)) if emails else "Not found"
    phone_numbers = ', '.join(set(phone_numbers)) if phone_numbers else "Not found"
    addresses = ', '.join(set(addresses)) if addresses else "Not found"
    
    print("Data", emails, phone_numbers, addresses)
    # Append extracted data to the list
    data.append([url, emails, phone_numbers, addresses])

# Close the WebDriver
driver.quit()

# Create a DataFrame from the data
output_df = pd.DataFrame(data, columns=['URL', 'Email', 'Phone Number', 'Address'])

# Save the DataFrame to a CSV file
output_df.to_csv('output_contact_info.csv', index=False)

print("Scraping completed and data saved to 'output_contact_info.csv'.")
