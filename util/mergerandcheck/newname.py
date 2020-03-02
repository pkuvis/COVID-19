import json

with open("trans.json", encoding="utf-8") as f:
    name_old_to_new = json.load(f)

name_new_to_old = {}
for key in name_old_to_new:
    value = name_old_to_new[key]
    name_new_to_old[value] = key

def get_pure_province_name(province_name):
    if province_name in name_old_to_new:
        province_name = name_old_to_new[province_name]
    else:
        #if province_name not in name_new_to_old:
        #    print("*** not found province", province_name)
        # else:
        #     print("*** found new", province_name, "old is", name_new_to_old[province_name])
        province_name = province_name.replace("省", "")
        province_name = province_name.replace("市", "")
        province_name = province_name.replace("壮族自治区", "")
        province_name = province_name.replace("回族自治区", "")
        province_name = province_name.replace("维吾尔自治区", "")
        province_name = province_name.replace("自治区", "") # 内蒙古，西藏
        province_name = province_name.replace("卫生健康委员会", "")
    return province_name

def get_pure_city_name(city_name):
    if city_name in name_old_to_new:
        city_name = name_old_to_new[city_name]
        #if city_name.find("市") != -1:
        #    print("*** find 市", city_name)
    else:
        #if city_name not in name_new_to_old:
        #    print("*** not found city", city_name)
        # else:
        #     print("*** found new", city_name, "old is", name_new_to_old[city_name])
        city_name = city_name.replace("市", "")
    return city_name
