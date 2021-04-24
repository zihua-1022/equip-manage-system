//解析当前url中的参数
function GetRequest() 
{
    var url = window.location.href; 
    if (url.indexOf("=") != -1) //获取url中"="符后的字串
    {    //判断是否有参数
       var str = url.substr(0); //从第一个字符开始 因为第0个是=号 获取所有除问号的所有符串
       strs = str.split("/");    
       userEquId = strs[4].split("&");
       userId = userEquId[0].split("=")[1];
       equipCode = userEquId[1].split("=")[1];          //直接弹出第一个参数 （如果有多个参数 还要进行循环的）    
    }
}

//请求保存实验信息到数据库对应的表中
function uploadInfor(){
    let $theme = $('#theme').val();
    let $desc =  $('#desc').val();

    if($theme != '' && $desc != '')
    {
        GetRequest();
        $.ajax({
            type: 'POST',
            url: '/upload_exp_infor/scan_qr',
            data: {theme: $theme,desc:$desc,userID:userId,equipCode:equipCode},  //类型是number   1
            dataType:"text",
            success: function (rec) {
                layer.msg(rec, {
                    time: 2000, //2000ms后自动关闭
                });
                setTimeout(function (){
                    location.href='/';
                }, 2000); 
            },
            error: function () {
                alert('机器启动失败');
            }
        });
    }
    else
    {
        return alert('请填写实验的主题与内容描述');
    }           

}