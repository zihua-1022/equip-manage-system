//解析当前url中的参数
function GetRequest() 
{
    var url = window.location.href; 
    if (url.indexOf("=") != -1) //获取url中"?"符后的字串
    {    //判断是否有参数
       var str = url.substr(0); //从第一个字符开始 因为第0个是=号 获取所有除问号的所有符串
       strs = str.split("/");
       strs = strs[4].split("=")   //用等号进行分隔 （因为知道只有一个参数 所以直接用等号进分隔 如果有多个参数 要用&号分隔 再用等号进行分隔）
       eq_inf_ID = strs[1];          //直接弹出第一个参数 （如果有多个参数 还要进行循环的）
       read_flag =strs[0];
      }
}



//分页
function separatePage(page) 
{
    currentNum = page;
    switchPageNum(page,pageNumber)
    for (let i = 0; i < pageNumber; i++) 
    {
        if (i + 1 == page)  //第一页
        {
          
          var flag = "#PageNavId" + (i).toString();
          var flag1 = "PageNavId" + (i).toString();
          var $trs = $("tr[id="+flag1+"]");
          for(let i=0;i<$trs.length;i++)
          {
              $trs[i].style.display = "";
          }

        //     $(flag).show();
        }
        else 
        {
            
            var flag = "#PageNavId" + (i).toString();
            var flag1 = "PageNavId" + (i).toString();
            var $trs = $("tr[id="+flag1+"]");
            for(let i=0;i<$trs.length;i++)
            {
                $trs[i].style.display = "none";
            }
            // $(flag).hide();
        }
    }

    var flag = "#PageNavId" + (currentNum-1);
	  var flag1 = "PageNavId" + (currentNum-1).toString();
    var $trs = $("tr[id="+flag1+"]");
    var $clickCount=$(""+flag+" input[type='checkbox']:checked").length;
    if($clickCount == 0)
    {
      $('#checkonepages').text('选择单页');
      clicks=1;
    }
    if($clickCount == $trs.length)
    {
        $('#checkonepages').text('取消单页');
        clicks=0;
    }
}

//设置当前页数为高亮显示
function switchPageNum(page,pageNumber)
{
    $('.current').removeAttr("class",'current');
    $('#num'+page+'').attr('class','current');
    if(page > 2 && page < pageNumber)
    {
      $('#num').attr('class','current');
    }
 
}

//上一页————————————————————
function pageUper() 
{
  if (currentNum > 1) {
    separatePage(currentNum - 1);
  }

}
//下一页——————————————————————————————————
function pageDowner() 
{
  if (currentNum < pageNumber) {
    separatePage(currentNum + 1);
  } 
    
}

//多页，用来输入框跳转
function jumpPage() 
{
    separatePage($('#page_input').val()*1);
}
