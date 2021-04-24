var twoFA = false;
$ (function (){
    $("input[name='remember']").prop("checked", true);   //将记住我按钮其value值设置为真true
    GetRequest();
});
//解析当前url中的参数
function GetRequest() 
{
    let url = window.location.href; 
    strs = url.split("/");   
    equipCode = strs[4];          //直接弹出第一个参数 （如果有多个参数 还要进行循环的）       
    $('#user_reg').attr('href','/qrcode/equipcode=/'+equipCode)
}


//登录
function logIn()
{
    var $phone_email = $("input[name='phone_email']").val();
    var $password= $("input[name='password']").val();
   

    if(!$phone_email || !$password)
    {
        layer.msg('必填项不能为空！', {
            time: 2000, //2000ms后自动关闭
        });
        return false;    
    }
    else
    {   
        $.ajax({
            type: "POST",
            url: "/user_verify",
            data: {
                userphone: $phone_email,
                password:$password,
                remember_me: $("#remember-me:checked").val()        
            },
            dataType:"json",
            success: function(data)
            {    
                if(data==0)
                {
                    layer.msg('帐号密码错误！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    $("input[name='password']").val('');
                }
                else
                { 
                    layer.msg('核对成功！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    setTimeout(function (){
                        location.href='/write_exp_infor/user_id='+ data +'&equip_id='+ equipCode;
                    }, 2000);                                        
                }      
            }
        }); 
    }     
}


//监听回车键
$(document).keyup(function(event){ 
    if(event.keyCode ==13){ 
        console.log("执行回车");
        $("#login-confirm").trigger("click"); 
    } 
});

