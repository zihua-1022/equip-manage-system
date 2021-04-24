var userData;	//用户数据
// var changeStatus=false;	//判断当前页面是否改为可修改状态
var pageNumber;	//总页数
var currentNum;	//记录这是第几页

//按时间查找信息
$(document).ready(function() {
	layui.use('laydate', function searchTime(){
		var laydate = layui.laydate;
		//执行一个laydate实例
		laydate.render({
		elem: '#time_collection' ,//指定元素
		done: function(date){    //根据时间查找信息
				web='search_time'//时间查找网址
				types = 'wx_user';
				var time = date;
				$.ajax({
					type: 'GET',
					url: 'https://2v595i1604.zicp.vip/search_time/',
					dataType: 'json',
					data: { time: time,types:types },
					success: function (res) {
						userData= res;
						showData();
					}
				});
			}
		});
	});

	
});



//展示数据
function showData() 
{
	$("#checkall").prop("checked",false); 
    $("#mode").empty();
    $('.page').empty(); 
    var content;
    pageNumber = Math.ceil(userData.length / 4); //总页数
    for (let j = 0; j < pageNumber; j++) //2ye
    {
		for (let i = 0; i < 4; i++) 
		{
			if ((i + j * 4) < userData.length)
			{
				content ='<tr id="PageNavId' + j + '">\
						<td><input id="jcheck" type="checkbox" onclick="clickOne()" name="jcheck" value="'+userData[i + j * 4][0]+'">\
						</td>\
						<td name="userId" id="userId'+userData[i + j * 4][0]+'">' + userData[i + j * 4][0] + '</td>\
						<td name="userName" id="userName'+userData[i + j * 4][0]+'">' + userData[i + j * 4][1] + '</td>\
						<td name="userPhone" id="userPhone'+userData[i + j * 4][0]+'">' + userData[i + j * 4][2] + '</td>\
						<td name="userMail" id="userMail'+userData[i + j * 4][0]+'">' + userData[i + j * 4][3] + '</td>\
						<td><button name="alter_btn" id="alter_btn(' + userData[i + j * 4][0] + ')"class="layui-btn layui-btn-radius layui-btn-danger"\
						onclick="changeData(' + userData[i + j * 4][0] + ')" disabled="disabled" value="修改"><i class="layui-icon">&#xe6b2;</i>修改</button>\
						</td>\
						</tr>';
				$('#mode').append(content);
			}                       
		} 
		if (j != 0) 
		{          
			var flag1 = "PageNavId" + (j).toString();
			var $trs = $("tr[id="+flag1+"]");
			for(let i=0;i<$trs.length;i++)
			{
				$trs[i].style.display = "none";
			}
		}
    }
		if ((pageNumber+1) <= 5) 
		{//————————————————————————————————————————————————————
			for (let i = 1; i < (pageNumber+1); i++) 
			{
				if (i == 1 && (pageNumber+1) != 2) 
				{
					var content = '<span id="prev" href="javascript:;" onclick="pageUper()">&laquo;</span>\
					<span id="num'+i+'" href="javascript:;" onclick="separatePage(' + i + ')">' + i + '</span>';
					$('.page').append(content);
				}
				else if (i == (pageNumber+1)-1 && (pageNumber+1) != 2) 
				{
					var content = '<span id="num'+i+'" href="javascript:;" onclick="separatePage(' + i + ')">' + i + '</span>\
					<span id="next" href="javascript:;" onclick="pageDowner()">&raquo;</span>';
					$('.page').append(content);
				}
				else 
				{
					$('.page').append('<span id="num'+i+'" href="javascript:;" onclick="separatePage(' + i + ')">' + i + '</span>');
				}
			}
		} 
		if ((pageNumber+1) > 5) 
		{     
			var jump = '<div class="layui-inline" style="width:20%;">\
			<input style="height:36px" type="text" id="page_input" placeholder="' + ((pageNumber+1) - 1) + '" autocompvare="off" class="layui-input">\
			</div>\
			<button style="height:36px" class="layui-btn layui-btn-sm" onclick="jumpPage()" id="go_btn" type="button">Go!</button>';
		
			var up= ' <span id="prev" href="javascript:;" onclick="pageUper()">&laquo;</span> ';
			var down=  '<span id="next" href="javascript:;" onclick="pageDowner()">&raquo;</span>';		
			$('.page').append(up);
			$('.page').append('<span id="num1" href="javascript:;" onclick="separatePage(1)">1</span>');
			$('.page').append('<span id="num2" href="javascript:;" onclick="separatePage(2)">2</span>');
			$('.page').append('<span id="num" href="javascript:;">...</span>');
			$('.page').append('<span id="num'+ ((pageNumber+1) - 1) +'" href="javascript:;" onclick="separatePage(' + ((pageNumber+1) - 1) + ')">' + ((pageNumber+1) - 1) + '</span>');
			$('.page').append(down);
			$('.page').append(jump);
		}
      
        separatePage(1);//————————————————————————————————————————————————————————————————————————————————————
        
}


