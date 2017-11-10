var appointments;
$(document).ready(function () {
    $.ajax({
        async: false,
        url: '/api/classroom/500/',
        type: 'get',
        mine: '',
        data: {},
        success: function (data) {
            console.log(data);
            appointments = data.appointments;
            console.log(data);
            for (var i = 0; i < appointments.length; i++) {
                $("#appointments").html(appointments);
            }
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