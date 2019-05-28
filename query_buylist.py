import pymysql

user_id = 44
conn = pymysql.connect(host="192.168.33.200", user="root", password="my-secret-pw", port=3306, database="db01")
cur = conn.cursor()
query = "SELECT contents FROM buylist WHERE userid = %s ORDER BY buydatetime DESC limit 1"

cur.execute(query, user_id)

result = cur.fetchone()

plist = []
alist = []
result1 = result[0][2:-2]
# print(result1)
result2 = result1.split("', '")
# print(result2)
for i in result2:
    result3 = i.split(",")
    # print(result3)
    for j in result3:

        if j.isdigit():
            alist.append(j)
        else:
            plist.append(j)
print(plist)
print(alist)

query = "DROP TEMPORARY TABLE IF EXISTS `productprice`;"
cur.execute(query)
query = ("CREATE TEMPORARY TABLE productprice (`item_id` INT NOT NULL AUTO_INCREMENT, "
         "`item_name` VARCHAR(50) NOT NULL,"
         "`amount` INT NOT NULL, "
         "PRIMARY KEY(`item_id`));")
cur.execute(query)
for i in range(len(plist)):
    query = "INSERT INTO productprice (item_name, amount) VALUES (%s, %s)"
    info = (plist[i], alist[i])
    cur.execute(query, info)
    conn.commit()

query = "SELECT pp.item_name , pp.amount, ip.priceperunit, pp.amount*ip.priceperunit total FROM productprice pp, itemprice ip WHERE pp.item_name = ip.itemname"
# query = "SELECT * FROM productprice"
cur.execute(query)
resultf = cur.fetchall()
flist = []
for l in resultf:
    dic1 = {}
    dic1["pname"] = l[0]
    dic1["amount"] = l[1]
    dic1["priceperunit"] = l[2]
    dic1["total"] = l[3]
    flist.append(dic1)
print(flist)
conn.close()

