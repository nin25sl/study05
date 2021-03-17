// 商品リストを表示する関数
let master_table = document.getElementById("itemlist")
console.log("item")

eel.item_list()
eel.expose(get_item_list)
function get_item_list(item){
    let newRow = master_table.insertRow()
    for (i = 0; i < item.length; i++){
        let newCell = newRow.insertCell()
        let newText = document.createTextNode(item[i])
        newCell.appendChild(newText)
    }
}   

//入力されたアイテムコードと個数を取得して、pythonに送る
let order = document.getElementById("order")
order.addEventListener('click', () => {
    let order_code = document.getElementsByName("order_code")[0].value
    let order_num = document.getElementsByName("order_dev")[0].value

    if(order_code == ""){
        alert("アイテムコードを入力してください")
    }else if(order_num == ""){
        alert("個数を入力してください")
    }else{
        eel.buy_information(order_code, order_num)
        eel.expose(get_buy_information)
    }

})

//pythonからの値を受け取り、注文リストを表示する
let orders = []
function get_buy_information(text,flag, order_list){
    if(flag == 0){
        let order_table = document.getElementById("orderlist")
        let newRow = order_table.insertRow()
        for (i = 0; i < order_list.length; i++){
            let newCell = newRow.insertCell()
            let newText = document.createTextNode(order_list[i])
            newCell.appendChild(newText)
        }
        orders.push(order_list)
        console.log(orders)
    }else{
        alert(text)
    }
}

//レジ操作ボタンを押されたときに、合計金額を表示する
sum_price = 0
let calc = document.getElementsByClassName("order_calcurate")[0]
calc.addEventListener('click', ()=> {
    sum_price = 0
    for(i = 0;i < orders.length; i++){
        sum_price += orders[i][4]
    }
    console.log(sum_price)
    if(sum_price > 0){
        calc_result = "合計金額：¥" + sum_price
        document.getElementsByClassName("calcurate_result")[0].innerHTML = calc_result
    }else{
        alert("orderが一件もありません")
    }
})

//再試行を行う（未完成）
let del_order = document.getElementsByClassName("order_delete")[0]
del_order.addEventListener('click', () => {
    // orderlistのテーブルを削除する
    initialize()
})

function initialize(){
    let delete_table = document.getElementById('orderlist')
    for(i = delete_table.rows.length - 1 ; i > 0 ; i--){
        delete_table.deleteRow(i)
    }
    orders = []
    sum_price = 0
    document.getElementsByClassName("calcurate_result")[0].innerHTML =  "合計金額："
    document.getElementsByClassName("back_result")[0].innerHTML = "お釣り："
    document.getElementsByClassName("recept")[0].innerHTML = "レシートファイル："
}

//支払い金額を受け取り、お釣りとレシートファイルを表示する
let allowwance = document.getElementsByClassName("allowwance")[0]
console.log(allowwance)
allowwance.addEventListener('click', () => {
    if(sum_price > 0){
        flag = 0
    }else{
        alert("orderが一件もありません")
    }

    if(flag == 0){
        allowwance_price = document.getElementsByClassName("allowwance_price")[0].value
        if(allowwance_price >= sum_price){
            //レシート作成の追加
            back_price = allowwance_price - sum_price
            back_result = "お釣り：¥" + back_price
            document.getElementsByClassName("back_result")[0].innerHTML = back_result
            
            eel.make_recept(orders, sum_price, allowwance_price)
            eel.expose(recept_output)
        }else{
            alert("支払い金額が足りません")
        }
    }
})

function recept_output(file_name){
    output_file = "レシートファイル：" + file_name
    document.getElementsByClassName("recept")[0].innerHTML = output_file
}

let re = document.getElementsByClassName("re")[0]
re.addEventListener('click', () => {
    initialize()
})
