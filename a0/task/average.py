"""
Run python autograder.py 
"""

def average(priceList):
    "Return the average price of a set of fruit"
    priceset = set(priceList)
    return sum(priceset)/len(priceset)