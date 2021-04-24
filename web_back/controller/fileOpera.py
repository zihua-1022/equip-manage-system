from flask import Blueprint,request,render_template,json
from common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor


# 实例化一个蓝图
fileoperaapp=Blueprint('fileoperaapp',__name__,template_folder="../templates",static_folder="../static")


@fileoperaapp.route('/out_info/', methods=['GET', 'POST'])
def out_info():
    if request.method == 'GET':
        return render_template('out_info.html')
    else:
        return ''


## 信息导出按时间查找数据(修改过)
@fileoperaapp.route('/searchtime/')  # 查询数据使用GET请求
def searchtime():
    types = request.args.get('types')
    time = request.args.get('time')
    time = '\'%s\'' % time
    if types == "wx_user":
        sql = 'select * from wx_user where date(date)=%s' % time
    elif types == "upload_img":
        sql='select distinct * from v_userImgs where date(date)=%s' % time
    else:
        sql = 'select *from logs where date(date)=%s' % time
    cursor.execute(sql)
    user_data=cursor.fetchall()
    fields = cursor.description
    column_list = []
    json_list = []
    for i in fields:
        column_list.append(i[0])
    for row in user_data:
        data = {}
        for i in range(len(column_list)):
            data[column_list[i]] = row[i]
        json_list.append(data)
    alldata = json.dumps(json_list, cls=CJsonEncoder)
    return alldata

