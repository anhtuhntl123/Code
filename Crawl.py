import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_journal_info(journal_url):
    response = requests.get(journal_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    journal_name =  soup.find("h1").getText()

    # impact_factor_craw = soup.find("section","app-journal-metrics")     
    impact_factor_craw = soup.find("dd",{"data-test":"impact-factor-value"})

    impact_factor = impact_factor_craw.getText() if impact_factor_craw else ""


    section_issn = soup.find("div",{"class":"u-display-flex-at-sm"})
    e_issn = ""
    issn = ""
    if section_issn:
        label = section_issn.find_all('dt')
        value = section_issn.find_all('dd')
        
        for i,j in zip(label,value):
          if i.text == 'Electronic ISSN':
            e_issn = j.text
          elif i.text == 'Print ISSN':
            issn = j.text

        j_son = {
            'Journal Name': journal_name,
            'Impact Factor (2 years)': impact_factor,
            'ISSN': issn,
            'E-ISSN': e_issn
        }
        print(j_son)
        return j_son

base_url = "https://link.springer.com/journals/"
characters = "abcdefghijklmnopqrstuvwz0"

journal_data = []

for char in characters:
    journal_list_url = base_url + char
    page_number = 1
    while True:
        url = f"{journal_list_url}/{page_number}"
        response = requests.get(f"{journal_list_url}/{page_number}")
        soup = BeautifulSoup(response.content, 'html.parser')
        journal_links = soup.find_all(class_='c-atoz-list__link')
        journal_urls = [link.get('href') for link in journal_links] 
        if len(journal_urls) == 0:
            continue
        for journal_url in journal_urls:
            journal_info = extract_journal_info(journal_url)
            if journal_info:
              journal_data.append(journal_info)
        next_page = soup.find("a", {"class" : "c-pagination-listed__link c-pagination-listed__next"})
        if next_page is not None:
          page_number += 1
        else:
          break

df = pd.DataFrame(journal_data)
df.to_excel('springer1.xlsx')