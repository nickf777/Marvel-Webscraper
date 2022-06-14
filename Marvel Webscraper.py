#!/usr/bin/env python
# coding: utf-8

# # Project Plan

# - Write a web scraper that scrapes title, description, metrics etc. on a list of marvel superheroes from Wikipedia
# - Uses PyMYSQL to write to a database 
# 	- Several tables 
# - Data Cleaning with Python and SQL
# - Calculated fields with Python SQL
# 
# Eventually:
# 
# - Data Modeling in either PowerBI or SQL itself
# - Visualization that looks very professional and fun
# 

# # Importing Libraries

# In[1]:


import pandas as pd
import numpy as np
import re
import requests
from bs4 import BeautifulSoup
import csv
import pymysql
import re

pd.set_option("display.max_rows", None)


# # Table 1: Character Scraper

# In[2]:


# https://en.wikipedia.org/wiki/Characters_of_the_Marvel_Cinematic_Universe

'''class Character(self, name, designation, description, link):
    self.name = name
    self.designation = designation
    self.description = description
    self.link = link
'''
def get_major_characters():
    html = requests.get('https://en.wikipedia.org/wiki/Characters_of_the_Marvel_Cinematic_Universe')
    bs = BeautifulSoup(html.text, 'lxml')
    
    #Character Names
    try:
        names = bs.find_all('h3')
        names = [names[i].getText().rstrip('[edit]') for i in range(len(names)-2) if not names[i].getText().startswith('Introduced')]
    except:
        print('There was an error pulling character names.')
    
    #Character Descriptions
    descriptions = []
    try:
        for heading in bs.find_all('h3'):
            description = heading.findNext('p')
            if not description.getText().startswith('The depiction of adapted and original characters in the MCU'):
                descriptions.append(description.getText())
    except:
        print('There was an error in pulling descriptions.')
    
    #Movie Appearances
    appearances = []
    try: 
        for heading in bs.find_all('h3'):
            appearance = heading.find_previous_sibling('p')
            if not appearance.getText().startswith('The following is a supplementary list of characters that appear in lesser roles') and not appearance.getText().startswith('Phase Four'):
                appearances.append(appearance.getText())
    except:
        print('There was an error in pulling appearances.')
        
    try:
        last_appearance = bs.find('span',id = 'Minor_characters').parent.find_previous_sibling('p').getText()
        appearances.append(last_appearance)
    except:
        print('Could not pull final appearance.')
        
    #Designation (find the previous h2)
    designations = []
    try:
        ref_name = bs.find_all('h3')
        for item in ref_name:
            if not item.getText().startswith('Introduced') and not item.getText() == 'Search':
                designation = item.find_previous_sibling('h2').getText()
                designations.append(designation)
    except:
        print('There was an error in pulling designations.')
                
    return names, designations, descriptions, appearances


# In[3]:


names, designations, descriptions, appearances = get_major_characters()


# In[4]:


print(f'There are {len(names)} in names')
print(f'There are {len(descriptions)} in descriptions')
print(f'There are {len(appearances)} in appearances')
print(f'There are {len(designations)} in designations')


# In[5]:


character_data = list(zip(names, designations, descriptions, appearances))


# In[6]:


character_df = pd.DataFrame(character_data, columns = ['Name','Designation','Description','Appearances'])


# In[7]:


character_data_dict = dict((z[0],list(z[1:])) for z in zip(names, designations,descriptions, appearances))


# # Write To Characters Table

# In[8]:


'''conn = pymysql.connect(host = '****',user = 'root', passwd = '*****', db = 'mysql', 
                       charset = 'utf8')
cur = conn.cursor()
cur.execute('USE marvel_database')

def store_characters(name, designation, description, appearance):
    cur.execute('INSERT INTO characters (char_name,char_type,char_desc,appearances) VALUES ''("%s","%s","%s","%s")',
                (name, designation, description, appearance))
    cur.connection.commit()
try:
    for key, value in character_data_dict.items():
        store_characters(key,value[0],value[1],value[2])
finally:
    cur.close()
    conn.close()
'''


# Fields I might want to add to this table:
# - Number of Appearances (calculation off of appearances column)
# - Country
# - Debut Year
# 
# I also might want to go back and scrape minor characters as well. 

# # Scraping Character Details

# In[9]:


# Grab the link from the characters table for each actor
# Grab the portrayed by: information
# Grab the actor link from those
# Take the relevant details from that page


# In[10]:


def get_links():
    html = requests.get('https://en.wikipedia.org/wiki/Characters_of_the_Marvel_Cinematic_Universe')
    bs = BeautifulSoup(html.text, 'lxml')
    
    # No links available for Darcy Lewis and Katy
    links = []
    try:
        div = bs.find_all('div', {'role':'note'})
        for item in div:
            link = item.findNext('a')['href']
            if link == '/wiki/Marvel_Cinematic_Universe:_Phase_One':
                break
            else:
                links.append(link)
    except:
        print('There was an error retrieiving links.')
    
    links = links[1:]
    return links


# In[11]:


links = get_links()


# In[12]:


def get_character(link_list):
    
    '''
    Errors occur when the link redirects to a list of characters rather than the main character page
    '''
    master_list = []
    for item in link_list:
        html = requests.get(f'https://en.wikipedia.org{item}')
        bs = BeautifulSoup(html.text,'lxml')
        
        try:
             #Get category headers
            portrayed = bs.find('table', {'class':'infobox'})
            categories = portrayed.find_all('th',{'class':'infobox-label'})
            category_list = [i.getText() for i in categories]

            #Get category data
            data = portrayed.find_all('td',{'class':'infobox-data'})
            data_list = [i.getText() for i in data]

            #Get name
            char_name = portrayed.find('th').getText()
            label = 'char_name'

            category_list.append(label)                
            data_list.append(char_name)

        except:
            print(f'There was an error in retrieving the character information for: {item}.')

        data_dict = dict(zip(category_list,data_list))
        master_list.append(data_dict)
            
    return master_list


