var $cart = $('#selected-seats'),
    $counter = $('#counter'),
    $total = $('#total');
var sc;
var unavailables = [];
var duration = [];
var infos = {};
var appointments;

var fix = function (num, length) {
    return ('' + num).length < length ? ((new Array(length + 1)).join('0') + num).slice(-length) : '' + num;
};

var create_sc = function (week) {
    //console.log("create sc with week " + week);
    var Myrows = [];
    for (var i = 1; i <= 7; i++) {
        var d = new Date();
        d.setDate(d.getDate() + i - 1 + week * 7);
        Myrows.push(fix(d.getMonth() + 1, 2) + "-" + fix(d.getDate(), 2));
    }
    sc = $('#seat-map').seatCharts({
        map: [
            'eeeeeeeeeeeeeee',
            'eeeeeeeeeeeeeee',
            'eeeeeeeeeeeeeee',
            'eeeeeeeeeeeeeee',
            'eeeeeeeeeeeeeee',
            'eeeeeeeeeeeeeee',
            'eeeeeeeeeeeeeee'

        ],
        seats: {
            e: {
                price: 40,
                classes: 'economy-class', //your custom CSS class
                category: 'Economy Class'
            }

        },
        naming: {
            //top : false,
            getLabel: function (character, row, column) {
                return "";
            },
            rows: [Myrows[0], Myrows[1], Myrows[2], Myrows[3], Myrows[4], Myrows[5], Myrows[6]]
        },
        legend: {
            node: $('#legend'),
            items: [
                ['e', 'available', '可以预订'],
                ['e', 'unavailable', '已被占用']
            ]
        },
        click: function () {
            if (this.status() === 'available') {
                // console.log(this.settings.id);
                //let's create a new <li> which we'll add to the cart items

                $('<li>' + this.settings.id.split("_")[0].split("-")[0] + "月" + this.settings.id.split("_")[0].split("-")[1] + "日" + this.settings.id.split("_")[1] + ':00<a href="#" class="cancel-cart-item">[取消]</a>')
                    .attr('id', 'cart-item-' + this.settings.id)
                    .data('seatId', this.settings.id)
                    .appendTo($cart);
                duration.push(this.settings.id);
                console.log(duration);
                /*
                 * Lets update the counter and total
                 *
                 * .find function will not find the current seat, because it will change its stauts only after return
                 * 'selected'. This is why we have to add 1 to the length and the current seat price to the total.
                 */
                $counter.text(sc.find('selected').length + 1);
                return 'selected';
            } else if (this.status() === 'selected') {
                //update the counter
                $counter.text(sc.find('selected').length - 1);
                //and total
                $('#cart-item-' + this.settings.id).remove();
                //console.log($cart);
                duration.removeByValue(this.settings.id);
                console.log(duration);
                //seat has been vacated
                return 'available';
            } else if (this.status() === 'unavailable') {
                var title = '该时间段已被占用：(';
                var msg = '占用信息：<br>' + "日期：" + this.settings.id.split("_")[0].split("-")[0] +
                    "月" + this.settings.id.split("_")[0].split("-")[1] + "日" +
                    '<br>' + infos[this.settings.id].split(";")[0] + '<br>' + infos[this.settings.id].split(";")[1]
                    + '<br>' + infos[this.settings.id].split(";")[2] + '<br>' + infos[this.settings.id].split(";")[3]
                    + '<br>' + infos[this.settings.id].split(";")[4] + '<br>' + infos[this.settings.id].split(";")[5];

                notification(title, msg);
                console.log(duration);
                //seat has been already booked
                return 'unavailable';
            } else {
                return this.style();
            }
        }
    });
    //console.log(unavailables);
    sc.get(unavailables).status('unavailable');
};

// 根据appointments来补充info变量，并将对应位置置为unavailable
var display_appointments = function (appointments_json) {
    console.log(appointments_json);
    sc.get(unavailables).status('available');
    unavailables = [];
    var temp_seatID;
    for (var i = 0; i < appointments_json.length; i++) {
        for (var j = appointments_json[i].start; j < appointments_json[i].end; j++) {
            temp_seatID = appointments_json[i].date.slice(5) + "_" + j + "-" + (j + 1);
            unavailables.push(temp_seatID);
            infos[temp_seatID] = "时间：" + appointments_json[i].start + "——" + appointments_json[i].end + "点;" +
                "预约人：" + appointments_json[i].custom__user__first_name + "[" + appointments_json[i].custom__grade + appointments_json[i].custom__major + "];" +
                "电话:" + appointments_json[i].custom__telephone + ";" +
                "预约原因：" + appointments_json[i].reason + ";" +
                "负责老师：" + appointments_json[i].boss + ";" +
                "负责人：" + appointments_json[i].director + "[电话:" + appointments_json[i].director_phone + "]";

        }
    }
    // console.log(unavailables);
    // console.log(infos);
    //let's pretend some seats have already been booked
    sc.get(unavailables).status('unavailable');
};

var notification = function (title, text) {
    $.gritter.add({
        // (string | mandatory) the heading of the notification
        title: title,
        // (string | mandatory) the text inside the notification
        text: text
    });
};

