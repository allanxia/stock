import requests
from bs4 import BeautifulSoup
import json


#可转债信息类
class Stock:
    #seq 序号
    #name 转债名称
    #code 转债代码
    #price 价格
    #over_rate 溢价率
    #return_rate 到期收益率
    def __init__(self, seq, name, code, price, over_rate, return_rate):
        self.seq = seq
        self.name = name
        self.code = code
        self.over_rate = over_rate
        self.price = price
        self.return_rate = return_rate
        self.score = 0
        self.rank = 0 

    #设置最终得分
    def setScore(self, score):
        self.score = score

    #设置顺序
    def setRank(self, rank):
        self.rank = rank

    #打印输出每支可转载的信息
    def show(self):
        print("seq:%s,name:%s,code:%s,price:%f,over_rate:%f,return_rate:%f,score:%f" % (self.seq, self.name, self.code, self.price, self.over_rate, self.return_rate, self.score))

#Stock对象序列化
class StockEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Stock):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

#可转载爬取类
class StockSpider:
    # url ：可转债信息接口，http://www.ninwin.cn/index.php?m=cb&a=cb_all&show_cb_only=Y&show_listed_only=Y 
    #price_weight：价格权重
    #over_weight：溢价率权重
    #return_weight：收益率权重
    #top_nums：需要展示的可转债数量
    def __init__(self, url, price_weight, over_weight, return_weight, top_nums):
        self.url = url
        self.price_weight = price_weight
        self.over_weight = over_weight
        self.return_weight = return_weight
        self.top_nums = top_nums
        self.stockList = []

    #爬取页面
    def getURL(self):
        headers = {'content-type': 'text/html;charset=gbk',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'}
        rsp = requests.get(self.url, headers = headers)
        return rsp.text

    #解析html中返回的表格，获取可转债的信息
    def parseHtml(self, rsp):
        soup = BeautifulSoup(rsp, "html.parser")
        table = soup.find(id="cb_hq")
        tbody = table.find("tbody")
        for idx, tr in enumerate(tbody.find_all("tr")):
            tds = tr.find_all("td")
            seq = tds[0].contents[0].strip()
            code = tds[1].contents[0].strip()
            name = tds[2].contents[0].contents[0].strip()
            price = float(tds[8].contents[0].strip())
            over_rate = float(tds[15].contents[0].strip().strip("%"))/100.0
            return_rate = float(tds[27].contents[0].strip().strip("%"))/100.0
            stock = Stock(seq, name, code,  price, over_rate, return_rate)
            self.stockList.append(stock)

    #根据价格，溢价率，税前收益率分别排序，计算一个总得分
    def sort(self):
        #价格由低到高
        priceSortedList = sorted(self.stockList, key = lambda x : x.price, reverse = False)
        #溢价率由低到高
        overSortedList = sorted(self.stockList, key = lambda x : x.over_rate, reverse = False)
        #税前收益率由高到低排序
        returnSortedList = sorted(self.stockList, key = lambda x : x.return_rate, reverse = True)

        for i in range(len(self.stockList)):
            stock = self.stockList[i]
            priceIndex = self.index(stock, priceSortedList)
            overIndex = self.index(stock, overSortedList)
            returnIndex = self.index(stock, returnSortedList)
            score = self.price_weight * priceIndex + self.over_weight * overIndex + self.return_weight * returnIndex
            stock.setScore(score)

        #根据打分从低到高排序,这里直接修改stockList中元素的顺序
        self.stockList.sort(key = lambda x : x.score, reverse = False)

        #设置元素的排序
        for i in range(len(self.stockList)):
            self.stockList[i].setRank(i + 1)


    #查询一个对象在list中的位置,从1开始
    def index(self, stock, stockList):
        for i in range(len(stockList)):
            if stockList[i].code == stock.code:
                return i + 1

    def run(self):
        rsp = self.getURL()
        self.parseHtml(rsp)
        self.sort()
        #只返回top的信息
        return self.stockList[:self.top_nums]


def main():
    url = "http://www.ninwin.cn/index.php?m=cb&a=cb_all&show_cb_only=Y&show_listed_only=Y"
    s = StockSpider(url = url, 
                    price_weight = 1, 
                    over_weight = 1,
                    return_weight = 1, 
                    top_nums = 20)
    s.run()

if __name__ == "__main__":
    main()
