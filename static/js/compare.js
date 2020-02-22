$(window).unload(function () {
    var pictureId = $("#bicubic_Upscale img").attr("id");
    $.ajax({
        url: '/closecompare',
        type: 'post',
        dataType: 'json',
        data: JSON.stringify({
            pictureId: pictureId
        }),
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        contentType: 'application/json; charset=utf-8',
        success: function (res) {

        }
    })
});