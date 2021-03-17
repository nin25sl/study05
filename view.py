import eel
import possystem
import desktop

app_name="html"
end_point="index.html"
size=(700,600)

@eel.expose
def item_list():
    possystem.item_list()
    #return result

@eel.expose
def buy_information(order_code, order_num):
    possystem.buy_information(order_code, order_num)

@eel.expose
def make_recept(order_list, sum_price, allowwance_price):
    possystem.make_recept(order_list, sum_price, allowwance_price)

desktop.start(app_name,end_point,size)
