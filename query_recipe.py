from pymongo import MongoClient
import random

def query_recipe(rs, obj):
    try:
        conn = MongoClient("mongo", 27017)
        db = conn.recipe
        collection = db.images.files

        result_list = []
        output_list = []
        selected = []
        result = collection.find({"菜式": rs})
        for r in result:
            result_list.append(r)

        for s in result_list:
            if obj in s["食材"]:
                ind = result_list.index(s)
                selected.append(ind)
                output_list.append(s)

        while len(output_list) < 3:
            n = random.randint(range(0, len(result_list)))
            if n not in selected:
                output_list.append(result_list[n])
            else:
                pass
        else:

            choose = random.sample(range(0, len(output_list)), 3)
            output = []
            for i in choose:
                output.append(output_list[i])
            return output
    finally:
        conn.close()

# print(query_recipe("韓式", "洋蔥"))
qr = query_recipe("韓式", "洋蔥")

print(qr[0])
print(qr[0]["食譜照"])





