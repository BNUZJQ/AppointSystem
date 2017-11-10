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
                $("<tr>" + "<td>" + appointments[i].classroom__name + "</td>" + "</tr>")
                    .attr('id', 'myappinfo')
                    .appendTo$("#myappinfo")
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
    return appointments;

});