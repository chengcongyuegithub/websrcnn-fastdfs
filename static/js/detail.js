function initTab() {
    var myTab = document.getElementById("tab"); //整个div
    var myUl = myTab.getElementsByTagName("ul")[0]; //一个节点
    var myLi = myUl.getElementsByTagName("li"); //数组
    var myDiv = myTab.getElementsByClassName("dd"); //数组
    for (var i = 0; i < myLi.length; i++) {
        myLi[i].index = i;
        myLi[i].onclick = function () {
            for (var j = 0; j < myLi.length; j++) {
                myLi[j].className = "off";
                myDiv[j].className = "hide dd";
            }
            this.className = "on";
            myDiv[this.index].className = "show dd";
        }
    }
}
function addTabAndPic(res) {
    if (res['code'] == '200') {
        var newTab = "<li class='off'>" + res['action'] + "</li>";
        $("#tab ul").append(newTab);
        var button="<div class='comparefunctions'><input id='compare' type='button' name='compare' value='比较'/>&nbsp;</div>";
        var temp = "<div class='hide dd' name='pic'>" +
            "<p style='text-align: center;'>图片名称：" + res['name'] + "</p>" +
            "<div id='" + res['id'] + "_" + res['action'] + "' class='showD' style='height: " + res['width'] + "px;width:" + res['height'] + "px '>" +
            "<img src='" + res['url'] + "' class='showP'/><span class=\"delete\" >+</span>"+
            "</div>";
        if(res['action']!='SRCNN')
        {
            temp=temp+button;
        }
        temp+="</div>";
        $("#picContent").append(temp);
        initTab();
    } else {
        alert('图片已经处理过了,请选择其他的操作')
    }
}
window.onload = function () {
    initTab();
};
$(document).ready(function () {
    $("#srcnnfunctions").on('click', '#upscaling', function () {
        if ($("#upscalingMenu").length > 0) {
            return;
        }
        var times = "<select id=\"upscalingMenu\"> \n" +
            "<option value=\"1\">1x</option> \n" +
            "<option value=\"2\">2x</option> \n" +
            "<option value=\"3\">3x</option> \n" +
            "</select> "
        $('#times').append(times)
    })

    $("#srcnnfunctions").on('change', '#upscalingMenu', function () {
        var times = $("#upscalingMenu option:selected").val();
        if (parseInt(times) == 1) {
            return;
        }
       var picid = $("#picid").val();
        $.ajax({
            url: '/upscaling',
            type: 'post',
            dataType: 'json',
            data: JSON.stringify({
                "times": times,
                "picid": picid
            }),
            headers: {
                "Content-Type": "application/json;charset=utf-8"
            },
            contentType: 'application/json; charset=utf-8',
            success: function (res) {
                addTabAndPic(res);
            }
        })
    });

    $("#srcnnfunctions").on('click', '#superresolution', function () {
        var picid = $("#picid").val();
        $.ajax({
            url: '/superresolution',
            type: 'post',
            dataType: 'json',
            data: JSON.stringify({
                "picid": picid
            }),
            headers: {
                "Content-Type": "application/json;charset=utf-8"
            },
            contentType: 'application/json; charset=utf-8',
            success: function (res) {
                addTabAndPic(res);
            }
        })
    })

    $("#picContent").on('click', '#compare', function (e) {
        var picId = $(e.target).parent().parent().children('div').first().attr("id");
        window.open("/compare/" + picId);
    })

    $("#picContent").on('click','.delete',function(e){
      var picId=$(e.target).parent().attr("id");
      var sub=picId.indexOf('_');
      var pictureId=picId.substring(0,sub);
      var pictureAction=picId.substring(sub+1);
      if(pictureAction=='Origin')
      {
          var con=confirm("你选择是原图,点击删除将会删除其所有相关资源");
          if(!con)
          {
              return ;
          }
      }
      $.ajax({
            url: '/delete',
            type: 'post',
            dataType: 'json',
            data: JSON.stringify({
                pictureId:pictureId,
                pictureAction:pictureAction
            }),
            headers: {
                "Content-Type": "application/json;charset=utf-8"
            },
            contentType: 'application/json; charset=utf-8',
            success: function (res) {
                if(res['code']=="200")
                {
                    window.parent.opener.location.reload();
                    window.close();
                }else
                {
                    var picId=res['pictureId']+"_"+res['pictureAction'];
                    $("#"+picId).parent().remove();
                    ($("#tab ul li.on").remove());
                    $("#tab ul").children().first().attr("class","on");
                    $("#picContent").children().first().attr("class","show dd");
                    initTab();
                }
            }
        })
  });

})