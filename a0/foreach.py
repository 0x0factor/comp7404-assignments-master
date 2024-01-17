fruits = ['apples','oranges','pears','bananas']
for fruit in fruits:
    print (fruit,'for sale')
    
fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75}
for fruit, price in fruitPrices.items():
    if price < 2.00:
        print(fruit,'cost',str(price),'a pound')
    else:
        print(fruit,' are too expensive!')
