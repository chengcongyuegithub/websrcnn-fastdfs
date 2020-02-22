$(document).ready(function () {
        $("#uploader").click(function(){
            var formData = new FormData();
            formData.append('file', $('#fileinput')[0].files[0]);
            $.ajax({
                url: '/uploader',
                type: 'post',
                data: formData,
                contentType: false,
                processData: false,
                success: function (res) {
                    var num=$('#showpicture > a').length;
                    var row=Math.floor(num/5);
                    var lastrowNum=num%5;
                    var i;
                    var picIndex = "<a target=\"_blank\" href='/detail/" + res.id + "'><img src='" + res.url + "'/></a>";
                    if(num==0)
                    {
                        $('#contentpic').append("<div id='showpicture'></div>")
                        $('#contentpic').children().last().append(picIndex)
                        return ;
                    }
                    var curDiv=$('#contentpic').children().first();
                    curDiv.prepend(picIndex);
                    for(i=0;i<row;i++)
                    {
                        lastDiv=curDiv.children().last();
                        if(lastrowNum==0&&i==row-1)
                        {
                            if(row==2)
                            {
                               lastDiv.remove();
                            }else
                            {
                               $('#contentpic').append("<div id='showpicture'></div>")
                               $('#contentpic').children().last().append(lastDiv)
                            }
                        }
                        else
                        {
                            curDiv=curDiv.next();
                            curDiv.prepend(lastDiv);
                        }
                    }
                }
            })
        });
})