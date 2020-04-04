import pandas as pd

df = pd.read_csv("~/Downloads/Neighborhood_Zhvi_AllHomes.csv")

clt = df[df['City'] == 'Charlotte']


#Zip Code Data

df = pd.read_csv("~/Downloads/Zip_Zhvi_AllHomes.csv", encoding='latin-1')

clt = df[df['City'] == 'Charlotte']

clt = clt[clt['State'] == 'NC']