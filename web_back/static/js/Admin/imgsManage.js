var imageData;  //储存全部图片数据
var currentNum; //记录这是第几页
var pageNumber;	//总页数



// function review_imgs(){
//   var layer = layui.layer;
//   for (var i = 0; i < imageData.length; i++) 
//   {
//       var j=i+1;
//       var img = '<img class="banner_img' +j+ '" src="../' + imageData[i] + '" >' //../可以去掉
//     layer.open({
//       type:1,  //Page层类型
//       area: ['1000px', '600px'],
//       shift: 2,
//       shade:0,
//       title:'查看图片',
//       shadeClose:true,
//       content:img
//     });
//   }
// }

$(document).ready(function () {
  //按时间查找信息
  layui.use('laydate', function searchTime(){
    var laydate = layui.laydate;
    //执行一个laydate实例
    laydate.render({
    elem: '#date' ,//指定元素
    done: function(date){    //根据时间查找信息
        web="search_time";//时间查找网址
        types="upload_img";
        var time = date;
        $.ajax({
          type: "GET",
          url: "https://2v595i1604.zicp.vip/search_time/",
          dataType: "json",
          data: { time: time,types:types },
          success: function (res) {
            $("#mode").empty();
            $(".page div").remove();
            $("#ID").val('');
            imageData = res;
            showData();
          }
        });
      }
    });
    
  });

    

  //重置
  $("#reset").click(function reset(){
    web="getimagedata";
    $("#date").val("");
    $("#ID").val('');
    $.ajax({
      url: "https://2v595i1604.zicp.vip/getimagedata/",
      type: "get",
      dataType: "json",
      success: function (res) {
        $(".page div").remove();
        imageData = res;
        showData();
      }
    });
  });
  //关闭弹出层和遮罩层
  $(".banner_img").click(function closePopover() {
    $(".frame").fadeOut();
    $(".fill").fadeOut();
  })
  // 搜索名字
  $("#search").click(function searchName() {
    types="upload_img";
    var name = $("#ID").val();
    $.ajax({
      type: "GET",
      url: "https://2v595i1604.zicp.vip/searchdata/",
      dataType: "json",
      data: { name: name,types:types },
      success: function (res) {
        $('#date').val('');
        imageData = res;
        showData();
      },
      error: function () {
        console.log("获取数据失败");
      }
    });
  });


  // 删除图片
  $("#delAll").click(function delAll() {
    statistical();

    types="upload_img";
    var ischk = $(":checkBox:checked");//获取选中框
    layer.confirm("确认要删除吗，删除后不能恢复", { title: "删除确认" }, function (index) {
      $.ajax({
        type: "POST",
        url: "https://2v595i1604.zicp.vip/delete/",
        dataType: "json",
        data: {'id':IDArr,types:types},
        traditional:true,
        success: function (res) {
          layer.close(index);
          layer.msg('删除成功！', {
            time: 2000, //2000ms后自动关闭
          });
          ischk.each(function () {
            $(this).parent().parent().remove();
          })
        },
        error: function (res) {
          alert("删除失败");
        }
      });
    });
  });
  
  bannerNumber();//banner页数高亮显示

  timer = setInterval(autoReplaceBanner, speed * 1000);//banner切换计时器
  
});


//查看图片
function reviewImages(num){
    var ID=num;
    setDivCenter(".frame");
    $(".fill").fadeIn();
    
    $.ajax({
      type: "GET",
      url: "https://2v595i1604.zicp.vip/search_image/",
      dataType: "json",
      data: { id: ID },
      success: function (res) {
        $(".banner_img").empty();
        for (let i = 0; i < res.length; i++) 
        {
          var j=i+1;
          var img = '<img class="banner_img' +j+ '" src="../' + res[i][2] + '" >'; //../可以去掉
          $(".banner_img").append(img);
        }
          loads();
      },
      error: function (res) {
        alert("图片请求失败");
      }
    });
 
}

