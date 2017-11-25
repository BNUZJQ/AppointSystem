var appointments;


$(document).ready(function () {
    $.ajax({
        async: false,
        url: '/api/appointment/',
        type: 'get',
        mine: '',
        data: {
            "mine": "mine"
        },
        success: function (data) {
            console.log(data);
            appointments = data.appointments;
            for (var i = 0; i < appointments.length; i++) {
                $("#myappinfo").append("<tr>" +
                    "<td>" + appointments[i].classroom__name + "</td>" +
                    "<td>" + appointments[i].date + "</td>" +
                    "<td>" + appointments[i].start + "-" + appointments[i].end + "点</td>" +
                    "<td>" + appointments[i].reason + "</td>" +
                    "<td>" + appointments[i].boss + "</td>" +
                    "<td>" +
                    //"<button class=\"btn btn-success btn-xs\"><i class=\"fa fa-check\"></i></button>" +
                    "<button name=\"" +
                    appointments[i].id +
                    "\" class=\" search btn btn-primary btn-xs\"><i class=\" fa fa-search\"></i></button>" +
                    "<button name=\"" +
                    appointments[i].id +
                    "\" class=\" delete btn btn-danger btn-xs\"><i class=\" fa fa-trash-o\"></i></button>" +
                    "</td>" +
                    "</tr>");
                //$("#appointments").html(appointments[i].classroom__name + appointments[i].date);
            }

            console.log(appointments);
        }, // success
        error: function (data) {
            if (data.status === 400) {
                alert("400 error");
            }
            if (data.status === 403) {
                alert("403 error");
            }
        } // error
    }); // ajax

    $(".delete").click(function () {
        var id = $(this).attr("name");
        console.log(id);
        if (confirm("确定删除此条预约？   ID = " + id)) {
            //点击确定后操作
            //get_appointments(classroom);
            var delete_id = -1;
            for (var i = 0; i < appointments.length; i++) {
                if (appointments[i].id == id) {
                    delete_id = appointments[i].id;
                }
            }
            if (delete_id === -1) {
                alert("NOT FOUND", "请重新选择需要取消的预约");
                return;
            }
            $.ajax({
                async: false,
                url: '/api/appointment/' + delete_id + '/delete_appoint/',
                type: 'POST',
                data: {
                    'id': delete_id,
                    'csrfmiddlewaretoken': $('#csrf_token').val()
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
                },
                success: function (data) {
                    alert("操作成功", "已取消预约");
                    location.reload();
                },
                error: function (data) {
                    if (alert.status === 400) {
                        notification("400 Error", data.msg);
                    }
                    if (data.status === 404) {
                        notification("404 NOT FOUND", data.msg)
                    }
                }
            })


        }
    });
    $(".search").click(function () {
        var id = $(this).attr("name");
        console.log(id);
        for (var i = 0; i < appointments.length; i++) {
            if (appointments[i].id == id) {
                notification("其他信息", "使用原因：" + appointments[i].reason + '<br>' +
                    "使用者：" + appointments[i].director + '<br>' +
                    "使用者电话： " + appointments[i].director_phone + '<br>' +
                    "是否移动桌椅： " + appointments[i].desk + '<br>' +
                    "是否使用多媒体 ：" + appointments[i].multimedia);
            }
        }


    });
    return appointments;
});

var notification = function (title, text) {
    $.gritter.add({
        // (string | mandatory) the heading of the notification
        title: title,
        // (string | mandatory) the text inside the notification
        text: text
    });
};