// 添加修改按钮  
function addModBtn()
{
	//循环添加修改按钮
	if ($('#change').val()=='修改数据') 
	{ 
			$("button[name='alter_btn']").removeAttr("disabled");
			$("td[name='userName']").attr("contentEditable", true);
			$("td[name='userPhone']").attr("contentEditable", true);
			$("td[name='userMail']").attr("contentEditable", true);
			$('#change').val('取消修改');
			$("#change").html('<i class="layui-icon">&#x1007;</i>取消修改');		
	}
	else if($('#change').val()=='取消修改') 
	{
		$("button[name='alter_btn']").attr("disabled", true);
		$("td[name='userName']").attr("contentEditable", false);
		$("td[name='userPhone']").attr("contentEditable", false);
		$("td[name='userMail']").attr("contentEditable", false);
		$('#change').val('修改数据');
		$("#change").html('<i class="layui-icon">&#xe631;</i>修改数据');
	}
}

// 修改用户数据
function changeData(num){
	var $ID = $("#userId"+num+"").text();
	var $name = $("#userName"+num+"").text();
	var $email = $("#userMail"+num+"").text();
	var $phone = $("#userPhone"+num+"").text();
	layer.confirm("确认要修改吗，修改后不能恢复", { title: "修改确认" }, function (index) {
		$.ajax({
			type: "GET",
			url: "https://2v595i1604.zicp.vip/change_userdata/",
			dataType: "json",
			data: { id: $ID ,name:$name,email:$email,phone:$phone},
			success:function(feedBack){
				userData=feedBack;     
				$('#change').val('修改数据');
				$("#change").html('<i class="layui-icon">&#xe631;</i>修改数据');
				layer.close(index);
				layer.msg('修改成功！', {
                    time: 2000, //2000ms后自动关闭
                });
				showData();
			},
			error:function(feedBack){
				alert('修改失败');
			}
		});
	});
}

// 根据姓名查找用户
$(function searchName(){
	$("#search").click(function (){
		var $name = $("#search-id").val();
		types='wx_user';
		$.ajax({
			type:"GET",
			url:"https://2v595i1604.zicp.vip/searchdata/",
			data:{name:$name,types:types},
			dataType:"json",
			success:function(searchdata){
				userData=searchdata;				
				$('#date').val('');
				showData();
			},
			error:function(){
				console.log("获取数据失败")
			}
		});
	});
});
	

//删除选中框
$(function delAll(){
	$("#delAll").click(function () {
		statistical();
		types="wx_user";
		// var ischk = $(":checkBox:checked");//获取选中框
		layer.confirm("确认要删除吗，删除后不能恢复", { title: "删除确认" }, function (index) {
			$.ajax({
				type: "POST",
				url: "https://2v595i1604.zicp.vip/delete/",
				dataType: "json",
				data: { 'id': IDArr,types:types },
				traditional: true,
				success: function (res) {
					layer.close(index);
					layer.msg('删除成功！', {
						time: 2000, //2000ms后自动关闭
					});
					userData=res;
					showData();

				}
			});
		});
	});
});


//重置
function reset(){
	$('#time_collection').val('');
	$('#search-id').val('');
	$.ajax({
		type:'GET',
		url:'https://2v595i1604.zicp.vip/getuserdata/',
		dataType:'json',
		success:function(data){
			userData=data;
			showData();
		}
	});
}

//初始化获取用户数据
$(function getData(){
	reset();
});



	