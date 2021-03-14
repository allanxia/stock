from flask import Flask, Response
#引入模版插件
from flask import render_template
from flask import request
from stock import StockSpider, StockEncoder
import json

app = Flask(__name__,
        static_folder = "./vue/static", #设置静态资源目录
        template_folder = "./vue") #设置vue编译输出的文件夹,为Flask模版文件目录

@app.route("/")
def index():
    return render_template("index.html", name="index") 

@app.route("/getStocks")
def getStocks():
    #获取输入参数信息
    price_weight = round(float(request.args.get("price_weight").strip()), 4)
    over_weight = round(float(request.args.get("over_weight").strip()), 4)
    return_weight = round(float(request.args.get("return_weight").strip()), 4)
    top_nums = int(request.args.get("top_nums").strip())

    #爬取可转债信息并打分，返回排名靠前的可转债
    url = "http://www.ninwin.cn/index.php?m=cb&a=cb_all&show_cb_only=Y&show_listed_only=Y"
    s = StockSpider(url = url, 
                    price_weight = price_weight , 
                    over_weight = over_weight ,
                    return_weight = return_weight , 
                    top_nums = top_nums )
    stockList = s.run()
    return Response(json.dumps(stockList, cls=StockEncoder), mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
