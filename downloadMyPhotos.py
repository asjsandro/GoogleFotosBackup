#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import os
from Google import Create_Service
import pandas as pd
import requests


# In[2]:


pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 150)
pd.set_option('display.max_colwidth', 150)
pd.set_option('display.width', 150)
pd.set_option('expand_frame_repr', True)


# In[3]:


CLIENT_SECRET_FILE = 'client_secret_GoogleCloudPlatform.json'
API_NAME = 'photoslibrary'
API_VERSION = 'v1'
SCOPES = ['https://photoslibrary.googleapis.com']


# In[4]:


def download_file(url:str, destination_folder:str, file_name:str):
    response = requests.get(url)
    if response.status_code == 200:
        print('Download file {}'.format(file_name))
        with open(os.path.join(destination_folder, file_name), 'wb') as f:
            f.write(response.content)
            f.close()


# In[5]:

print("Criando o Serviço no Google Platform!!")
service = Create_Service(CLIENT_SECRET_FILE, API_NAME,API_VERSION, SCOPES)


# In[6]:


"""
list method
"""
response = service.mediaItems().list(
    pageSize=100).execute()

lstItens = response.get('mediaItems')
nextPageToken = response.get('nextPageToken')


# In[7]:


interacao = 0
while nextPageToken and interacao < 3:
    response = service.mediaItems().list(
        pageSize=100,
        pageToken=nextPageToken).execute()
    lstItens.extend(response.get('mediaItems'))
    nextPageToken = response.get('nextPageToken')
    interacao += 1


# In[8]:


dfItens = pd.DataFrame(lstItens)


# In[9]:


destination_folder = r'download'
for index, dfIten in dfItens.iterrows():
    file_name = dfIten['filename']
    download_url = dfIten['baseUrl'] + '=d'
    download_file(download_url, destination_folder, file_name)
    if index == 100:
        break
