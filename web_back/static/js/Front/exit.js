var userid=$.cookie("userid");
//渲染登录者的用户名
username=localStorage.username;
$(function(){
    $('#admin').append(username);
})


//退出登录
function exits()
{ 
    try
    {
                  
        $.cookie("userid","",{expires:7,path:'/'});
        $.ajax({
        type: "POST",
        url: "https://2v595i1604.zicp.vip/clearkey/",
        data: {userid:userid}
        });
        layer.msg('退出成功！', {
        time: 2000, //2000ms后自动关闭
        });
        setTimeout(function (){
            location.href='/';
        }, 2000); 
    }
    catch(err)
    {
        alert("错误");
        var script=document.createElement("script");
        script.type="text/javascript";
        script.src='https://cdn.bootcdn.net/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.js';
        document.getElementsByName("head")[0].appendChild(script);
        script.onload=function(){
        $.cookie("userid","",{expires:7,path:'/'});
        location.href='/user_manage/';

        }
    }
}
