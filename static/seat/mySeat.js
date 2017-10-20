var firstSeatLabel = 1;
var unavailables = [];
var display_appointments = function (appointments) {
    var infos = [];
    var apppointments_json = JSON.parse(appointments);
    for (var i = 0; i < apppointments_json.length; i++) {
        for (var j = apppointments_json[i].start; j < apppointments_json[i].end; j++) {
            //console.log(apppointments_json[i].date.slice(5) + "_" + j);
            unavailables.push(apppointments_json[i].date.slice(5) + "_" + j);
            infos.push("Who:" + apppointments_json[i].custom + "Reason:" + apppointments_json[i].reason);
        }
    }
    console.log(unavailables);
    console.log(infos);
};

$(document).ready(function () {
    console.log("begin");
    var classroom = "500";
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

    var firstSeatLabel = 1;

    $(document).ready(function () {
        var $cart = $('#selected-seats'),
            $counter = $('#counter'),
            $total = $('#total'),
            $check = $('#check'),
            sc = $('#seat-map').seatCharts({
                map: [
                    'eeeeeeeeeeeeee',
                    'eeeeeeeeeeeeee',
                    'eeeeeeeeeeeeee',
                    'eeeeeeeeeeeeee',
                    'eeeeeeeeeeeeee',
                    'eeeeeeeeeeeeee',
                    'eeeeeeeeeeeeee',

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
                        //let's create a new <li> which we'll add to the cart items
                        $('<li>' + this.settings.label + ':00<a href="#" class="cancel-cart-item">[cancel]</a></li>')
                            .attr('id', 'cart-item-' + this.settings.id)
                            .data('seatId', this.settings.id)
                            .appendTo($cart);
                        //   $('<li>' + this.data().category + ' Seat # ' + this.settings.label + ': <b>$' + this.data().price + '</b> <a href="#" class="cancel-cart-item">[cancel]</a></li>')
                        //       .attr('id', 'cart-item-' + this.settings.id)
                        //       .data('seatId', this.settings.id)
                        //       .appendTo($cart);

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
    };
});