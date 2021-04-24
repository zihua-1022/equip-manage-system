var nowID=0;
var IMAGE_LENGTH;
var userID=$.cookie("userid");
var eq_inf_ID;
var read_flag;

// 获取用户点击查看的图片数据
$(function getUserData(){
    GetRequest();
    $('.active').removeAttr("class",'current');
    $('.equip_info').children('a').addClass('active');
    $.ajax({
        type:"GET",
        url:"https://2v595i1604.zicp.vip/del_unread_data/",
        dataType:"json",
        data:{userID:userID,inforID:eq_inf_ID,read_flag:read_flag},
        success:function(data){
            IMAGE_LENGTH=Math.ceil(data.length);
            addUnreadData(IMAGE_LENGTH,data);
        },
        error:function(){
            console.log("获取数据失败");
        }
    });
});

// 渲染未读图片及其信息
function addUnreadData(length,data){
    $("#image_li").empty();
    for(let i=0;i<length;i++){
        // var j=i+1;
        var li='<li id="li'+i+'" style="display:none;"><img src="../'+data[i][2]+'" alt=""></li>';
        $("#image_li").append(li);
    }
    $("#image_title").append(data[0][1]);
    $("#image_desc").append(data[0][0]);
    var imageUrl='../'+data[0][2]+'';
    var img=new Image();

    img.src=imageUrl;
    img.onload=function(){
        var w=img.width;
        var h=img.height;
    }

    $("#li"+nowID+"").css('display','inline');
}

// 下一张图片显示
function afterShow(){
    $("#li"+nowID+"").css('display','none');
    if(nowID==IMAGE_LENGTH-1){
        nowID=0;
    }
    else if(nowID<IMAGE_LENGTH-1){
        nowID=nowID+1;
    }
    $("#li"+nowID+"").css('display','inline');
}

// 前一张图片显示
function beforeShow(){
    $("#li"+nowID+"").css('display','none');
    if(nowID==0){
        nowID=IMAGE_LENGTH-1;
    }
    else if(nowID>0){
        nowID=nowID-1;
    }
    $("#li"+nowID+"").css('display','inline');
}



