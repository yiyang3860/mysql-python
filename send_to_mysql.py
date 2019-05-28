import pymysql
from time import sleep
import os
from query_recipe import query_recipe
import requests

dic1 = {"carrot": "紅蘿蔔", "onion": "洋葱", "chili": "辣椒", "greenpepper": "青椒", "springonion": "葱"}
conn = pymysql.connect(host="mysql", user="root", password="my-secret-pw", port=3306, database="db01")
cur = conn.cursor()

# 開人臉csv
path = os.path.abspath('.')

old_face_time = ""
newq_objresult = []
old_objresult = []

while True:
    ld = os.listdir(path+"/usr_info")
    print(ld)
    # directory not empty
    if ld:
        with open(path+'/usr_info/OutPut_info.csv', 'r', encoding="utf-8") as f:
            face = f.readlines()
            facer = face[1][:-20]
            print(facer)
            print(face[1][0])
            face_time = face[1][-19:]
            # face not none and time not old time
            if face[1][0] != "unknown" and face_time != old_face_time:
                # face write to redis
                # conn.set("face1", facer)
                # detect objresult
                # write face_time as old_face_time
                old_face_time = face_time

                # query objresult directory as newq_objresult
                newq_objresult = os.listdir(path + '/objresult')
                # comparable newqobjresult and old_objresult
                new_objresult = list(set(newq_objresult).difference(set(old_objresult)))
                # find the newobjresult and take item name
                objlst = []
                # objal = []
                for objresult in new_objresult:
                    old_objresult = newq_objresult
                    print(path + '/objresult/' + objresult)
                    with open(path + '/objresult/' + objresult, 'r', encoding='utf-8') as obj:
                        objrs = obj.read().split("\n")
                        if len(objrs) != 0:
                            for o in range(len(objrs)):
                                objf = objrs[o].split(",")[0]
                                # amount = objrs[o].split(",")[1]
                                objlst.append(objf)
                                # objal.append((objf, amount))
                                print(objf)
                                print(str(objlst))
                                # print("objrs",objrs)
                                # print("objal",objal)
                            # # obj write to redis
                            # conn.set("obj1", str(objlst))
                            # print(conn.get("obj1"))


                            with open(path + '/recipeoutput/object.csv', "r", encoding="utf-8") as rr:
                                rs = rr.read()
                                print(rs)
                                qr = query_recipe(rs, dic1[objlst[0]])
                                # write recipe to redis
                                # conn.set("rr1", str(qr))
                                rlist = []
                                for q in qr:
                                    id = str(q['_id'])
                                    rlist.append(id)
                                print(rlist)
                                idquery = "SELECT userid, lineid FROM userprofile WHERE username = %s"
                                username = facer
                                cur.execute(idquery, username)
                                idr = cur.fetchone()
                                print(idr)
                                cur.fetchall()
                                query = "INSERT INTO buylist (userid, contents, buydatetime, idrecomrecipe1, idrecomrecipe2, idrecomrecipe3, confirmstatus) VALUES (%s, %s, %s, %s, %s, %s, 0)"
                                info = (str(idr[0]), str(objrs), str(face_time), str(rlist[0]), str(rlist[1]), str(rlist[2]))

                                cur.execute(query, info)
                                conn.commit()

                                data = {
                                    "user_id": idr[0],
                                    "line_id": idr[1],
                                    "recomrecipe1": str(qr[0]["食譜連結"]),
                                    "recomrecipe2": str(qr[1]["食譜連結"]),
                                    "recomrecipe3": str(qr[2]["食譜連結"]),

                                }


                                r = requests.post("https://cb10502.serveo.net/touser", data=data)


                        else:
                            pass
            else:
                sleep(3)
    else:
        print("No user")

conn.close()
# print(type(os.listdir(path + '/objresult')))
    # if ld != None and
# with open("/usr_info/Output")
# conn.set("face1", )

# list1 = ["a", "b", "c"]
# list2 = ["a", "b", "c", "d"]
# list3 = list(set(list2).difference(set(list1)))
# print(list3)
