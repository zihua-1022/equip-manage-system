var inforData;//储存全部json数据
var types, dropdownVal;//选择不同类型数据
var currentNum;//记录这是第几页
var pageNumber;	//总页数


layui.use(['form', 'code'], function () {
    var form = layui.form;
    form.on("select", function (data) {
        dropdownClick(data.value);
    });

});

//初始化页面
$(function getInforData()
{
    $('.active').removeAttr("class",'current');
    $('.out_info').children('a').addClass('active');
    $("#setli").click();//数据管理
});

////重置
function reset() {
    window.location.reload();
}




//展示数据
function showData(typee) {
    $("#checkall").prop("checked",false); 
    $("#mode").empty();
    $('.page').empty();
    $('#header').empty();  
    var content;
    var userManage;
    var imageManage;
    var logsManage;
    userManage='<tr>\
        <th><input type="checkbox" name="jcheck" id="checkall" onclick="clickAll()">\
        </th>\
        <th>I D</th>\
        <th>名 称</th>\
        <th>手 机</th>\
        <th>邮 箱</th>\
    </tr>';

    imageManage='<tr>\
        <th>\
        <input type="checkbox" name="jcheck" id="checkall" onclick="clickAll()">\
        </th>\
        <th>I D</th>\
        <th>名 称</th>\
        <th>数 量</th>\
        <th>时 间</th>\
    </tr>';

    logsManage='<tr>\
        <th>\
        <input type="checkbox" name="jcheck" id="checkall" onclick="clickAll()">\
        </th>\
        <th>I D</th>\
        <th>名 称</th>\
        <th>用户类型</th>\
        <th>手 机</th>\
        <th>时 间</th>\
    </tr>';
    pageNumber = Math.ceil(inforData.length / 4);
    for (let j = 0; j < pageNumber; j++) //2ye
    {
        if (typee == '用户管理') {
            for (let i = 0; i < 4; i++) 
            {
                if ((i + j * 4) < inforData.length)
                {
                  	content ='<tr id="PageNavId' + j + '">\
							<td style="line-height:40px"><input  id="jcheck" name="jcheck" type="checkbox" value="'+ (i + j * 4) + '" onclick="clickOne()">\
							</td>\
							<td contentEditable="false" >'+ inforData[i + j * 4].id + '</td>\
							<td contentEditable="false" >' + inforData[i + j * 4].name + '</td>\
							<td contentEditable="false">' +inforData[i + j * 4].phone + '</td>\
							<td contentEditable="false" >' + inforData[i + j * 4].email + '</td>\
							</td>\
						  </tr>'
                    $("#mode").append(content);
                    
				}                       
            } 
            $('#header').empty(); 
            $("#header").append(userManage);
        }
        else if (typee == '数据管理') {
            for (let i = 0; i < 4; i++) {
                if ((i + j * 4) < inforData.length) {
                    content ='<tr id="PageNavId' + j + '">\
                    <td style="line-height:40px"><input  id="jcheck" name="jcheck" type="checkbox" value="'+ (i + j * 4) + '" onclick="clickOne()">\
                    </td>\
                    <td>' + inforData[i + j * 4].id + '</td>\
                    <td>' +inforData[i + j * 4].name + '</td>\
                    <td>' + inforData[i + j * 4].number + '</td>\
                    <td>' + inforData[i + j * 4].date + '</td>\
                    </td>\
                  </tr>'
             $("#mode").append(content);
            
                }
            }
            $('#header').empty(); 
            $("#header").append(imageManage);
        }
        else if (typee == '日志管理') {
            for (let i = 0; i < 4; i++) {
                if ((i + j * 4) < inforData.length) {
                    content ='<tr id="PageNavId' + j + '">\
                    <td style="line-height:40px"><input  id="jcheck" name="jcheck" type="checkbox" value="'+ (i + j * 4) + '" onclick="clickOne()">\
                    </td>\
                    <td>' + inforData[i + j * 4].id + '</td>\
                    <td>' + inforData[i + j * 4].name + '</td>\
                    <td>' + inforData[i + j * 4].user_type + '</td>\
                    <td>' + inforData[i + j * 4].phone + '</td>\
                    <td>' + inforData[i + j * 4].date + '</td>\
                    </td>\
                  </tr>'
            $("#mode").append(content);
                }
            }
            $('#header').empty(); 
            $("#header").append(logsManage);
        }
        if (j != 0) 
        {          
            var flag1 = "PageNavId" + (j).toString();
            var $trs = $("tr[id="+flag1+"]");
            for(let i=0;i<$trs.length;i++)
            {
                $trs[i].style.display = "none";
            }
                // var flag = "#PageNavId" + (j).toString();
                // $(flag).hide();
        }
    

    }
          
          if ((pageNumber+1) <= 5) 
          {//————————————————————————————————————————————————————
              for (let i = 1; i < (pageNumber+1); i++) 
              {
                  if (i == 1 && (pageNumber+1) != 2) 
                  {
                      var content = '<span id="prev" href="javascript:void(0);" onclick="pageUper()">&laquo;</span>\
                      <span id="num'+i+'" href="javascript:void(0);" onclick="separatePage(' + i + ')">' + i + '</span>';
                      $('.page').append(content);
                  }
                  else if (i == (pageNumber+1)-1 && (pageNumber+1) != 2) 
                  {
                      var content = '<span id="num'+i+'" href="javascript:void(0);" onclick="separatePage(' + i + ')">' + i + '</span>\
                      <span id="next" href="javascript:void(0);" onclick="pageuper()">&raquo;</span>';
                      $('.page').append(content);
                  }
                  else 
                  {
                      $('.page').append('<span id="num'+i+'" href="javascript:void(0);" onclick="separatePage(' + i + ')">' + i + '</span>')
                  }
              }
          } 
          if ((pageNumber+1) > 5) {     //div=col-lg-1 pageNumber变成了pageNumber-1
              var jump = '<div class="layui-inline" style="width:20%;">\
              <input style="height:36px" type="text" id="page_input" placeholder="' + ((pageNumber+1) - 1) + '" autocomplete="off" class="layui-input">\
              </div>\
              <button style="height:36px" class="layui-btn layui-btn-sm" onclick="jumpPage()"  type="button">Go!</button>';
              var up=  '<span id="prev" href="javascript:void(0);" onclick="pageUper()">&laquo;</span>'
      
              var down= ' <span id="next" href="javascript:void(0);" onclick="pageDowner()">&raquo;</span> '
                     
               $('.page').append(up);
              $('.page').append('<span id="num1" href="javascript:void(0);" onclick="separatePage(1)">1</span>');
              $('.page').append('<span id="num2" href="javascript:void(0);" onclick="separatePage(2)">2</span>');
              $('.page').append('<span id="num" href="javascript:void(0);">...</span>');
              $('.page').append('<span id="num'+ ((pageNumber+1) - 1) +'" href="javascript:void(0);" onclick="separatePage(' + ((pageNumber+1) - 1) + ')">' + ((pageNumber+1) - 1) + '</span>')
              $('.page').append(down);
              $('.page').append(jump);
          }
    
          separatePage(1);//————————————————————————————————————————————————————————————————————————————————————
      
}


