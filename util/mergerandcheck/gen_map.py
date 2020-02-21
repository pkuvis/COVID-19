import datetime
from dateutil.parser import parse as dateparse
import utils
import newname

new_in_file_name = "MergeData_20200213.csv"

new_out_map_file_name = "map.csv"

new_header = ["公开时间", "类别", "省份", "城市", "新增确诊病例", "新增治愈出院数", "新增死亡数", "核减"]

def gen_new_data_key(row):
    return str(row[0])+'-'+str(row[1])+'-'+str(row[2])+'-'+str(row[3])

def gen_new_date_str(datum, start_time_column, end_time_column):
    new_date = dateparse(datum[start_time_column])
    # print(new_date, datum[start_time_column], datum[end_time_column])
    return utils.date_to_str_1(new_date)

def update_map_csv(table_data, table_header, new_header):
    new_data = []
    start_time_column = table_header.index("数据起始时间")
    end_time_column = table_header.index("数据结束时间")
    layer_column = table_header.index("类别")
    country_column = table_header.index("省份")
    province_column = table_header.index("省份")
    city_column = table_header.index("城市")
    new_patient_column = table_header.index("新增确诊病例")
    new_cure_column = table_header.index("新增治愈出院数")
    new_dead_column = table_header.index("新增死亡数")
    new_decr_column = table_header.index("核减")

    map_time_column = 0
    map_type_column = 1
    map_province_column = 2
    map_city_column = 3
    map_new_patient_column = new_header.index("新增确诊病例")
    map_new_cure_column = new_header.index("新增治愈出院数")
    map_new_dead_column = new_header.index("新增死亡数")
    map_new_decr_column = new_header.index("核减")
    map_value_column_start = 4

    source_columns = [new_patient_column, new_cure_column, new_dead_column, new_decr_column]
    target_columns = [map_new_patient_column, map_new_cure_column, map_new_dead_column, map_new_decr_column]
    source_to_target_columns = list(zip(source_columns, target_columns))

    existing_new_data = {}
    for n_index, n_datum in enumerate(table_data):
        if n_datum[0] == "":
            continue
        layer_value = n_datum[layer_column]
        new_row = ["" for i in range(len(new_header))]
        new_row[map_time_column] = gen_new_date_str(n_datum, start_time_column, end_time_column)
        if layer_value == "城市级":
            layer_value = "地区级"
        if layer_value == "国外":
            layer_value = "国家级"
        new_row[map_type_column] = layer_value
        # print(n_index)
        if layer_value == "区县级":
            province_value = n_datum[province_column]
            city_value = n_datum[city_column]
            print("**", "区县级", n_index, province_value, city_value)
            continue
            province_value = newname.get_pure_province_name(province_value)
            city_value = newname.get_pure_city_name(city_value)
            new_row[map_province_column] = province_value
            new_row[map_city_column] = city_value
        elif layer_value == "地区级":
            province_value = n_datum[province_column]
            city_value = n_datum[city_column]
            province_value = newname.get_pure_province_name(province_value)
            city_value = newname.get_pure_city_name(city_value)
            new_row[map_province_column] = province_value
            new_row[map_city_column] = city_value
        elif layer_value == "省级":
            province_value = n_datum[province_column]
            province_value = newname.get_pure_province_name(province_value)
            new_row[map_province_column] = province_value
        elif layer_value == "国家级":
            country_value = n_datum[country_column]
            if (country_value != "中国") and (country_value != ""):
                new_row[map_province_column] = country_value
                new_row[map_city_column] = "NA"
        else:
            print("** unknown", "类别", layer_value)

        for (s, t) in source_to_target_columns:
            new_row[t] = utils.get_entry_value(n_datum[s])

        new_data_key = gen_new_data_key(new_row)
        # print(n_index, new_data_key)
        if new_data_key not in existing_new_data:
            existing_new_data[new_data_key] = [n_index, new_row]
        else:
            print("!! more than one value", n_index, new_data_key, existing_new_data[new_data_key][0])
            for i in target_columns:
                existing_new_data[new_data_key][1][i] += new_row[i]
    for new_data_key in sorted(existing_new_data.keys(), key=lambda x: existing_new_data[x][0]):
        new_data.append(existing_new_data[new_data_key][1])
    return new_data

def gen_new_map(in_file_name, new_header, out_file_name):
    table_data, table_header = utils.read_csv_file(in_file_name)
    new_data = update_map_csv(table_data, table_header, new_header)
    utils.write_csv_file(out_file_name, new_data, new_header)

gen_new_map(new_in_file_name, new_header, new_out_map_file_name)
