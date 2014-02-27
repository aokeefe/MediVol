function resetPassword()

$(document).ready(function() {
    $('#resetPassword').click(function() {
        var password = $('#password').val();
        var confirmPassword = $('#confirmPassword').val();
        
        if (password == '' || confirmPassword == '') {
            $('.requiredMessage').html('All fields are required.');
            $('.requiredMessage').show();
            
            return;
        } else if (password != confirmPassword) {
            $('.requiredMessage').html('Passwords do not match.');
            $('.requiredMessage').show();
            
            return;
        }
    });
});