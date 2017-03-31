import re
import csv
import time


def get_row_counts():
# 获取信息表中记录的数量
    f_rd = open('staff_table.csv', 'r',encoding="utf-8")
    readlines = csv.reader(f_rd)
    line_count = 0
    for line in readlines:
        if len(line) > 0:
            line_count += 1
    f_rd.close()
    print("count : %s"%line_count)
    return line_count


def get_record_count_and_column_location():
    f_rd = open('staff_table.csv', 'r', encoding="utf-8")
    readlines = csv.reader(f_rd)
    result = {}
    count = 0
    for line in readlines:
        if len(line) > 0:
            if count == 0:
                for i in range(len(line)):
                    result[line[i]] = i
                    # result[i] = line[i]
            count += 1
    f_rd.close()
    result["count"] = count - 1
    # print(result)
    return result

def get_records_msg(table_msg , *column_names ):
    print(column_names)
    f_rd = open('staff_table.csv', 'r', encoding="utf-8")
    readlines = csv.reader(f_rd)
    count = 0
    record_msg = {}
    for column_name in column_names:
        record_msg[column_name] = []
    for line in readlines:
        if len(line) > 0:
            if count > 0 :
            #文件数据部分
                for column_name in column_names:
                    if column_name in table_msg:
                        record_msg[column_name].append( line[table_msg[column_name]] )
            count += 1
    f_rd.close()
    return record_msg


def write_to_csv(filename , data):
    csvfile = open(filename , 'a+',encoding="utf-8")
    writer = csv.writer(csvfile)
    write_data = []
    write_data.append(data)
    writer.writerows(write_data)
    csvfile.close()

def create_record():
    table_msg = get_record_count_and_column_location()
    record_list = []
    table_records = get_records_msg(table_msg, "staffid","phone"  )
    print("table_records: %s"%table_records)
    if "staffid" in table_records and len( table_records["staffid"] ) > 0 :
        #有记录, staffid 自增
        staffid_str = int( table_records["staffid"].pop() )  + 1
    else:
        #无记录，staffid = 0
        staffid_str = 0
    print("请输入员工信息")
    record_list.append(staffid_str)
    name_str = input("姓名:").strip()
    record_list.append(name_str)
    age_str = input("年龄:").strip()
    record_list.append(age_str)
    phone_str = input("电话:").strip()
    if not phone_str.isdigit():
        print("输入错误，请输入正确的电话号码")
        return False
    else:
        print("phone" in table_records)
        if "phone" in table_records and len( table_records["phone"] ) > 0:
            # 有电话号码，判断输入的电话号码是否是唯一的
            for phone_numver in table_records["phone"]:
                if phone_numver.strip() == phone_str.strip():
                    print("该号码已经存在，请输入别的号码")
                    return False
    record_list.append(phone_str)
    dept_str = input("职业:").strip()
    record_list.append(dept_str)
    enroll_date_str =  time.strftime( "%Y/%m/%d %H:%M:%S" , time.localtime())
    record_list.append(enroll_date_str)
    write_to_csv('staff_table.csv', record_list)
    print("新员工记录创建成功")
    return True

def get_search_condition(sql):
    #将 sql 解析成字典形式
    # sql:  select name,age from staff_table where age > 22
    # sql_dict: {'select': 'name,age', 'table': ' staff_table', 'where': 'age > 22'}
    if  sql.find("select") >= 0:
        if sql.find("table") >= 0:
            if sql.find("where") >= 0 :
                sql_re = re.search("select\s(?P<select>.*)\sfrom(?P<table>.*)\s+where\s+(?P<where>.*)", sql, flags=re.I)
            else:
                sql_re = re.search("select\s(?P<select>.*)\sfrom(?P<table>.*)", sql, flags=re.I)
    else:
        sql_re = None
    print("sql_re : %s"%sql_re)

    if  sql_re:
        sql_dict = sql_re.groupdict()
        print("sql_dict : %s" % sql_dict)
        return sql_dict
    else:
        print("查询语句输入错误，请重新输入")
        return None