//下拉框事件
function dropdownClick(typee) {
    dropdownVal = typee;
    $('#time_collection').val('');
    getData(typee);
    // $('#setli').val(typee);
}

//获取数据
function getData(typee) {
    if (typee == '数据管理') {
        $.getJSON("https://2v595i1604.zicp.vip/get_imagedata/", function (imageData) {
            $('#page').empty();
            inforData = imageData;
            showData(typee);//展示数据
        });
    }
    else if (typee == '用户管理') {
        $.getJSON("https://2v595i1604.zicp.vip/get_userdata/", function (userData) {
            $('#page').empty();
            inforData = userData;
            showData(typee);//展示数据 
        });
    }
    else if (typee == '日志管理') {
        $.getJSON("https://2v595i1604.zicp.vip/get_logsdata/", function (logsData) {
            $('#page').empty();
            inforData = logsData;
            showData(typee);//展示数据
        });
    }
}

//时间值改变触发事件
$(document).ready(function () {
    layui.use('laydate', function searchTime(){
        var laydate = layui.laydate;
        //执行一个laydate实例
        laydate.render({
        elem: '#time_collection' ,//指定元素
        done: function(date){ 
            var time = date
            if (dropdownVal == '数据管理') {
                types = 'upload_img';
                $.getJSON("https://2v595i1604.zicp.vip/searchtime/", { time: time, types: types }, function (data) {
                    $('.page').empty();
                    inforData = data;
                    showData(dropdownVal);//展示数据
                });
            }
            else if (dropdownVal == '用户管理') {
                types = 'wx_user';
                $.getJSON("https://2v595i1604.zicp.vip/searchtime/", { time: time, types: types }, function (data) {
                    $('.page').empty();
                    inforData = data;
                    showData(dropdownVal);//展示数据
                });
            }
            else if (dropdownVal == '日志管理') {
                types = 'logs';
                $.getJSON("https://2v595i1604.zicp.vip/searchtime/", { time: time, types: types }, function (data) {
                    $('.page').empty();
                    inforData = data;
                    showData(dropdownVal);//展示数据
                    // console.log(types)
                });
            }
        }
        });
    });
});


// 导出Excel事件 
function sheet2Blob(sheet, sheetName) {
    sheetName = sheetName || 'sheet1';
    var workbook = {
        SheetNames: [sheetName],
        Sheets: {}
    };
    workbook.Sheets[sheetName] = sheet;
    // 生成excel的配置项
    var wopts = {
        bookType: 'xlsx', // 要生成的文件类型
        bookSST: false, // 是否生成Shared String Table，官方解释是，如果开启生成速度会下降，但在低版本IOS设备上有更好的兼容性
        type: 'binary'
    };
    var wbout = XLSX.write(workbook, wopts);
    var blob = new Blob([s2ab(wbout)], { type: "application/octet-stream" });
    // 字符串转ArrayBuffer
    function s2ab(s) {
        var buf = new ArrayBuffer(s.length);
        var view = new Uint8Array(buf);
        for (let i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
        return buf;
    }
    return blob;
}

function openDownloadDialog(url, saveName) {
    if (typeof url == 'object' && url instanceof Blob) {
        url = URL.createObjectURL(url); // 创建blob地址
    }
    var aLink = document.createElement('a');
    aLink.href = url;
    aLink.download = saveName || ''; // HTML5新增的属性，指定保存文件名，可以不要后缀，注意，file:///模式下不会生效
    var event;
    if (window.MouseEvent) event = new MouseEvent('click');
    else {
        event = document.createEvent('MouseEvents');
        event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    }
    aLink.dispatchEvent(event);
}

//信息导出事件
function inforExport() {
    statistical();
    var inforArr = [];
    for (let i = 0; i < IDArr.length; i++) {
        inforArr.push(inforData[IDArr[i]]);
    }
    console.log(inforArr);
    var sheet = XLSX.utils.json_to_sheet(inforArr);
    openDownloadDialog(sheet2Blob(sheet), '数据信息.xlsx');
}