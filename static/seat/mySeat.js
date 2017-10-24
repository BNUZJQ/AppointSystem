var firstSeatLabel = 1;
var unavailables = [];
var duration = [];
var display_appointments = function (appointments) {
    console.log(appointments);
    var infos = [];
    var apppointments_json = JSON.parse(appointments);
    for (var i = 0; i < apppointments_json.length; i++) {
        for (var j = apppointments_json[i].start; j < apppointments_json[i].end; j++) {
            //console.log(apppointments_json[i].date.slice(5) + "_" + j);
            unavailables.push(apppointments_json[i].date.slice(5) + "_" + (j + 7) + "-" + (j + 8));
            infos.push("Who:" + apppointments_json[i].custom + "Reason:" + apppointments_json[i].reason);
        }
    }
    console.log(unavailables);
    console.log(infos);
};
$(".choose_classroom").click(function () {
    var classroom = $("#classroom").val();
    // 获取未来一个月内的预约情况
    $.ajax({
        async: false,
        url: '/api/classroom/' + classroom,
        type: 'get',
        data: {},
        success: function (data) {
            display_appointments(data.appointments);
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

$(".submit").click(function () {
    var classroom = $("#classroom").val();
    var reason = $("#reason").val();
    var multimedia = $("#multimedia").val();
    var desk = $("#desk").val();
    // 获取未来一个月内的预约情况
    $.ajax({
        async: false,
        url: '/api/classroom/' + classroom,
        type: 'post',
        data: {},
        beforeSend: function () {
            console.log("flag" + classroom + reason + multimedia + desk);
            console.log(duration);
            var temp = [];
            var thisdate = duration[0].split("_")[0];
            var error_code = 0;
            for (var i = 0; i < duration.length; i++) {
                temp.push(duration[i].split("_")[1].split("-")[0]);
                if (duration[i].split("_")[0] != thisdate) {
                    error_code = 1;//一条预约必须是同一天
                    console.log("一条预约必须是同一天");
                    alert("一条预约必须是同一天");
                }
            }
            console.log(duration.length);
            if (((Math.max.apply(null, temp)) - (Math.min.apply(null, temp)) + 1) == duration.length) {
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
    console.log(activeTab);

});

$(document).ready(function () {
    console.log("begin");
    $(".choose_classroom").trigger("click");
    var $cart = $('#selected-seats'),
        $counter = $('#counter'),
        $total = $('#total'),
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
            },
            legend: {
                node: $('#legend'),
                items: [
                    ['e', 'available', '可以预订'],
                    ['e', 'unavailable', '已被占用']
                ]
            },
            click: function () {
                if (this.status() == 'available') {
                    // console.log(this.settings.id);
                    //let's create a new <li> which we'll add to the cart items
                    $('<li>' + this.settings.label + ':00<a href="#" class="cancel-cart-item">[cancel]</a></li>')
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
                    $total.text(recalculateTotal(sc) + this.data().price);
                    return 'selected';
                } else if (this.status() == 'selected') {
                    //update the counter
                    $counter.text(sc.find('selected').length - 1);
                    //and total
                    $total.text(recalculateTotal(sc) - this.data().price);
                    //remove the item from our cart
                    $('#cart-item-' + this.settings.id).remove();
                    duration.pop(this.settings.id);
                    //seat has been vacated
                    return 'available';
                } else if (this.status() == 'unavailable') {

                    confirm("我觉得这样显示就很好，点unavailable的时候，用一个alert函数就做到了。。。");

                    //seat has been already booked
                    return 'unavailable';
                } else {
                    return this.style();
                }
            }
        });

    //this will handle "[cancel]" link clicks
    $('#selected-seats').on('click', '.cancel-cart-item', function () {
        //let's just trigger Click event on the appropriate seat, so we don't have to repeat the logic here
        sc.get($(this).parents('li:first').data('seatId')).click();
    });

    //let's pretend some seats have already been booked
    sc.get(unavailables).status('unavailable');

});

function recalculateTotal(sc) {
    var total = 0;

    //basically find every selected seat and sum its price
    sc.find('selected').each(function () {
        total += this.data().price;
    });

    return total;
}
