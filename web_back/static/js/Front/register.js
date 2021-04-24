// 解析当前URL的参数
$(function GetRequest() 
{
    let url = window.location.href; 
    strs = url.split("/");  
    regType = strs[5];          //直接弹出第一个参数 （如果有多个参数 还要进行循环的）    
    
    $('#user_login').attr('href','/admin_login/'+regType)
});

//用户注册
function register()
{
    var $userName = $("input[name='name']").val();
    var $pwd= $("input[name='passwd']").val();
    var $repwd= $("input[name='repasswd']").val();
    var $mailCode = $("input[name='email_code']").val();
    var $userPhone = $("input[name='phone']").val();
    var $userMail = $("#email").val()+$("#email_postfix").val();
    // $('#register-confirm').addClass("disabled")
    // $('#register-confirm').attr("disabled","disabled")
    let userName = checkUserName();
    let userPhone = checkPhone();
    let repwd = ConfirmPassword();
    let pwd = checkPassword();
    console.log(userName,userPhone,repwd,pwd)
    if( !$userName || !$pwd || !$repwd  || !$userMail || !$mailCode || !$userPhone)
    {
        // $('#register-confirm').removeClass("disabled")
        // $('#register-confirm').removeAttr("disabled")
        layer.msg('必填项不能为空！', {
            time: 2000, //2000ms后自动关闭
        });
    }
    else if(!userName || !userPhone || !repwd || !pwd)
    {
        layer.msg('信息填写不符合规范！', {
            time: 2000, //2000ms后自动关闭
        });
    }
    else
    {
        $.ajax({
            type: "POST",
            url: "/register/user_name="+$userName,
            data: { 
                userName:$userName,
                pwd:$pwd,
                userMail:$userMail,
                userPhone:$userPhone,
                mailCode:$mailCode
            },
            success:function(data)
            {
                if(data==2)
                {
                    layer.msg('该用户已经注册！', {
                        time: 2000, //2000ms后自动关闭
                    }); 
                    setTimeout(function (){
                        location.reload();
                    }, 2000);                                    
                }
                 else if(data==1)
                {
                    layer.msg('注册成功！', {
                        time: 2000, //2000ms后自动关闭
                    });
                    setTimeout(function (){
                        location.href='/admin_login/'+regType;
                    }, 2000);

                }
                else
                {
                    layer.msg('注册失败，验证码错误！<br>2s后自动跳转注册页面...', {
                        time: 2000, //2000ms后自动关闭
                    });
                    setTimeout(function (){
                        location.reload();
                    }, 2000);                  
                }  
            }
        }); 
    }     
}


$(document).keyup(function(event){ 
    if(event.keyCode ==13){ 
        console.log("执行回车");
        $("#register-confirm").trigger("click"); 
    } 
});

