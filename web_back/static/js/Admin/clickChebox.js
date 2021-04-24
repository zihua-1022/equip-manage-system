// document.write("<script language=javascript src='/js/iamgemanage.js'></script>");
var clicks=1; //选择单页点击按钮状态
var IDArr=[]; //储存id信息


//选择单页事件
function clickOnePage()
{  
    console.log(currentNum)
    var flag = "#PageNavId" + (currentNum-1);
    if(clicks%2==1){
      $(""+flag+" input[type='checkbox']").prop("checked", true);   //将其value值设置为真true
      $('#checkonepages').text('取消单页');
    }
    if(clicks%2==0){
      console.log('选择');
      $(""+flag+" input[type='checkbox']").prop("checked", false);   //将其value值设置为假
      $('#checkonepages').text('选择单页');
    }
      clicks++;
      var $jcheck = $("input[id=jcheck]");
      $("#checkall").prop("checked", $jcheck.length == $jcheck.filter(":checked").length ? true : false);
}

//主要是用来统计选中的复选框的ID或选中第几行数据
function statistical()
{
    var array = [];
    $.each($("#mode").find("input:checked"), function () {
        array.push($(this).val());
        IDArr=array;
    });
}

//全选事件
function clickAll() 
{
      if ($("#checkall").prop("checked")) // 全选 
      { 
          $("input[name='jcheck']").each(function()   //取当前页面所有name='check_name'的input元素，循环每一个取到的元素,
          {
            $(this).prop("checked", true);   //将其value值设置为真true
          });
          $('#checkonepages').text('取消单页');
          clicks = 0;
      }
      else   // 取消全选 
      { 
          $("input[name='jcheck']").each(function () {
            $(this).prop("checked", false);
          });
          $('#checkonepages').text('选择单页');
          clicks = 1;
      }
}

//单选
function clickOne() 
{
    console.log(44444);
    var flag = "#PageNavId" + (currentNum-1);
    var flag1 = "PageNavId" + (currentNum-1).toString();
    var $trs = $("tr[id="+flag1+"]");
    var $clickCount=$(""+flag+" input[type='checkbox']:checked").length;
    var $jcheck = $("input[id=jcheck]");
    $("#checkall").prop("checked", $jcheck.length == $jcheck.filter(":checked").length ? true : false);
    if($clickCount != $trs.length)
    {
      $('#checkonepages').text('选择单页');
      clicks = 1;
    }
    else
    {
      $('#checkonepages').text('取消单页');
      clicks = 0;
    }
}


$(function(){

  //刷新渲染
  layui.use(['form', 'code'], function () {
    layui.form.render();   
  });  
});
 






