var $cart = $('#selected-seats'),
    $counter = $('#counter'),
    $total = $('#total');
var sc;
var unavailables = [];
var duration = [];

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
            'eeeeeeeeeeeeee',
            'eeeeeeeeeeeeee',
            'eeeeeeeeeeeeee',
            'eeeeeeeeeeeeee',
            'eeeeeeeeeeeeee',
            'eeeeeeeeeeeeee',
            'eeeeeeeeeeeeee'

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
                return column;
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
                /*
                 * Lets update the counter and total
                 *
                 * .find function will not find the current seat, because it will change its stauts only after return
                 * 'selected'. This is why we have to add 1 to the length and the current seat price to the total.
                 */
                $counter.text(sc.find('selected').length + 1);
                $total.text(recalculateTotal(sc) + this.data().price);
                return 'selected';
            } else if (this.status() === 'selected') {
                //update the counter
                $counter.text(sc.find('selected').length - 1);
                //and total
                $total.text(recalculateTotal(sc) - this.data().price);
                //remove the item from our cart
                $('#cart-item-' + this.settings.id).remove();
                duration.pop(this.settings.id);
                //seat has been vacated
                return 'available';
            } else if (this.status() === 'unavailable') {
              $.gritter.add({
                // (string | mandatory) the heading of the notification
                title: 'This is a Notice Without an Image!',
                // (string | mandatory) the text inside the notification
                text: 'This will fade out after a certain amount of time. This note also contains a link example. Thank you so much to try Dashgum. Developed by <a href="#" style="color:#FFD777">Alvarez.is</a>.'
              });
                confirm("我觉得这样显示就很好，点unavailable的时候，用一个alert函数就做到了。。。");

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

var display_appointments = function (appointments) {
    //console.log(appointments);
    sc.get(unavailables).status('available');
    unavailables = [];
    var infos = [];
    var apppointments_json = JSON.parse(appointments);
    for (var i = 0; i < apppointments_json.length; i++) {
        for (var j = apppointments_json[i].start; j < apppointments_json[i].end; j++) {
            //console.log(apppointments_json[i].date.slice(5) + "_" + j);
            unavailables.push(apppointments_json[i].date.slice(5) + "_" + j + "-" + (j + 1));
            infos.push("Who:" + apppointments_json[i].custom + "Reason:" + apppointments_json[i].reason);
        }
    }
    // console.log(unavailables);
    // console.log(infos);
    //let's pretend some seats have already been booked
    sc.get(unavailables).status('unavailable');
};
$(".choose_classroom").click(function () {
    var classroom = $("#classroom").val();
    // 获取未来一个月内的预约情况
    $.ajax({
        async: false,
        url: '/api/classroom/' + classroom + '/',
        type: 'get',
        data: {},
        success: function (data) {
            display_appointments(data.appointments);
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
});

//提交函数
$(".submit").click(function () {
    var classroom = $("#classroom").val(),
        reason = $("#reason").val(),
        multimedia = $('input[type="checkbox"]#multimedia').checked,
        desk = $('input[type="checkbox"]#desk').checked,
        d = new Date(),
        temp = [],
        thisdate = duration[0].split("_")[0],
        error_code = 0,
        start = 0,
        end = 0;
    console.log("flag" + classroom + reason + multimedia + desk);
    console.log(duration);
    for (var i = 0; i < duration.length; i++) {
        temp.push(duration[i].split("_")[1].split("-")[0]);
        if (duration[i].split("_")[0] != thisdate) {
            error_code = 1;//一条预约必须是同一天
            console.log("一条预约必须是同一天");
            alert("一条预约必须是同一天");
        }
    }
    console.log(duration.length);
    start = Math.min.apply(null, temp);
    end = Math.max.apply(null, temp) + 1;
    // 获取未来一个月内的预约情况
    $.ajax({
        async: false,
        url: '/api/classroom/' + classroom + '/',
        type: 'post',
        data: {
            'classroom': classroom,
            'csrfmiddlewaretoken': $('#csrf_token').val(),
            "date": d.getFullYear() + '-' + thisdate,
            "start": start,
            "end": end,
            "reason": reason,
            "multimedia": multimedia,
            "desk": desk
        },
        beforeSend: function () {

            if ((end - start) == duration.length) {
                error_code = 0;//预约信息合法
                console.log("预约信息合法");
            }
            else {
                error_code = 2;//预约的时间必须是连续的时间段
                console.log("预约的时间必须是连续的时间段");
                alert("预约的时间必须是连续的时间段");
            }

            if (error_code != 0)
                return false;

        },
        success: function (msg) {
            $(".choose_classroom").trigger("click");
            console.log(msg)
        },
        error: function () {
            console.log("post error!")
        }
    }); // ajax
});

$('a[data-toggle="tab"]').on("click", function (e) {
    // 获取已激活的标签页的名称
    var activeTab = $(e.target).text();
    $('.seatCharts-row').remove();
    $('.seatCharts-legendItem').remove();
    $('#seat-map,#seat-map *').unbind().removeData();
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
    $(".choose_classroom").trigger("click");
    //this will handle "[cancel]" link clicks
    $('#selected-seats').on('click', '.cancel-cart-item', function () {
        //let's just trigger Click event on the appropriate seat, so we don't have to repeat the logic here
        sc.get($(this).parents('li:first').data('seatId')).click();
    });

    //let's pretend some seats have already been booked
    sc.get(unavailables).status('unavailable');

});
