import eel
import pandas as pd
import datetime
import os

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_code(self):
        return self.item_code

    def get_name(self):
        return self.item_name

    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_name_list = []
        self.item_price_list = []
        self.item_quantity = []
        self.item_master=item_master
   
    def add_item_order(self,item_code, item_name,item_price,item_quantity):
        self.item_order_list.append(item_code)
        self.item_name_list.append(item_name)
        self.item_price_list.append(item_price)
        self.item_quantity.append(item_quantity)
        
    def view_item_list(self):
        for i in range(len(self.item_order_list)):
            sum = int(self.item_quantity[i]) * int(self.item_price_list[i])
            print("商品コード:{}".format(self.item_order_list[i]),"商品名:{}".format(self.item_name_list[i]),"値段:{}".format(self.item_price_list[i]), "個数:{}".format(self.item_quantity[i]), "合計金額:{}".format(sum))

    def make_item_list_recept(self, file_name):
        text = '------注文品-----'
        self.make_order_recept(text,file_name)
        text = ''
        for i in range(len(self.item_order_list)):
            sum = int(self.item_quantity[i]) * int(self.item_price_list[i])
            tuple = "商品コード:{}".format(self.item_order_list[i]),"商品名:{}".format(self.item_name_list[i]),"値段:{}".format(self.item_price_list[i]), "個数:{}".format(self.item_quantity[i]), "合計金額:{}".format(sum)
            for string in tuple:
                text += string + ","
            self.make_order_recept(text, file_name)
            text = ''

    #不要コード
    def registration(self, item_code):
        #アイテム登録
        name = input("名前を入力してください>>> ")
        #price = int(input("値段を入力してください>>> "))
        #個数の追加     
        quantity = input('個数を入力してください')

        if len(item_code) == 1:
            item_code = "00" + item_code
        elif len(item_code) == 2:
            item_code = "0" + item_code
        else:
            item_code = item_code
        self.add_item_order(item_code, name)
    
    def get_sum_price(self):
        sum = 0
        for price, quantity in zip(self.item_price_list, self.item_quantity):
            sum += int(price) * int(quantity)
        return sum
    
    def make_recept_sumprice(self, file_name):
        text = '-----合計金額-----'
        self.make_order_recept(text, file_name)
        sum = 0
        for price, quantity in zip(self.item_price_list, self.item_quantity):
            sum += int(price) * int(quantity)
        text = sum
        self.make_order_recept(text, file_name)
    
    def make_order_recept(self,text, file_name):
        path = './recept/' + file_name
        text = str(text)

        if os.path.exists(path):
            with open(path, mode = 'a') as f:
                f.write('\n' + text)
        else:
            with open(path, mode = 'w') as f:
                f.write(text)

class Allowwance:
    def __init__(self,price):
        self.price = price
    
    def calcurate(self, money):
        back = money - self.price
        if back < 0:
            print("支払い金額が{}円足りません".format(0-back))
            return False
        else:
            print("支払いが完了しました")
            print("お釣りは{}円です".format(back))
            return True
    
    def make_recept_calcurate(self, money, file_name):
        text = '-----お支払い金額-----'
        self.make_recept(text, file_name)
        text = money
        self.make_recept(text, file_name)
        back = money - self.price
        text = '-----お釣り-----'
        self.make_recept(text, file_name)
        text = "お釣りは{}円です".format(back)
        self.make_recept(text, file_name)

    def make_recept(self, text,file_name):
        path = './recept/' + file_name
        text = str(text)
        with open(path, mode = 'a') as f:
            f.write('\n' + text)

#csvからマスタを読み込み、javascript側へ返す
def make_item_master():
    df = pd.read_csv('./master.csv', header = None, dtype=object)
    read_csv = []
    for i in range(len(df)):
        read_csv.append(df.iloc[i].tolist())
    # マスタ登録
    item_master = []

    for item in read_csv:
        item_master.append(Item(item[0], item[1], int(item[2])))
    
    return item_master

def item_list():
    item_master = make_item_master()
    back_list = []
    for item in item_master:
        back_list = ["{}".format(item.get_code()), "{}".format(item.get_name()), "{}".format(item.get_price())]
        eel.get_item_list(back_list)

#html側での購入リストを受け取り、コード、名前、値段、個数、合計値段を返す
def buy_information(order_code, order_num):
    item_master = make_item_master()
    flag = 0
    for item in item_master:
        if order_code == item.get_code():
            name = item.get_name()
            price = item.get_price()
            flag = 0
            break
        else:
            flag = 1

    if flag == 0:
        sum_price = int(order_num) * int(price)
        order_list = [order_code, name, price, order_num, sum_price]
        text = f"商品コード：{order_code}, 商品名：{name}, 個数：{order_num}, 合計：¥{sum_price}"
        order_list = [order_code, name,price, order_num, sum_price]
        eel.get_buy_information(text, flag, order_list)
    else:
        text = f"商品が存在しません(Error: Code[{order_code}] not exist)"
        eel.get_buy_information(text, flag)
#レシートを作る関数
def make_recept(order_list, sum_price, allowwance_price):
    dt_now = datetime.datetime.now()
    file = dt_now.strftime('%Y-%m-%d-%H-%M-%S')

    write_file(file, '------注文品-----')
    for order in order_list:
        code = order[0]
        name = order[1]
        price = order[2]
        num = order[3]
        one_price = order[4]
        text = f'商品コード:{code},商品名:{name},値段:{price},個数:{num},合計:{one_price}'
        write_file(file, text)
    
    write_file(file, '-----合計金額-----')
    text = f'合計は¥{sum_price}です'
    write_file(file, text)

    write_file(file, '-----お支払い金額-----')
    text = f'¥{allowwance_price}お預かりします'
    write_file(file, text)

    write_file(file, '-----お釣り-----')
    back_price = int(allowwance_price) - int(sum_price)
    text = f'お釣りは¥{back_price}です'
    write_file(file, text)

    eel.recept_output(file)

def write_file(file, text):
    path = './recept/' + file
    text = str(text)

    if os.path.exists(path):
        with open(path, mode = 'a') as f:
            f.write('\n' + text)
    else:
        with open(path, mode = 'w') as f:
            f.write(text)


