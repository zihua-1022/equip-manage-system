

//当浏览器返回（后退时）刷新被返回的页面
if(window.name != "bencalie"){
    location.reload();
    window.name = "bencalie";
}
else{
    window.name = "";
}

//显示每台设备所在的位置
function searchByStationName(data,num) 
{
    var lngLatArr = [];
    for(let i=0;i<num;i++)
    {
        lngLat = data[i][6].split(',');
        lngLatArr[i] = lngLat;
        var address = data[i][4];//查询的详细地址 
        var point = new BMap.Point(lngLatArr[i][0],lngLatArr[i][1]);
        var equipName = data[i][1];
        markerLab(point,address,equipName);
    }

    function markerLab(point,address){
        var marker = new BMap.Marker(point);
        var label = new BMap.Label(address,{"offset":new BMap.Size(20,-20)});
        var infoWindow = new BMap.InfoWindow(equipName); 
        map.enableScrollWheelZoom();
        map.centerAndZoom(point, 6.5);
        marker.setLabel(label); 
        marker.addEventListener("click",function(){this.openInfoWindow(infoWindow);});
        map.addOverlay(marker);
        map.addControl(new BMap.NavigationControl());   
        map.addControl(new BMap.ScaleControl());   
        map.addControl(new BMap.OverviewMapControl());
                    
        // marker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画
        localSearch.search(address);
    }

}

// 获取设备具体信息
$(function getEquipInfor(){

    $('.active').removeAttr("class",'current');
    $('.equip_info').children('a').addClass('active');
    $.ajax({
        type:"GET",
        url:"https://2v595i1604.zicp.vip/get_equip_detail_data/",
        dataType:"json",
        //async:false, //同步请求，则所有的请求均为同步请求，在没有返回值之前，同步请求将锁住浏览器，用户其它操作必须等待请求完成才可以执行
        success:function(data){
            getEquipNum(data.length);
            addEquipData(data,data.length);
            searchByStationName(data,data.length);

        },
        error:function(){
            console.log("获取数据失败");
        }
    });
});

// 获取设备数量
function getEquipNum(num)
{
    $("#equip_items").empty();
    for (let i = 0; i < num; i++) {
        var j=i+1;
        var equip = '<div style="width:190px;height:240px; position:relative; float:left">\
                <a id="nums_'+i+'" style="float:left" href="/unread_data/equip_id='+j+'">\
                    <img style="height:90%; width:90%; margin:10px;" src="../static/imgs/iswork.png"></img>\
                </a>\
                <p id="equip_name'+i+'">设备名称</P>\
                <p id="equip_adr'+i+'">设备地址</P>\
                <p id="equip_code'+i+'">设备识别码</P>\
                <p class="work_status'+i+'"></p>\
            </div>';
            $("#equip_items").append(equip);
    }
    getUnreadData(num);
}



// 获取所有设备对应的未读消息的数量
function getUnreadData(num){
    let userID=$.cookie("userid");
    $.ajax({
        type:"GET",
        url:"https://2v595i1604.zicp.vip/get_equip_data/",
        dataType:"json",
        data: {userID:userID},
        //async:false, //同步请求，则所有的请求均为同步请求，在没有返回值之前，同步请求将锁住浏览器，用户其它操作必须等待请求完成才可以执行
        success:function(data){
            addUnreadData(data,num);
        },
        error:function(){
            console.log("获取数据失败");
        }
    });
}


//用于在所有设备的右上角显示未读消息的数量
function addUnreadData(data,num){
    for(let i=0;i<=num;i++){
        if (data[i] > 0) {
            var infor = '<i class="count" style="border-radius:11px 11px 11px 0;color:#fff; height:27px; width:27px; line-height:27px; position:absolute; top:2px; left:155px; background-color:#e60012">' + data[i] + '</i>';
            $("#nums_"+i+"").append(infor);              
        }
    }
    
}

//用于显示设备名称和设备地址
function addEquipData(data,num){
    for(let i=0;i<num;i++){
        $("#equip_name"+i+"").text("设备名称：" + data[i][1]) + "";
        $("#equip_adr"+i+"").text("设备地址：" + data[i][4]) + "";
        $("#equip_code"+i+"").text("设备识别码：" + data[i][8]) + "";
        if(data[i][3] == 1)
        {
            var status = '<i class="layui-icon layui-icon-circle" style="font-size: 10px; color:#00a500"></i>&nbsp;正在工作';
        }
        else
        {
            var status = '<i class="layui-icon layui-icon-circle" style="font-size: 10px; color:#FF0000"></i>&nbsp;已关机';
        }
        $(".work_status"+i+"").append(status);
    }
    
   
}


