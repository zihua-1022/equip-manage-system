var userID=$.cookie("userid");
//初始化获个人信息
$(document).ready(function personData() {
    $.getJSON("/getuserval/",{userID:userID}, function (data) {
        $('#userName').val(data[0][1]);
        $('#nickName').val(data[0][1]);
        $('#phone').val(data[0][2]); 
        $('#email').val(data[0][3]); 
    }); 
});


$(function(){
    layui.use('layer', function(){
        let layer = layui.layer;   
        $("#getsmscode").click(function () {
            sendCode();
        });
        $("#getphecode").click(function () {
            sendCode();
        });
        
    });   
});
//发送验证码函数
function sendCode(){
    let $codeVerify = $('#verify').val();
    if($codeVerify)
    {
        $.ajax({  
            type: "POST", //用POST方式传输  
            // dataType: "json", //数据格式:JSON  
            url: "/sendcode/", 
            data: {userMail:$codeVerify},  
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
        layer.msg('必填空不能为空！', 
        {
            time: 2000, //2000ms后自动关闭
        });  
    } 
}
  

//修改邮箱
function alterEmail(){
    let $newMail= $("input[name='newEmail']").val();
    let $oldMail = $("input[name='oldEmail']").val();
    let $mailCode= $("input[name='emailCode']").val();
    if(!$oldMail || !$newMail || !$mailCode){
        layer.msg('必填空不能为空！', {
            time: 2000, //2000ms后自动关闭
        }); 
    }

    else{
        $.ajax({
            type: "POST",
            url: "/change_emails/",
            data: { oldMail:$oldMail,newMail:$newMail,mailcode:$mailCode,userID:userID},
            success:function(data){
                if(data==0){
                    layer.msg('修改成功！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    setTimeout(function (){
                        location.href='/personal_cental/'; 
                    }, 2000);
                                     
                }
                else{
                    layer.msg('验证码错误！', {
                    time: 2000, //2000ms后自动关闭
                    });  
                }
            }    
        });
    }
}

//修改电话
function alterPhone(){
    let $oldPhone= $("input[name='oldPhone']").val();
    let $newPhone= $("input[name='newPhone']").val();
    let $mailCode= $("input[name='phoneCode']").val();
    if(!$oldPhone || !$newPhone || !$mailCode){
        layer.msg('必填空不能为空！', {
            time: 2000, //2000ms后自动关闭
        });  
    }

    else{
        $.ajax({
            type: "POST",
            url: "/change_phones/",
            data: { oldPhone:$oldPhone,newPhone:$newPhone,mailcode:$mailCode,userID:userID},
            success:function(data){
                if(data==0){
                    layer.msg('修改成功！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    setTimeout(function (){
                        location.href='/personal_cental/'; 
                    }, 2000);  
                }
                else{
                    layer.msg('验证码错误！', {
                    time: 2000, //2000ms后自动关闭
                    });  
                }
            }    
        });
    }
}

//修改密码
function alterPwd(){
    let $oldPwd= $("input[name='oldPwd']").val();
    let $newPwd= $("input[name='newPwd']").val();
    let $rePwd= $("input[name='rePwd']").val();
    if(!$oldPwd || !$newPwd || !$rePwd){
        layer.msg('必填空不能为空！', {
            time: 2000, //2000ms后自动关闭
        }); 
    }
    else{
        $.ajax({
            type: "POST",
            url: "/change_passwords/",
            data: { oldpwd:$oldPwd,newpwd:$newPwd,userID:userID},
            success:function(data){
                if(data==0){
                    layer.msg('修改成功！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    setTimeout(function (){
                        location.href='/personal_cental/'; 
                    }, 2000);  
                }
                else{
                    layer.msg('验证码错误！', {
                    time: 2000, //2000ms后自动关闭
                    });  
                }
            }    
        });
    }
}