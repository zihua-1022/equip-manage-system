var getData;
var userID=$.cookie("userid");
var eq_inf_ID;


//当浏览器返回（后退时）刷新被返回的页面
if(window.name != "bencalie"){
    location.reload();
    window.name = "bencalie";
}
else{
    window.name = "";
}

// 获取未读的图片信息
$(function getUnreadData(){
    GetRequest();
    $('.active').removeAttr("class",'current');
    $('.equip_info').children('a').addClass('active');
    $.ajax({
        type:"GET",
        url:"https://2v595i1604.zicp.vip/get_unread_data/",
        dataType:"json",
        data: {userID:userID,equipID:eq_inf_ID},
        success:function(data){
            getData=data;
            dataLength=Math.ceil(data.length)/3;
            imageLength=dataLength;
            addUnreadData(dataLength,data,0);
            getIsData();
        },
        error:function(){
            console.log("获取数据失败");
        }
    });
});


    


// 获取已读的图片信息
function getIsData(){
    $.ajax({
        type:"GET",
        url:"https://2v595i1604.zicp.vip/get_is_data/",
        dataType:"json",
        data: {userID:userID,equipID:eq_inf_ID},
        success:function(data){
            getData=data;
            dataLength=Math.ceil(data.length)/3;
            imageLength=dataLength;
            addUnreadData(dataLength,data,1);
        },
        error:function(){
            console.log("获取数据失败");
        }
    });
};


//用于展示已读和未读的图片信息
function addUnreadData(length,data,type){
    var j=0;
    if(type==0){
        $("#unknow_items").empty();
        for (let i = 0; i < length; i++) {
            var li = '<tr>\
                <td class="layui-bg-red">'+ data[j] + '</td>\
                <td class="layui-bg-red">'+ data[j + 2] + '</td>\
                <td class="layui-bg-red">'+ data[j + 1] + '</td>\
                <td><a href="/equip_list/unread_id='+ data[j] + '"  class="layui-btn">查看详细信息</a></td>\
            </tr>';
            $("#unknow_items").append(li);
            j = j + 3;
        } 
    }else if(type==1){
        $("#is_items").empty();
        for (let i = 0; i < length; i++) {
            var li = '<tr>\
                <td class="layui-bg-green">'+ data[j] + '</td>\
                <td class="layui-bg-green">'+ data[j + 2] + '</td>\
                <td class="layui-bg-green">'+ data[j + 1] + '</td>\
                <td><a href="/equip_list/have_read_id='+ data[j] + '"  class="layui-btn">查看详细信息</a></td>\
            </tr>';
            $("#is_items").append(li);
            j = j + 3;
        } 
    }
    
}
