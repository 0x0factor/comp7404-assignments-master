import shop

shopName = 'HKU ParknShop'
fruitPrices = {'apples': 1.00, 'oranges': 1.50, 'pears': 1.75}
hkushop = shop.FruitShop(shopName, fruitPrices)
applePrice = hkushop.getCostPerPound('apples')
print('Apples cost $%.2f at %s.' % (applePrice, shopName))

otherName = 'Wellcome Westwood'
otherFruitPrices = {'kiwis':6.00, 'apples': 4.50, 'peaches': 8.75}
otherFruitShop = shop.FruitShop(otherName, otherFruitPrices)
otherPrice = otherFruitShop.getCostPerPound('apples')
print('Apples cost $%.2f at %s.' % (otherPrice, otherName))
print("Wow, that's expensive!")