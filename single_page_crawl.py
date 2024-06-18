import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def extract_emails(text):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.findall(email_regex, text)

def extract_phone_numbers(text):
    phone_regex = r'(\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\b\d{3}[-.\s]??\d{4}\b)'
    return re.findall(phone_regex, text)

def extract_addresses(text):
    address_regex = r"([0-9]{1,5})(.{5,75})((?:Ala(?:(?:bam|sk)a)|American Samoa|Arizona|Arkansas|(?:^(?!Baja )California)|Colorado|Connecticut|Delaware|District of Columbia|Florida|Georgia|Guam|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Miss(?:(?:issipp|our)i)|Montana|Nebraska|Nevada|New (?:Hampshire|Jersey|Mexico|York)|North (?:(?:Carolin|Dakot)a)|Ohio|Oklahoma|Oregon|Pennsylvania|Puerto Rico|Rhode Island|South (?:(?:Carolin|Dakot)a)|Tennessee|Texas|Utah|Vermont|Virgin(?:ia| Island(s?))|Washington|West Virginia|Wisconsin|Wyoming|A[KLRSZ]|C[AOT]|D[CE]|FL|G[AU]|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])).{1,2}([0-9]{5})"
    addresses = re.findall(address_regex, text)
    
    formatted_addresses = []
    for address in addresses:
        out_address = " ".join(address)
        out_address = " ".join(out_address.split())
        formatted_addresses.append(out_address)
    
    return formatted_addresses

def crawl_contact_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the webpage: {url}. Error: {e}")
        return [], [], []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    
    emails = extract_emails(text)
    phones = extract_phone_numbers(text)
    
    addresses = extract_addresses(text)
    
    return emails, phones, addresses

def main():
    input_file = 'input_urls_list.csv'
    output_file = 'output_contact_info.csv'
    
    urls_df = pd.read_csv(input_file, header=None, names=['url'])
    results = []
    
    for index, row in urls_df.iterrows():
        url = row['url'].strip()
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        emails, phones, addresses = crawl_contact_info(url)
        results.append({
            'url': url,
            'emails': ', '.join(emails),
            'phones': phones,
            'addresses': ', '.join(addresses)
        })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Contact info saved to {output_file}")

if __name__ == '__main__':
    main()
