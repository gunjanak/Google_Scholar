from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pickle
import re
import pandas as pd


#This file contains functions to aid web scraping from google scholar

def get_id(html_content):
    try:
        data_aid_values = []
        print("Get the id")
        bs = BeautifulSoup(html_content,'html.parser')
        div_elements= bs.find_all('div', class_='gs_r')
        for i in range(len(div_elements)):
            try:
                data_aid_values.append(div_elements[i]['data-aid'])
            except Exception as e:  # Generic except block
                print(f"Error: {type(e).__name__} occurred!")
        return data_aid_values
    except Exception as e:
        print(e)


def get_title(html_content):

    try:
        bs = BeautifulSoup(html_content,'html.parser')
        mydivs = bs.find_all("h3")

        titles = []
        links = []
        for mydiv in mydivs:
            title = mydiv.get_text(strip=True)
            titles.append(title)
            link_element = mydiv.find("a")
            link = link_element['href']
            links.append(link)

        return titles,links
    except Exception as e:
        print(e)


def get_authors_publication(html_content):
    try:
        # Regular expression pattern to extract the year
        pattern = r'\d{4}\s*-'
        
        bs = BeautifulSoup(html_content,'html.parser')
        gs_a_tags = bs.find_all(class_="gs_a")

        all_text = []
        authors = []
        publications = []
        years = []
        for gs_a in gs_a_tags:
            gs_a_text = gs_a.get_text(strip=True)
            # print(gs_a_text)
            parts1 = gs_a_text.split("-", 1)
            author = parts1[0].strip().split(",")
            publication = parts1[1].strip()
            # print(publication)

            #Find year
            match = re.search(pattern,publication)
            if match:
                year = match.group()
                years.append(year[:-2])
            else:
                print("Year not found in the string.")

            #find publication
            publication = publication.split()[-1]

            # # all_text.append(gs_a_text)
            authors.append(author)
            publications.append(publication)
        

    
        return authors,publications,years
    except Exception as e:
        print(e)


def get_abstract(html_content):
    try:
        abstracts = []
        bs = BeautifulSoup(html_content,'html.parser')
        gs_rs_tags = bs.find_all(class_="gs_rs")
        for tag in gs_rs_tags:
            abstracts.append(tag.get_text(strip=True))

        return abstracts
    except Exception as e:
        print(e)

def get_citations_no(html_content):
    try:

        citations = []
        links_to_citations = []
        bs = BeautifulSoup(html_content,'html.parser')
        # Find all elements containing "Cited by" and "Related articles" text
        # cited_by = # Find all <a> tags with the specified form
        target_a_tags = bs.find_all("a", href=lambda href: href and href.startswith("/scholar?cites="))
        for tag in target_a_tags:
            links_to_citations.append(tag['href'])
            citations.append(tag.get_text(strip=True))

        # Extract numbers using regular expressions and convert to integers
        citations = [int(re.search(r'\d+', string).group()) for string in citations]

        
        return citations,links_to_citations
    except Exception as e:
        print(e)