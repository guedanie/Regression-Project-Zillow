# Linear Regression Project

## Objectives: 
1. To wrangle the data, remove, null values and filter features to meet the brief's especifications.
1. Find the best key features to predict the tax assessed value of single unit properties that the tax district assessed during the months of May 2017 - June 2017. 
1. To generate and evaluate an effective linear regression model using key features to help predict property values.
1. To calculate tax rates and provide a visual distribution of tax rate for all counties that the properties are located in
1. Present the findings in report

## Project Brief:
> We want to be able to predict the values of single unit properties that the tax district assesses using the property data from those whose last transaction
was during the "hot months" (in terms of real estate demand) of May and June in 2017. We also need some additional information outside of the model.

> Zach lost the email that told us where these properties were located. Ugh, Zach :-/. Because property taxes are assessed at the county level, 
we would like to know what states and counties these are located in.

> We'd also like to know the distribution of tax rates for each county.

> The data should have the tax amounts and tax value of the home, so it shouldn't be too hard to calculate. Please include in your report to us the 
distribution of tax rates for each county so that we can see how much they vary within the properties in the county and the rates the bulk of the 
properties sit around.

> Note that this is separate from the model you will build, because if you use tax amount in your model, you would be using a future data point to 
predict a future data point, and that is cheating! In other words, for prediction purposes, we won't know tax amount until we know tax value.

## Executive Summary: 

1. I found that bathroom square footage and total property square footage were two of the most important features when it came to calculating tax assessed home value. The key insight is that the target variable is not "market house price" (i.e not what the seller would value their house), but rather what the county values the property as for tax purposes. This means that the focus needs to be on features that tax assessors look for when evaluating properties, and number of bathrooms, as well as bathroom count, are key features because they are a good indicator of the property's quality. Number of bedrooms is not always as reliable, because this is a key driver of market value, which leads to many homeowners to create smaller bedrooms to inflate this metric. 

    * A successful model was created using bedroom square feet, bathroom square feet, and total square feet (excluding bathroom and bedroom square footage). These features were engineered using the data and domain knowledge to help reduce the dependency that the original features share, which was leading a skew in the model. 

### Further improvements:
* To improve the model, we would need more features that are important to tax assessors, such as:
    * Location: While latitude and longitude is avialable in the data, any useful analysis would require a clustering algorithms to group locations of higher value, and currently this is not possible. 
    * Quality features: Garage square footage, pool size, number of fireplaces, etc. These are factors that tax assessors are more likely to look at, rather than bedroom count, because they are a better representation of the quality of the property. Unfortunately, the data available has a lot of null values for all of these categories, which makes them unsable for the model. 

## Requirements to access report:

1. To access the full report, the repo needs to be cloned, along with all the .py files.
1. Due to the size of the data, the report pulls the data from a SQL database. In order to get access to the data, and the report, an env.py file will need to be present in the same directory that the files are cloned to, and the file needs to have the following variables:
    `user` = username information for the sql database
    `host` = host number
    `password` = password. 

    The `wrangle.py` file will look for the env.py file to access the SQL database and pull the data. A new file csv file will then be created and stored in the same directory for future use. 
