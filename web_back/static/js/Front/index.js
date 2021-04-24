//加载页面时执行函数检验用户是否已在当前浏览器登录过（即用户自动登录）
$(function checkLogIn(){
    var userid=$.cookie("userid");
    layui.use('layer', function(){
        var layer = layui.layer;
        if(userid!=null && userid!="")
        {
            $.ajax({
            type: "POST",
            url: "https://2v595i1604.zicp.vip/check_users/",
            data: { userid: userid},
            success:function(data)
            {
                if(data==2)
                {
                    layer.alert('已经登录！', {
                        skin: 'layui-layer-molv' //样式类名layui-layer-molv
                        ,closeBtn: 0
                    }, function(){
                        location.href='/admin_manage/';
                    });

                }
            }
            });
        }
    });
});