// 下载图片数据
function exportTxt(num) 
{
  var ID=num;
    $.ajax({
      type: "GET",
      url: "/export_id/",
      dataType: "json",
      data: { id: ID },
      success: function (res) {
        alert("Loading...");
      },
      error: function (data) {
        alert("下载数据失败",data);
      }
    });
}


$(function getData(){
  $("#reset").click();

});

//展示数据
function showData() 
{
console.log(imageData)
    $("#checkall").prop("checked",false); 
    $("#mode").empty();
    $('.page').empty(); 
    var content;
    var number;
    pageNumber = Math.ceil(imageData.length / 4);
    for (let j = 0; j < pageNumber; j++) //2ye
    {
        for (let i = 0; i < 4; i++) 
        {
            if ((i + j * 4) < imageData.length)   //onchange=chkChange('+i+')name="jcheck'+i+'"  bu id="see'+i+'" onclick="reviewImages('+i+')"
            {
              if(imageData[i + j * 4][8] == 0 || imageData[i + j * 4][8] == null)
              {
                number = imageData[i + j * 4][3];
              }
              else
              {
                number = imageData[i + j * 4][3] / 2;
              }
              content ='<tr id="PageNavId' + j + '">\
                  <td><input id="jcheck" type="checkbox" onclick="clickOne()" name="jcheck" value="'+imageData[i + j * 4][1]+'">\
                  </td>\
                  <td>' + imageData[i + j * 4][1] + '</td>\
                  <td>' + imageData[i + j * 4][0] + '</td>\
                  <td>' + number + '</td>\
                  <td>' + imageData[i + j * 4][4] + '</td>\
                  <td><button type="button" id="see'+imageData[i + j * 4][1]+'" onclick="reviewImages('+imageData[i + j * 4][1]+')"  class="layui-btn layui-btn-normal">查看</button>&emsp;\
                  <a style="background-color: #009688;" type="button" id="export'+imageData[i + j * 4][1]+'" href="/export_data/content=实验数据&txtid=/'+imageData[i + j * 4][1]+'" class="layui-btn layui-btn-normal">下载</a>\
                  </td>\
                </tr>';
              // $("#PageNavId" + j).append(content);
              $("#mode").append(content);
              if(imageData[i + j * 4][8] == 0 || imageData[i + j * 4][8] == null)
              {
                $('#export'+imageData[i + j * 4][1]+'').css('display','none');
              }
              
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
            // var flag = "#PageNavId" + (j).toString();
            // $(flag).hide();
        }
    } 

    if ((pageNumber+1) <= 5) {//————————————————————————————————————————————————————
        for (let i = 1; i < (pageNumber+1); i++) {
            if (i == 1 && (pageNumber+1) != 2) {
                var content = '<span id="prev" href="javascript:void(0);" onclick="pageUper()">&laquo;</span>\
                <span id="num'+i+'" href="javascript:void(0);" onclick="separatePage(' + i + ')">' + i + '</span>';
                $('.page').append(content);
            }
            else if (i == (pageNumber+1)-1 && (pageNumber+1) != 2) {
                var content = '<span id="num'+i+'" href="javascript:void(0);" onclick="separatePage(' + i + ')">' + i + '</span>\
                <span id="next" href="javascript:void(0);" onclick="pageDowner()">&raquo;</span>';
                $('.page').append(content);
            }
            else {
                $('.page').append('<span id="num'+i+'" href="javascript:void(0);" onclick="separatePage(' + i + ')">' + i + '</span>');
            }
        }
    }
    if ((pageNumber+1) > 5) {     //div=col-lg-1 pagenum变成了pagenum-1
        var jump = '<div class="layui-inline" style="width:20%;">\
        <input style="height:36px" type="text" id="page_input" placeholder="' + ((pageNumber+1) - 1) + '" autocompvare="off" class="layui-input">\
        </div>\
        <button style="height:36px" class="layui-btn layui-btn-sm" onclick="jumpPage()" id="go_btn" type="button">Go!</button>';
        var up=  '<span id="prev" href="javascript:void(0);" onclick="pageUper()">&laquo;</span>';

        var down= ' <span id="next" href="javascript:void(0);" onclick="pageDowner()">&raquo;</span> ';
                
        $('.page').append(up);
        $('.page').append('<span id="num1" href="javascript:void(0);" onclick="separatePage(1)">1</span>');
        $('.page').append('<span id="num2" href="javascript:void(0);" onclick="separatePage(2)">2</span>');
        $('.page').append('<span id="num" href="javascript:void(0);">...</span>');
        $('.page').append('<span id="num'+ ((pageNumber+1) - 1) +'" href="javascript:void(0);" onclick="separatePage(' + ((pageNumber+1) - 1) + ')">' + ((pageNumber+1) - 1) + '</span>');
        $('.page').append(down);
        $('.page').append(jump);
    }

    separatePage(1);//————————————————————————————————————————————————————————————————————————————————————
  
}
      

//图片弹出层
function setDivCenter(divName) {
  var top = ($(window).height() - $(divName).height()) / 2;
  var left = ($(window).width() - $(divName).width()) / 2;
  var $scrollTop = $(document).scrollTop();
  var $scrollLeft = $(document).scrollLeft();
  $(divName).css({ position: 'absolute', 'top': top + $scrollTop, left: left + $scrollLeft }).fadeIn();
}

var banners = 1;//banner显示的第一幅画面1~banner_max范围内任意选择
var speed = 500;//每5秒切换一次
var BANNER_COUNT;//banner总数
var timer;//计时器对象

//img标签后直接调用运行
function loads() {
  var $imgNumber = $(".banner_img").children("img").length;//获取img标签的总数量
  BANNER_COUNT = $imgNumber;

  //隐藏所有banner
  for (let i = 1; i <= BANNER_COUNT; ++i) 
  {
    $(".banner_img" + i).fadeTo(100, 0);
  }

  $(".banner_img" + banners).fadeTo(100, 1);//显示设置的第一张banner
  
  var numbersSpan = "";
  if ($imgNumber <= 10)
  {
    for (let i = 1; i <= $imgNumber; ++i) 
    {
      numbersSpan += '<span class="num' + i + '" onclick="manualReplaceBanner(' + i + ')">' + i + '</span>'; //循环赋值到字符串
    }
    $(".numbers").html(numbersSpan);//设置对应banner的数字
    $(".numbers .num" + banners + "").css("color", "black");
    $(".numbers .num" + banners + "").css("backgroundColor", "white");
  }
  else
  {
    var numbersSpan_1 = "";
    var numbersSpan_2 = "";
    for (let i = 1; i <= 5; ++i) {
      numbersSpan_1 += '<span class="num' + i + '" onclick="manualReplaceBanner(' + i + ')">' + i + '</span>'; //循环赋值到字符串
    }
    for (let j = ($imgNumber-5); j <= $imgNumber; ++j) {
      numbersSpan_2 += '<span class="num' + j + '" onclick="manualReplaceBanner(' + j + ')">' + j + '</span>'; //循环赋值到字符串
    }
    numbersSpan = numbersSpan_1 +'<span class="num">...</span>'+numbersSpan_2;
    $(".numbers").html(numbersSpan);//设置对应banner的数字
    $(".numbers .num" + banners + "").css("color", "black");
    $(".numbers .num" + banners + "").css("backgroundColor", "white");

  }
  



  //自适应修改行高
  var $bannersHeight = $(".banners").height();
  $(".banners").css("line-height", $bannersHeight + "px");


}

//窗口事件修改行高
$(window).resize(function setWindow() {

  var $bannersHeight = $(".banners").height();
  $(".banners").css("line-height", $bannersHeight + "px");

});


//点击左右按钮更换banner
function bannerLeftRight(LorR) {
  var sjs;

  if (LorR == "left") {
    if (banners == 1) {
      sjs = BANNER_COUNT;
    }
    else {
      sjs = banners - 1;
    }
  }
  else {
    if (banners == BANNER_COUNT) {
      sjs = 1;
    }
    else {
      sjs = banners + 1;
    }
  }

  manualReplaceBanner(sjs);
}

//点击数字切换
function manualReplaceBanner(number) {
  var bannerz = banners;

  banners = number;

  if (banners == bannerz) {
    return;
  }

  clearInterval(timer);//停止计时器

  fadeInOut(bannerz, banners);//调用切换函数

  timer = setInterval(autoReplaceBanner, speed * 1000);//banner切换计时器重新启动
}

//自动更换banner
function autoReplaceBanner() {
  var bannerz = banners;

  if (banners == BANNER_COUNT) {
    banners = 1;
  }
  else {
    banners += 1;
  }

  fadeInOut(bannerz, banners);//调用切换函数
}

//淡入淡出效果方法
function fadeInOut(bannerz, banners) {
  var outID = ".banner_img" + bannerz;//淡出标签的ID名
  var $bannerOut = $(outID);//获取淡出对象

  var inID = ".banner_img" + banners;//淡入标签的ID名
  var $bannerIn = $(inID);//获取淡入对象

  $bannerOut.fadeTo(600, 0);//JQuery方法淡出到指定透明度,参数1为速度，参数2为透明度
  $bannerIn.fadeTo(500, 1);//JQuery方法淡入,参数1为速度，参数2为透明度

  bannerNumber();//调用数字颜色更换
}

//banner数字显示样式
function bannerNumber() {
  for (let i = 1; i <= BANNER_COUNT; i++) {
    var numID = ".num" + i;
    var $numObject = $(numID);
    if (banners == i) {
      $numObject.css("color", "black");
      $numObject.css("backgroundColor", "white");
    }
    else {
      $numObject.css("color", "white");
      $numObject.css("backgroundColor", "rgba(0,0,0,0)");
    }
  }
}

// //banner链接跳转
// function link(url, mode = true) {
//   if (mode == true) {
//     window.open(url);
//   }
//   else {
//     window.location.href = url;
//   }
// }









/*props={
    pageCount:30,//总页数
    currentPage:1,//当前页
    perPageNum:5,//每页按钮数(非必须,默认5)
}*/

// function PageNavCreate(id, props) {
//   if (id && props) {
//     this.id = id;
//     this.pageCount = parseInt(props.pageCount),
//       this.currentPage = parseInt(props.currentPage),
//       this.perPageNum = props.perPageNum || 5,
//       this.perPageNum = (this.perPageNum < 3 ? 3 : this.perPageNum);//每页按钮数量最小值不能小于3
//     this.target = document.getElementById(id);
//     this.clickPage = null;
//     this.halfPerPage = 3;

//   } else {
//     console.log("请传入正确参数");
//     return false;
//   }

//   this.target.innerHTML = "";
//   $('<div class="page-nav-inner clearfloat">' +
//     '<ul class="pagination">' +
//     '</ul>' +
//     '<div class="page-input-box">' +
//     '<input type="text" values=""/>' +
//     '<button class="btn-green">Go</button>' +
//     '</div>' +
//     '</div>').appendTo($(this.target));
//   this.pageNavUl = $(this.target).find("ul.pagination");
//   this.pageNavInput = $(this.target).find(".page-input-box");

//   //总页数写入placeholder
//   this.pageNavInput.children('input').val("").attr({ "placeholder": this.pageCount, "max": this.pageCount });

//   //若是总页数小于每页按钮数
//   if (this.pageCount <= this.perPageNum) {
//     this.pageNavUl.html("");
//     $('<li class="page-nav-first">' +
//       '<span href="javascript:void(null)" aria-label="First page" (pageNumber+1)="1" >' +
//       '<span aria-hidden="true">&laquo;</span>' +
//       '</span>' +
//       '</li>' +
//       '<li class="page-nav-prev">' +
//       '<span href="javascript:void(null)" aria-label="Previous" (pageNumber+1)="' +
//       (this.currentPage == 1 ? 1 : (this.currentPage - 1)) +
//       '" >' +
//       '<span aria-hidden="true">&lt;</span>' +
//       '</span>' +
//       '</li>').appendTo(this.pageNavUl);

//     for (var i = 1; i <= this.pageCount; i++) {
//       $('<li class="pageNum" ><span href="javascript:void(null)"  (pageNumber+1)="' + i + '" >' + i + '</span></li>').appendTo(this.pageNavUl);
//       if (i == this.currentPage) {
//         this.pageNavUl.children("li.pageNum").last().addClass('active');
//       }
//     }

//     $('<li class="page-nav-next">' +
//       '<span href="javascript:void(null)" aria-label="Last page"  (pageNumber+1)="' +
//       (this.currentPage == this.pageCount ? this.pageCount : (this.currentPage + 1)) +
//       '" >' +
//       '<span aria-hidden="true">&gt;</span>' +
//       '</span>' +
//       '</li>' +
//       '<li class="page-nav-last">' +
//       '<span href="javascript:void(null)" aria-label="Last page"  (pageNumber+1)="' + this.pageCount + '" >' +
//       '<span aria-hidden="true">&raquo;</span>' +
//       '</span>' +
//       '</li>').appendTo(this.pageNavUl);
//   } else {//总页数大于每页按钮数
//     //重写一遍翻页按钮 START
//     this.pageNavUl.html("");
//     $('<li class="page-nav-first">' +
//       '<span href="javascript:void(null)" aria-label="First page" (pageNumber+1)="1" >' +
//       '<span aria-hidden="true">&laquo;</span>' +
//       '</span>' +
//       '</li>' +
//       '<li class="page-nav-prev">' +
//       '<span href="javascript:void(null)" aria-label="Previous" (pageNumber+1)="' +
//       (this.currentPage == 1 ? 1 : (this.currentPage - 1)) +
//       '" >' +
//       '<span aria-hidden="true">&lt;</span>' +
//       '</span>' +
//       '</li>').appendTo(this.pageNavUl);

//     for (var i = 1; i <= this.perPageNum; i++) {
//       $('<li class="pageNum" ><span href="javascript:void(null)"  (pageNumber+1)="' + i + '" >' + i + '</span></li>').appendTo(this.pageNavUl);
//       if (i == this.currentPage) {
//         this.pageNavUl.children("li.pageNum").last().addClass('active');
//       }
//     }
//     $('<li class="disabled">' +
//       '<span href="javascript:void(null)">...</span>' +
//       '</li>' +
//       '<li class="page-nav-next">' +
//       '<span href="javascript:void(null)" aria-label="Last page"  (pageNumber+1)="' +
//       (this.currentPage == this.pageCount ? this.pageCount : (this.currentPage + 1)) +
//       '" >' +
//       '<span aria-hidden="true">&gt;</span>' +
//       '</span>' +
//       '</li>' +
//       '<li class="page-nav-last">' +
//       '<span href="javascript:void(null)" aria-label="Last page"  (pageNumber+1)="' + this.pageCount + '" >' +
//       '<span aria-hidden="true">&raquo;</span>' +
//       '</span>' +
//       '</li>').appendTo(this.pageNavUl);
//     //重写一遍翻页按钮 END

//     //若是目标页小于每页按钮数的一半/有余数+1,偶数+1
//     this.halfPerPage = parseInt(this.perPageNum / 2) + 1;
//     this.lastHalfPage = this.perPageNum % 2 == 0 ? (this.perPageNum / 2) - 1 : parseInt(this.perPageNum / 2);
//     if (this.currentPage <= this.halfPerPage) {
//       this.pageNavUl.children("li.disabled").show();
//       for (var i = 0; i < this.perPageNum; i++) {
//         this.pageNavUl.children("li.pageNum").eq(i).children('span').attr({ "(pageNumber+1)": i + 1 }).html(i + 1);
//       }
//       this.pageNavUl.children("li.pageNum").removeClass('active').eq(this.currentPage - 1).addClass('active');
//       this.pageNavUl.children("li:last-child").children("span").attr({ "(pageNumber+1)": this.pageCount });
//     } else if (this.currentPage >= (this.pageCount - this.lastHalfPage)) {//若是目标页是倒数每页按钮数一半以内,奇数一半，偶数-1
//       for (var i = 0; i < this.perPageNum; i++) {
//         this.pageNavUl.children("li.disabled").hide();
//         this.pageNavUl.children("li.pageNum").eq(i).children('span').attr({ "(pageNumber+1)": (this.pageCount - this.perPageNum + 1 + i) }).html(this.pageCount - this.perPageNum + 1 + i);
//         if ((this.pageCount - this.perPageNum + 1 + i) == this.currentPage) {
//           this.pageNavUl.children("li.pageNum").removeClass('active');
//           this.pageNavUl.children("li.pageNum").eq(i).addClass('active');
//         }
//       }
//       this.pageNavUl.children("li:last-child").children("span").attr({ "(pageNumber+1)": this.pageCount });
//     } else {
//       this.pageNavUl.children("li.disabled").show();
//       for (var i = 0; i < this.perPageNum; i++) {
//         this.pageNavUl.children("li.pageNum").eq(i).children('span').attr({ "(pageNumber+1)": (this.currentPage - parseInt(this.perPageNum / 2) + i) }).html(this.currentPage - parseInt(this.perPageNum / 2) + i);
//       }
//       this.pageNavUl.children("li.pageNum").removeClass('active').eq(parseInt(this.perPageNum / 2)).addClass('active');
//       //this.pageNavUl.children("li:last-child").attr({"(pageNumber+1)":this.pageCount});
//     }
//   }

// }

// PageNavCreate.prototype.afterClick = function (func) {
//   this.pageNavUl.children('li.pageNum').off("click").on("click", function (event) {
//     if ($(this).hasClass('active') != true) {
//       var clickPage = parseInt($(this).children('span').attr("(pageNumber+1)"));
//       //console.log("pageNum = "+clickPage);
//       //翻页按钮点击后触发的回调函数
//       func(clickPage);
//     } else {
//       return false;
//     }
//   });
//   this.pageNavUl.children('li.page-nav-first').off("click").on("click", function (event) {
//     var clickPage = parseInt($(this).children('span').attr("(pageNumber+1)"));
//     //console.log("prev = "+clickPage);
//     //翻页按钮点击后触发的回调函数
//     func(clickPage);
//   });
//   this.pageNavUl.children('li.page-nav-prev').off("click").on("click", function (event) {
//     var clickPage = parseInt($(this).children('span').attr("(pageNumber+1)"));
//     //console.log("prev = "+clickPage);
//     //翻页按钮点击后触发的回调函数
//     func(clickPage);
//   });
//   this.pageNavUl.children('li.page-nav-next').off("click").on("click", function (event) {
//     var clickPage = parseInt($(this).children('span').attr("(pageNumber+1)"));
//     //console.log("prev = "+clickPage);
//     //翻页按钮点击后触发的回调函数
//     func(clickPage);
//   });
//   this.pageNavUl.children('li.page-nav-last').off("click").on("click", function (event) {
//     var clickPage = parseInt($(this).children('span').attr("(pageNumber+1)"));
//     //console.log("next = "+clickPage);
//     //翻页按钮点击后触发的回调函数
//     func(clickPage);
//   });

//   this.pageNavInput.children('button').off("click").on("click", function (event) {
//     var inputVal = parseInt($(this).siblings('input').val());
//     var inputMax = parseInt($(this).siblings('input').attr("max"));
//     //console.log("button = "+inputVal);
//     if (inputVal && inputVal <= inputMax) {
//       //翻页按钮点击后触发的回调函数
//       func(inputVal);
//     } else {
//       return false;
//     }
//   });
//   this.pageNavInput.children('input').off("keydown").on('keydown', function (event) {
//     if (event.which == 13) {//若是回车
//       var inputVal = parseInt($(this).val());
//       var inputMax = parseInt($(this).attr("max"));
//       //console.log("input = "+inputVal);
//       if (inputVal && inputVal <= inputMax) {
//         //翻页事件触发的回调函数
//         func(inputVal);
//       } else {
//         return false;
//       }
//     }
//   });

// }