// 从api中获取classroom
var get_appointments = function (classroom) {
    $.ajax({
        async: false,
        url: '/api/appointment/',
        type: 'get',
        data: {
            "classroom": classroom
        },
        success: function (data) {
            appointments = data.appointments;
            display_appointments(appointments);
            $("#title").html(classroom + "预约情况");
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
    return appointments;
};

//提交函数
$(".submit").click(function () {
    if ($('input[type="checkbox"]#read').is(':checked') == false)
    {
        notification('请仔细阅读《会议室管理规定》！','请仔细阅读《会议室管理规定》！');
        return false;
    }
    if (duration[0] == null) {
        notification('请填写预约时间！', '请填写预约时间！');
        return false;
    }
    var classroom = $("#classroom").val(),
        reason = $("#reason").val(),
        boss = $("#boss").val(),
        director = $("#director").val(),
        director_phone = $("#director_phone").val(),
        multimedia = $('input[type="checkbox"]#multimedia').is(':checked'),
        desk = $('input[type="checkbox"]#desk').is(':checked'),
        d = new Date(),
        temp = [],
        thisdate = duration[0].split("_")[0],
        error_code = 0,
        start = 0,
        end = 0,
        error_reason = '';
        //console.log(director);
        //console.log(director_phone);
        if(director.length!=0 && director_phone.length == 0)
        {
            notification('信息缺失', '请填写使用者电话');
            return false;
        }
    console.log("flag" + classroom + reason + boss + director + director_phone + multimedia + desk);
    console.log(duration);
    for (var i = 0; i < duration.length; i++) {
        temp.push(duration[i].split("_")[1].split("-")[0]);
        if (duration[i].split("_")[0] !== thisdate) {
            error_code = 1;//一条预约必须是同一天
            error_reason = '一条预约必须为同一天';
            console.log(error_reason);
            notification('预约信息不合法！' + '    error_code = ' + error_code, error_reason);
            return false;
            //alert("一条预约必须是同一天");
        }
    }
    console.log(duration.length);
    start = Math.min.apply(null, temp);
    end = Math.max.apply(null, temp) + 1;
    if ((end - start) === duration.length) {
        error_code = 0;//预约信息合法
        error_reason = '预约信息合法';
        console.log(error_reason);

    }
    else {
        error_code = 2;//预约的时间必须是连续的时间段
        error_reason = '预约的时间必须是连续的时间段';
        console.log(error_reason);
        notification('预约信息不合法！' + '    error_code = ' + error_code, error_reason);
        //alert("预约的时间必须是连续的时间段");
    }
    /*if ((director) && ~(director_phone))
    {
        error_code=3;
        error_reason = "使用者姓名和电话必须都填写或者都不填写";
        notification('预约信息不合法！' + '    error_code = ' + error_code, error_reason);
    }
*/
    if (error_code !== 0)
        return false;

    // post信息
    $.ajax({
        async: false,
        url: '/api/appointment/',
        type: 'post',
        data: {
            'classroom': classroom,
            'csrfmiddlewaretoken': $('#csrf_token').val(),
            "date": d.getFullYear() + '-' + thisdate,
            "start": start,
            "end": end,
            "reason": reason,
            "multimedia": multimedia,
            "desk": desk,
            "boss": boss,
            "director": director,
            "director_phone": director_phone
        },
        success: function (msg) {
            // To do 刷新
            if(confirm('预约成功！点击确定返回页面')) {
                location.reload();
                $("#classroom").val(classroom);
                $(".choose_classroom").trigger("click");
            }
            else
            {
                location.reload();
                $("#classroom").val(classroom);
                $(".choose_classroom").trigger("click");
            }

        },
        error: function (msg) {
            console.log("post error!");
            console.log(msg)
            console.log(msg.responseText);
            var title = '预约信息不合法' + ' 错误代码 = post error';
            var text = msg.responseText;
            notification(title, text);
        }
    }); // ajax
});

$('a[data-toggle="tab"]').on("click", function (e) {
    //清空当前选择的位置
    var selected_seats = $('#selected-seats li');
    var len = selected_seats.length;
    for (var i = 0; i < len; i++) {
        sc.get(selected_seats[i].id.replace("cart-item-", "")).click();
    }
    // 获取已激活的标签页的名称
    var activeTab = $(e.target).text();
    $('.seatCharts-row').remove();
    $('.seatCharts-legendItem').remove();
    $('#seat-map,#seat-map *').unbind().removeData();
    //$cart.;
    if (activeTab === "未来7天") {
        create_sc(0);
    } else if (activeTab === "8-14天") {
        create_sc(1);
    } else if (activeTab === "15-21天") {
        create_sc(2);
    } else {
        create_sc(3);
    }

});

$(document).ready(function () {
    create_sc(0);
    $(".choose_classroom").click(function () {
        var classroom = $("#classroom").val();
        get_appointments(classroom);
    }).trigger('click');
    //this will handle "[cancel]" link clicks
    $('#selected-seats').on('click', '.cancel-cart-item', function () {
        //let's just trigger Click event on the appropriate seat, so we don't have to repeat the logic here
        sc.get($(this).parents('li:first').data('seatId')).click();
    });

    //let's pretend some seats have already been booked
    sc.get(unavailables).status('unavailable');


});

Array.prototype.removeByValue = function(val) {
    for(var i=0; i<this.length; i++) {
        if(this[i] == val) {
            this.splice(i, 1);
            break;
        }
    }
};