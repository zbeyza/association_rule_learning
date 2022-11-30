# ARL : Association Rule Learning

![Fc8KikNXwAIi6pT](https://user-images.githubusercontent.com/81737980/204904777-c4f8ce58-188f-422c-8c89-092c7ec6a863.jpg)

A rule-based machine learning technique used to find patterns in data. The Apriori Algorithm is used while the Association Rule Learning takes place. The Apriori algorithm calculates possible product pairs according to the support threshold value determined at the beginning of the process and creates the final table by making eliminations according to the support value determined in each iteration.

In this project after data preprosessing, Invoice-Item matrix is obtained which is needed for Apriori Algortihm. Afterwards, items that occur frequently together were found using the apriori algorithm and a rule table was obtained using the association rules method. After the rule table is created, a sorting is made according to the need and then the recommendation process is performed.

### You can reach the detailed explanation of the projects from the links below:
https://medium.com/@zbeyza/recommendation-systems-arl-association-rule-learning-bed1a07b5d9a

# About Data Set:
Online Retail II data set contains all the transactions occurring for a UK-based and registered, non-store online retail between 01/12/2009 and 09/12/2011.The company mainly sells unique all-occasion gift-ware. Many customers of the company are wholesalers.

# Variables:
- Invoice: Invoice number. Nominal. A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter ‘C’, it indicates a cancellation.
- StockCode: Product (item) code. Nominal. A 5-digit integral number uniquely assigned to each distinct product.
- Description: Product (item) name. Nominal.
- Quantity: The quantities of each product (item) per transaction. Numeric.
- InvoiceDate: Invoice date and time. Numeric. The day and time when a transaction was generated.
- UnitPrice: Unit price. Numeric. Product price per unit in sterling (£).
- CustomerID: Customer number. Nominal. A 5-digit integral number uniquely assigned to each customer.
- Country: Country name. Nominal. The name of the country where a customer resides.

### Source: 
https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

