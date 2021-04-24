var twoFA = false;
$ (function (){
    $("input[name='remember']").prop("checked", true);   //将其value值设置为真true
    GetRequest();
});
// 解析当前URL的参数
function GetRequest() 
{
    let url = window.location.href; 
    strs = url.split("/");   
    loginType = strs[4];          //直接弹出第一个参数 （如果有多个参数 还要进行循环的）    
    
    $('#user_reg').attr('href','/admin_register/user/'+loginType)
}

//用户登录
function logIn()
{
    var $phone_email = $("input[name='phone_email']").val();
    var $password= $("input[name='password']").val();
    var $code = $("#2fa-code").val();
   

    if(!$phone_email || !$password)
    {
        layer.msg('必填项不能为空！', {
            time: 2000, //2000ms后自动关闭
        });
        return false;    
    }
    else if(twoFA == true) 
    {
        if (!$("#2fa-code").val())
        {
          return false;
        }
    }
    else
    {
        $.ajax({
            type: "POST",
            url: "/check_user/",
            data: {
                userphone: $phone_email,
                password:$password,
                code:$code,
                remember_me: $("#remember-me:checked").val()        
            },
            dataType:"json",
            success: function(data)
            {
                if(data==0)
                {
                    layer.msg('验证码错误！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    $("#2fa-code").val('');
                    $("img[name='img_code']").click();
                    // $('.login-form-item').hide('500');
                    // $('form').removeClass('was-validated');
                    // $('#2fa-form').show('fast');
                }
                else if(data==1)
                {
                    layer.msg('帐号密码错误！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    $("input[name='password']").val('');
                    // $("input[name='code']").val('');
                    // $("img[name='img_code']").click();
                    // var errorMsg = '密码或邮箱不正确';
                    // if (twoFA == true) 
                    // {
                    //   errorMsg = '两步验证码错误'
                    // }
                    // swal('出错了', errorMsg, 'error');
                }
                else
                {
                    layer.msg('登录成功！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    $.cookie("userid",data[0],{expires:7,path:"/"});
                    localStorage.username = data[1];//储存用户名
                    setTimeout(function (){
                        location.href='/admin_manage/';
                    }, 2000);                                        
                }      
            }
        }); 
    }     
}



$(document).keyup(function(event){ 
    if(event.keyCode ==13){ 
        console.log("执行回车");
        $("#login-confirm").trigger("click"); 
    } 
});

