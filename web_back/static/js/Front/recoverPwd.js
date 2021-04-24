//找回帐号密码
function loss()
{
    var $email = $("input[name='email']").val();
    if($email==""){
    pass;
    }

    else{
        $.ajax({
            type: "POST",
            url: "https://2v595i1604.zicp.vip/findloss/",
            data: { userMail:$email},
            success:function(data){
                if(data==1)
                {
                    layer.msg('发送成功，请打开邮箱查看！', {
                        time: 2000, //2000ms后自动关闭
                        });
                }                
                else
                {
                    layer.msg('邮箱填写错误！', {
                        time: 2000, //2000ms后自动关闭
                        });
        
                } 
               
            },
            error:function(data){
                layer.msg('发送失败，请重新发送！', 
                {
                    time: 2000, //2000ms后自动关闭
                });        
            }
              
        });
    }
}
