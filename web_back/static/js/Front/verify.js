//发送验证码函数
$(function(){
    layui.use('layer', function(){
        var layer = layui.layer;   
    $("#email_verify").click(function () {
        var $mail = $("#email").val();
        var $userMail = $("#email").val()+$("#email_postfix").val();
        if($mail)
        {
            time($("#email_verify"));
            $.ajax({  
                type: "POST", //用POST方式传输  
                // dataType: "json", //数据格式:JSON  
                url: "/sendcode/", 
                data: {userMail:$userMail},  
                success: function ()
                {  
                    layer.msg('发送成功，请打开邮箱查看！', 
                    {
                        time: 2000, //2000ms后自动关闭
                    });                
                } ,
                error: function () 
                { 
                    layer.msg('发送失败，请重新发送！', 
                    {
                        time: 2000, //2000ms后自动关闭
                    });  
                }
                    
            });  
        }
        else
        {  
            layer.msg('邮箱不能为空！', 
            {
                time: 2000, //2000ms后自动关闭
            });  
        }  
    });
    });   
})

var WAIT = 120;
//timer处理函数 
function time(o) 
{
    if (WAIT == 0) 
    {
        o.removeAttr("disabled");
        o.text("重新发送");
        WAIT = 120;
    } 
    else 
    {
        o.attr("disabled", "disabled");
        o.text("(" + WAIT + ")");
        WAIT--;
        setTimeout(function () {
            time(o)
        },1000)
    }
}

//检验用户名的合法性   
function checkUserName()
{ 
    // $('#nameErr').css({display : 'block'}).fadeIn();
var username = document.getElementById('username'); 
var errname = document.getElementById('nameErr'); 
var pattern = /^[\u4e00-\u9fa5\a-zA-Z0-9_-]{2,6}$/;  //用户名格式正则表达式：用户名要2-6位 
if(username.value.length == 0){ 
    errname.innerHTML="用户名不能为空" 
    errname.className="error" 
    return false; 
    } 
if(!pattern.test(username.value)){ 
    errname.innerHTML="用户名不合规范" 
    errname.className="error" 
    return false; 
    } 
    else{ 
    errname.innerHTML="OK" 
    errname.className="success"; 
    return true; 
    } 

} 

//检验密码的合法性   
function checkPassword(){ 
var userpasswd = document.getElementById('passwd'); 
var errPasswd = document.getElementById('passwordErr'); 
var pattern = /^\w{4,8}$/; //密码要在4-8位 
if(userpasswd.value.length == 0){ 
    errPasswd.innerHTML="密码不能为空" 
    errPasswd.className="error" 
    return false; 
    } 
if(!pattern.test(userpasswd.value)){ 
    errPasswd.innerHTML="密码不合规范" 
    errPasswd.className="error" 
    return false; 
    } 
    else{ 
    errPasswd.innerHTML="OK" 
    errPasswd.className="success"; 
    return true; 
    } 
} 

//确认密码 
function ConfirmPassword(){ 
var userpasswd = document.getElementById('passwd'); 
var userConPassword = document.getElementById('repasswd'); 
var errConPasswd = document.getElementById('conPasswordErr'); 
if((userpasswd.value)!=(userConPassword.value) || userConPassword.value.length == 0){ 
    errConPasswd.innerHTML="前后密码不一致" 
    errConPasswd.className="error" 
    return false; 
    } 
    else{ 
    errConPasswd.innerHTML="OK" 
    errConPasswd.className="success"; 
    return true; 
    }    
} 

//检验手机号的合法性  
function checkPhone(){ 
var userphone = document.getElementById('phone'); 
var phonrErr = document.getElementById('phoneErr'); 
var pattern = /^1[0-9]{10}$/; //验证手机号正则表达式 (不验证第二位)
if(userphone.value.length == 0){ 
    phonrErr.innerHTML="手机号码不能为空" 
    phonrErr.className="error" 
    return false; 
    } 
if(!pattern.test(userphone.value)){ 
    phonrErr.innerHTML="手机号码不合规范" 
    phonrErr.className="error" 
    return false; 
    } 
    else{ 
    phonrErr.innerHTML="OK" 
    phonrErr.className="success"; 
    return true; 
    } 
} 