function resetPassword(resetCode, password, confirmPassword) {
    Dajaxice.administration.reset_password(
        function(response) {
            if (response == 'True') {
                window.location = '/login/';
            } else if (response == 'password mismatch') {
                $('.requiredMessage').html('Passwords do not match.');
                $('.requiredMessage').show();

                return;
            } else if (response == 'invalid code') {
                $('.requiredMessage').html('The reset code is invalid.');
                $('.requiredMessage').show();

                return;
            }
        },
        {
            'reset_code': resetCode,
            'password': password,
            'confirm_password': confirmPassword
        }
    );
}

$(document).ready(function() {
    $('#resetPassword').click(function() {
        var password = $('#password').val();
        var confirmPassword = $('#confirmPassword').val();
        var resetCode = $('#resetCode').val();

        if (password == '' || confirmPassword == '') {
            $('.requiredMessage').html('All fields are required.');
            $('.requiredMessage').show();

            return;
        } else if (password != confirmPassword) {
            $('.requiredMessage').html('Passwords do not match.');
            $('.requiredMessage').show();

            return;
        }

        resetPassword(resetCode, password, confirmPassword);
    });

    $('#addWarehouseWrapper').keydown(function (e){
        // detect enter key
        if(e.keyCode == 13){
            var buttonChildren = $(this).children('.button');
            buttonChildren[buttonChildren.length - 1].click();
        }
    });
});
