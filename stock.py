


class Stock:
    def __init__(self,name,buy_price,qty):
        self.name = name
        self.buy_price = buy_price
        self.qty = qty
        
    def value(self):
        return self.buy_price*self.qty
    
    def to_dict(self):
        return{
            "stock_name" : self.name,
            "buy_price" : self.buy_price,
            "quantity" : self.qty,
            "total_value" : self.value()
        }


# s = Stock("Apple" , 4 , 77)
# print(s.to_dict())