# In[13]:


character_info = get_character(links)


# In[14]:


cleaned_entries = []
for item in character_info:
    new_dict = {f"{key.lower().replace(' ','_').replace('(s)','')}": val for key, val in item.items()}
    cleaned_entries.append(new_dict)


# In[16]:


'''conn = pymysql.connect(host = '127.0.0.1',user = 'root', passwd = 'Ipgatt77', db = 'mysql', 
                       charset = 'utf8')
cur = conn.cursor()
cur.execute('USE marvel_database')

def store_data(char_list):
    for item in char_list:
        columns = ', '.join(item.keys())
        values = list(item.values())
        values = [i.replace('"',"") for i in values]
        values = ', '.join(['"'+str(i)+'"' for i in values])
        cur.execute(f'INSERT INTO character_details ({columns}) VALUES ({values});')
        cur.connection.commit()

try:
    store_data(cleaned_entries)
finally:
    cur.close()
    conn.close()
'''


# ## Clean Character Details

# In[17]:


char_details = pd.read_csv('C:/Users/Nickf/OneDrive/Documents/Data Analysis/Portfolio Project 6 - Marvel Webscraper/char_details.csv')


# In[18]:


#Find the percentage of missing values by column
char_details_preprocessed = char_details.copy()

missing_values = char_details.isna().mean()*100
columns_to_drop = missing_values[missing_values > missing_values.mean()].index

char_details_preprocessed = char_details_preprocessed.drop(columns_to_drop, axis = 1)
char_details_preprocessed = char_details_preprocessed.dropna(axis = 0,subset = ['char_name'])

char_details_preprocessed = char_details_preprocessed.reset_index().drop('index', axis = 1)

char_details_preprocessed


# In[19]:


char_details_preprocessed = char_details_preprocessed.fillna('N/A')
based_on_split = char_details_preprocessed['based_on'].str.split('by ', expand = True)
based_on = based_on_split[0]
# To remove unicode spaces and newlines
based_1 = based_on_split[1].str.normalize('NFKD').replace(r'\n',' ', regex = True)
based_2 = based_on_split[2].str.normalize('NFKD').replace(r'\n',' ', regex = True)
based_3 = based_on_split[3].str.normalize('NFKD').replace(r'\n',' ', regex = True)

# For simplicity we are just going to keep based (source material) and based_1 (author)

char_details_preprocessed['based_on_source'] = based_on
char_details_preprocessed['based_on_author'] = based_1
char_details_preprocessed = char_details_preprocessed.fillna('N/A')
char_details_preprocessed = char_details_preprocessed.drop(['based_on'], axis = 1)


# In[20]:


# There are quite a few newline characters 
# On first examination, they look like they should all be replaced with a comma or semi-colon with the exception of the first occurence
char_details_preprocessed = char_details_preprocessed.replace(r'\n',', ',regex = True)
df_obj = char_details_preprocessed.select_dtypes(['object'])

char_details_preprocessed[df_obj.columns] = df_obj.apply(lambda x: x.str.lstrip(', ').str.rstrip(', '))


# In[21]:


# To fix spacing issues
def separate_values(value):
    for i in range(0,len(value)):
        try:
            for i in range(0,len(value)):
                if value[i].islower() and value[i+1].isupper():
                    value = value[:i+1] + ', ' + value[i+1:]
                else:
                    pass
        except:
            continue
    return value


# In[44]:


columns_to_fix = ['based_on_author','adapted_by','occupation','created_by','team_affiliations','notable_aliases','abilities']
for item in columns_to_fix:
    char_details_preprocessed[item] = char_details_preprocessed[item].apply(lambda row: separate_values(row))
char_details_preprocessed['adapted_by'] = char_details_preprocessed['adapted_by'].apply(lambda x: x.replace('Stephen Mc, Feely','Stephen McFeely'))
len(char_details_preprocessed.columns)


# In[81]:


row_list = []
for index, row in char_details_preprocessed.iterrows():
    row_list.append(list(row.values))
    
cleaned_rows = []
for row in row_list:
    row = map(str,row)
    cleaned_rows.append('("' + '", "'.join(row) + '")')


# In[87]:


'''conn = pymysql.connect(host = '******',user = '*****', passwd = '****', db = 'mysql', 
                       charset = 'utf8')
cur = conn.cursor()
cur.execute('USE marvel_database')

def store_data_frame(df):
    columns = list(char_details_preprocessed.columns)
    columns = ', '.join(columns)
    
    row_list = []
    for index, row in char_details_preprocessed.iterrows():
        row_list.append(list(row.values))
    
    cleaned_rows = []
    for row in row_list:
        row = map(str,row)
        cleaned_rows.append('("' + '", "'.join(row) + '")')
                            
    final_rows = ', '.join(cleaned_rows)
    
    print(f'INSERT INTO character_details_clean ({columns}) VALUES ({final_rows});')
    cur.execute(f'INSERT INTO character_details_clean ({columns}) VALUES {final_rows};')
    cur.connection.commit()

try:
    store_data_frame(char_details_preprocessed)
finally:
    cur.close()
    conn.close()'''

