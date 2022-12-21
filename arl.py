###################
# Data Preprocessing
###################

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import warnings
warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
pd.set_option("display.expand_frame_repr", False)

df_original = pd.read_excel("datasets/online_retail_II.xlsx",
                            sheet_name = ["Year 2009-2010", "Year 2010-2011"])

df1 = df_original["Year 2009-2010"]
df2 = df_original["Year 2010-2011"]
df_ = df1.append(df2)

df = df_.copy()

df.shape

df.describe().T
# as you can see there are negative values, because of the returned products.
# we need to get rid of them.

df.describe().T
# as you can see there are negative values, because of the returned products.
# we need to get rid of them.

# getting rid of the returned products and NaNs and selecting quantitiy an price as bigger than 0
def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)  # eksisk değerlerin silinmesi
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    return dataframe

df = retail_data_prep(df)

df.describe().T
# as you can see negative values are no longer exist

df.isnull().sum()
# no more missing values

# limitation for outliers
def outlier_threshold(dataframe, varibale):
    quartile1 = dataframe[varibale].quantile(0.01)
    quartile3 = dataframe[varibale].quantile(0.99)
    # the reason why 0.01 and 0.99 are used is arrange outliers without making harsh changes in dataset
    interquartile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquartile_range
    low_limit = quartile1 - 1.5 * interquartile_range
    return low_limit, up_limit

# suppress outliers
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_threshold(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

replace_with_thresholds(df, "Quantity")
replace_with_thresholds(df, "Price")

###################
# Prepare ARL Data Structure
###################

# Invoice-Product Matrix:

# Description   NINE DRAWER OFFICE TIDY   SET 2 TEA TOWELS I LOVE LONDON    SPACEBOY BABY GIFT SET
# Invoice
# 536370                              0                                 1                       0
# 536852                              1                                 0                       1
# 536974                              0                                 0                       0
# 537065                              1                                 0                       0
# 537463                              0                                 0                       1

# reduction of the dataset to a single country
df_fr = df[df["Country"] == "France"]
df_fr.head()

df_fr.shape

df_fr.groupby(["Invoice", "StockCode"]).agg({"Quantity": "sum"}). \
    unstack(). \
    fillna(0). \
    applymap(lambda x: 1 if x > 0 else 0).iloc[0:8, 0:8]


def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)

fr_inv_pro_df = create_invoice_product_df(df_fr, id=True)
# Having product names as variable names causes it to take up a lot of memory and the code to run slowly,
# so it is healthier to name the variables with their stockCodes, not the product names.

fr_inv_pro_df.iloc[0:8, 0:8]

# reach description via stock code
def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)

check_id(df_fr, 10002)

#################
# Association Rules
#################

# items that occur frequently together and reach a predefined level of support and confidence
frequent_itemsets = apriori(fr_inv_pro_df,
                            min_support=0.01,
                            use_colnames=True)

frequent_itemsets.sort_values("support", ascending=False)

# association rules
rules = association_rules(frequent_itemsets,
                          metric="support",
                          min_threshold=0.01)

"""
antecedents : first product
consequents : second product
antecedent support : proportion of transactions that contains antecedent A
consequent support : proportion of transactions that contains consequent C
support : items’ frequency of occurrence
confidence : conditional probability of purchasing consequents C when antecedents A is purchased
lift : How many times the probability of purchasing consequents C increases when antecedents A is purchased
leverage : similar to lift but it gives priority to higher support.
conviction : expected frequency of antecedents A without consequent C
"""

#filtering associatiion fules with support, confidence and lift values
rules[(rules["support"] > 0.05)
      & (rules["confidence"] > 0.1)
      & (rules["lift"] > 5)].sort_values("confidence", ascending=False)

##################
# Product Recommendation
##################

def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

    return recommendation_list[0:rec_count]

arl_recommender(rules, 22492, 2)

# checking the product names from the id of the products going to recommend

def check_id(dataframe, stock_code):
    product_names = []
    for i in stock_code:
        product_name = dataframe[dataframe["StockCode"] == i][["Description"]].values[0].tolist()
        print(f"{i} : {product_name}")


check_id(df_fr, arl_recommender(rules, 22492, 2))


#################
# Script
#################

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe


def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)



def create_rules(dataframe, id=True, country="France"):
    dataframe = dataframe[dataframe['Country'] == country]  # ülkeye göre veriyi indirge
    dataframe = create_invoice_product_df(dataframe, id)
    frequent_itemsets = apriori(dataframe, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
    return rules


df = df_.copy()

df = retail_data_prep(df)
rules = create_rules(df)

rules[(rules["support"] > 0.05)
      & (rules["confidence"] > 0.1)
      & (rules["lift"] > 5)].sort_values("confidence", ascending=False)

def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

    return recommendation_list[0:rec_count]


def check_id(dataframe, stock_code):
    product_names = []
    for i in stock_code:
        product_name = dataframe[dataframe["StockCode"] == i][["Description"]].values[0].tolist()
        print(f"{i} : {product_name}")

check_id(df_fr, arl_recommender(rules, 22492, 2))







