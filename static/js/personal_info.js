var $account_id = document.getElementById('account_id').innerHTML;
$(document).ready(function () {
    var $infos;
    console.log($account_id);
    $.ajax({
        async: false,
        url: '/api/account/' + $account_id,
        type: 'get',
        mine: '',
        data: {},
        success: function (data) {
            $infos = data;
            console.log($infos);
            $("#username").html($infos.user);
            $("#student_id").html($infos.student_id);
            $("#gender").html($infos.gender);
            $("#telephone").html($infos.telephone);
            $("#email").html($infos.email);
            $("#major").html($infos.major);
            $("#role").html($infos.role);
            $("#grade").html($infos.grade);
            //("#question").html($infos.question);
            // $("#answer").html($infos.answer);
        }, // success
        error: function (data) {
            if (data.status === 400) {
                alert("400 error");
            }
            if (data.status === 403) {
                alert("403 error");
            }
        } // error
    }) // ajax
});

