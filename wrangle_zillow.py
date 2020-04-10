from env import host, password, user
import pandas as pd
import numpy as np
import os

database = "zillow"

query = '''
SELECT *
FROM properties_2017
JOIN predictions_2017 USING(id)
WHERE (predictions_2017.transactiondate >= '2017-05-01' AND predictions_2017.transactiondate <= '2017-06-30')
	AND propertylandusetypeid = "261"
	AND bathroomcnt > 0
	AND bedroomcnt > 0
	AND calculatedfinishedsquarefeet > 0
	AND taxamount > 0
	AND taxvaluedollarcnt > 0
;
'''





def pull_csv_file():
    global database
    global query
    url = f'mysql+pymysql://{user}:{password}@{host}/{database}'
    plain_data = pd.read_sql(query, url)
    plain_data.to_csv("zillow_plain_data.csv")
    

def check_for_json_file(file_name):
    if os.path.exists(file_name) == False:
        pull_csv_file()


def wrangle_plain_data():
    plain_data = pd.read_csv("zillow_plain_data.csv")
    plain_data["tax_rates"] = (plain_data.taxamount / plain_data.taxvaluedollarcnt) * 100
    return plain_data


def wrangle_zillow():

    data = [["CA", "Los Angeles", 6037], ["CA", "Orange County", 6059], ["CA", "Ventura County", 6111]]
    fips = pd.DataFrame(data, columns= ["state", "county", "fips"])
    zillow_data = pd.read_csv("zillow_plain_data.csv")
    zillow_data = zillow_data.drop(columns = "Unnamed: 0")
    zillow_data = zillow_data.dropna(axis=1, thresh=10_000)
    zillow_data = zillow_data.dropna()
    zillow_data.fips = zillow_data.fips.astype(int)
    zillow_data = zillow_data.merge(fips, left_on="fips", right_on="fips")
    zillow_data = zillow_data.rename(columns={"bathroomcnt": "bathrooms", "bedroomcnt": "bedrooms", "calculatedfinishedsquarefeet": "square_feet", "taxvaluedollarcnt": "house_value"})
    zillow_data["bedroom_sqft"] = zillow_data.bedrooms * 219
    zillow_data["bathroom_sqft"] = zillow_data.bathrooms * 40
    zillow_data["sqft_without_bedroom_bathroom"] = zillow_data["square_feet"] - zillow_data["bedroom_sqft"] - zillow_data.bathroom_sqft
    zillow_data["sqft_without_bathroom"] = zillow_data["square_feet"]  - zillow_data.bathroom_sqft
    zillow_data["total_area"] = zillow_data["sqft_without_bedroom_bathroom"] + zillow_data.lotsizesquarefeet	
    return zillow_data

def wrangle_mvp(df):
    mvp = df[["bathrooms", "bedrooms", "square_feet", "house_value"]]
    return mvp

def wrangle_final_model(df):
    mvp = df[["bathroomcnt", "bedroomcnt", "calculatedfinishedsquarefeet", "taxvaluedollarcnt", "county", "state", "landtaxvaluedollarcnt", ]]
    mvp = mvp.rename(columns={"bathroomcnt": "bathrooms", "bedroomcnt": "bedrooms", "calculatedfinishedsquarefeet": "square_feet", "taxvaluedollarcnt": "house_value", "landtaxvaluedollarcnt": "tax_amount"})
    return mvp

def add__house_value_bins(df):
    df["house_value_bin"] = pd.cut(df.taxamount, 4, labels=["> 45K", "> 88K", "> 132K", ">175K"])
    return df

def wrangle_geo_data(df):
    data = [["CA", "Los Angeles", 6037], ["CA", "Orange County", 6059], ["CA", "Ventura County", 6111]]
    fips = pd.DataFrame(data, columns= ["state", "county", "fips"])
    df.fips = df.fips.astype(int)
    geo_data = df.merge(fips, left_on="fips", right_on="fips")
    return geo_data

def remove_outliers(zillow_data):        
    zillow_data = zillow_data.drop(zillow_data[zillow_data.bathrooms > 7].index) # 100

    zillow_data = zillow_data.drop(zillow_data[zillow_data.square_feet > 5_000].index) # 125

    zillow_data = zillow_data.drop(zillow_data[zillow_data.bedrooms > 6].index) # 23

    zillow_data = zillow_data.drop(zillow_data[zillow_data.lotsizesquarefeet > 2_000_000].index) #1

    return zillow_data

def wrangle_adv():
    zillow_data = wrangle_zillow()
    zillow_data = remove_outliers(wrangle_zillow)
    zillow_data["bedroom_sqft"] = zillow_data.bedrooms * 219
    zillow_data["sqft_without_bedroom"] = zillow_data["square_feet"] - zillow_data["bedroom_sqft"]
    return zillow_data
