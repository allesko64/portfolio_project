from stock import Stock

class Portfolio:
    def __init__(self):
        self.stocks = []


    def check_stock(self ,stock_name):
        return any(s.name == stock_name for s in self.stocks)


    def add_stock(self,stock):
        if(not(self.check_stock(stock.name))):
            self.stocks.append(stock)
          

    def delete_stock(self,name):
        if(self.check_stock(name)):
            for s in self.stocks:
                if(s.name == name):
                    self.stocks.remove(s)
                    break
        

    def total_value(self):
        total_sum = 0
        for s in self.stocks:
            total_sum += s.value()
        return total_sum
    
    def get_all_stock(self):
        return [s.to_dict() for s in self.stocks]



# p = Portfolio()
# p.add_stock(Stock("tesla" , 56 , 76))
# p.add_stock(Stock("apple" , 87 , 99))
# print(p.get_all_stock())