def where_action(line , where_list , table_msg ):
    # 根据 where 子句找出符合条件的记录
    # print("line:%s"%line)
    res = []
    for i in  range(len(where_list)):
        if type(where_list[i]) is not list:
            res.append(where_list[i])
        else:
            exp_k , opt , exp_v = where_list[i]
            exp = ""
            if opt == "=":
                opt = "=="
            if opt != "like":
                if exp_v.isdigit():
                    exp_v = int(exp_v)
                    exp_k = int(line[table_msg[exp_k]])
                else:
                    exp_k = "'%s'"%line[table_msg[exp_k]]
                    exp_v = "'%s'" % exp_v
                exp = "%s%s%s"%(exp_k , opt , exp_v)
                # print("exp :%s"%exp)
                res.append(str(eval("%s%s%s"%(exp_k , opt , exp_v) )))
            else:
                # print("exp_v : %s"%exp_v)
                # print("line_value : %s" % line[table_msg[exp_k]])
                if exp_v  in  line[table_msg[exp_k]]:
                    res.append("True")
                else:
                    res.append("False")
    # print("res: %s"%res)
    result = eval( (' ').join(res) )
    # print("result:%s"%result)
    return result



def get_records_msg_for_search( sql_dict , where_list ):
    table_msg = get_record_count_and_column_location()
    print("table_msg : %s"%table_msg)
    column_list = sql_dict["select"].split(",")
    for i in range(len(column_list)):
        #去掉多余的空各位
        column =  column_list[i].strip()
        column_list[i] = column

    if len(column_list) == 1:
        #只有一个查询字段
        if column_list[0].find("*")  >= 0:
            #查询 *  ，则查询所有字段
            column_list = ["staffid" , "name","age","phone","dept","enroll_date"]

    print("column_list : %s" % column_list)

    f_rd = open('staff_table.csv', 'r', encoding="utf-8")
    readlines = csv.reader(f_rd)
    record_msg = {}
    count = 0
    for line in readlines:
        if len(line) > 0:
            print_str = ""
            for column_name in column_list:
                print_str += "%-20s"%line[table_msg[column_name]]
            if where_list and count > 0:
                result = where_action(line , where_list  , table_msg )
                if result:
                    print(print_str)
                continue
            print(print_str)
        count += 1
    f_rd.close()
    return record_msg

def three_parse(exp_str):
    # 'age>=22' --> ['age','>=','22']
    key = [">" , "<" , "="]
    res = []
    char = ""
    opt = ""
    tag = False
    for i in exp_str:
        if i not in key:
            if not tag:
                char += i
            else:
                tag = False
                res.append(opt)
                opt = ""
                char += i
        if i in key:
            if not tag:
                tag = True
                res.append(char)
                char = ""
                opt += i
            else:
                opt += i
    else:
        res.append(char)

    # 添加 like 功能
    if len(res) == 1:
        # 有 like
        res = res[0].split("like")
        res.insert(1,"like")
    # print("res: %s"%res)
    return res

def where_parse(where_str):
    # where 子句的解析
    # age >= 22 and dept = "it"' -->  ['age>=22', 'and', 'dept="it"']
    #     -->  [['age','>=','22'], 'and', ['dept', '=' ,'it']]
    print("where_str : %s"%type(where_str))
    where_list = where_str.split(" ")
    print("where_list : %s"%where_list)
    res = []
    key = ["and" , "or","not"]
    char = ""
    for i in where_list:
        if len(i) == 0:
            continue
        if i in key:
            # i为key 当中的逻辑运算符
            if len(char) != 0:
                char = three_parse(char)
                res.append(char)
                res.append(i)
                char = ""
        else:
            char += i
    else:
        char = three_parse(char)
        res.append(char)
    print("res:%s"%res)
    return res

def re_update_sql(sql_str):
    sql_re = re.search("select\s(?P<select>.*)\sfrom(?P<table>.*)\s+where\s+(?P<where>.*)", sql, flags=re.I)
    pass


if __name__ == '__main__':
    item_menus = ("创建员工记录","查询","修改","删除")
    while True:
        for i in range(len(item_menus)):
            print("%s , %s"%(i+1 , item_menus[i]))
        input_item = input("请输入菜单数字编号:   ")
        if input_item.isdigit():
            input_item = int(input_item)
            if input_item == 1:
                create_record()
            elif input_item == 2:
                sql_str = input("请输入要查询的sql 语句 :  ").strip()
                sql_dict = get_search_condition(sql_str)
                if "where" in sql_dict:
                    res_where = where_parse(sql_dict["where"])
                    print("res_where : %s"%res_where)
                else:
                    res_where = None
                if  sql_dict:
                    table_records = get_records_msg_for_search(sql_dict , res_where)
            elif  input_item == 2:
                sql_str = input("请输入要修改的sql 语句 :  ").strip()
                sql_dict = re_update_sql(sql_str)
        else:
            print("请输入数字")






