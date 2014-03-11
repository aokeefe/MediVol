var MAX_ABBREVIATION_LENGTH = 4;

function createWarehouse(name, abbreviation, address) {
    Dajaxice.administration.add_warehouse(
        function(response) {
            if (response == 'True') {
                window.location.reload();
            } else if (response == 'name') {
                $('.requiredMessage').html('A warehouse with this name already exists.');
                $('.requiredMessage').show();
            } else if (response == 'abbreviation') {
                $('.requiredMessage').html('A warehouse with this abbreviation already exists.');
                $('.requiredMessage').show();
            } else if (response == 'address') {
                $('.requiredMessage').html('A warehouse with this address already exists.');
                $('.requiredMessage').show();
            }
        },
        {
            'name': name,
            'abbreviation': abbreviation,
            'address': address
        }
    );
}

function removeWarehouse(abbreviation) {
    Dajaxice.administration.remove_warehouse(
        function(response) {
            if (response == 'True') {
                window.location.reload();
            }
        },
        {
            'abbreviation': abbreviation
        }
    );
}

function prepareWarehouseManagement() {
    $('#addWarehouse').click(function() {
        var name = $('#warehouseName').val();
        var abbreviation = $('#warehouseAbbreviation').val();
        var address = $('#warehouseAddress').val();

        if (name == '' || abbreviation == '' || address == '') {
            $('.requiredMessage').html('All fields are required.');
            $('.requiredMessage').show();

            return;
        } else if (abbreviation.length > MAX_ABBREVIATION_LENGTH) {
            $('.requiredMessage').html('Abbreviation must be ' + MAX_ABBREVIATION_LENGTH + ' characters or less.');
            $('.requiredMessage').show();

            return;
        }

        createWarehouse(name, abbreviation, address);
    });

    $('.removeWarehouse').click(function() {
        // what has my life become?
        var abbreviation = $($(this).parent().parent().children('td')[0]).html();
        var warehouse = $($(this).parent().parent().children('td')[1]).html();

        $.jConfirm('Are you sure you want to remove the "' + warehouse + '" warehouse?', '',
            function(result) {
                if (result) {
                    removeWarehouse(abbreviation);
                }
            }
        );
    });
}

function removeUser(username) {
    Dajaxice.administration.remove_user(
        function(response) {
            if (response == 'True') {
                window.location.reload();
            }
        },
        {
            'username': username
        }
    );
}

function changeUserGroup(username, newGroup) {
    Dajaxice.administration.change_group(
        function(response) {
            if (response == 'True') {

            }
        },
        {
            'username': username,
            'new_group': newGroup
        }
    );
}

function createUser(username, email, group, password, confirmPassword) {
    Dajaxice.administration.create_user(
        function(response) {
            if (response == 'True') {
                window.location.reload();
            } else if (response == 'username') {
                $('.requiredMessage').html('Username is already in use.');
                $('.requiredMessage').show();
            } else if (response == 'invalid email') {
                $('.requiredMessage').html('This email is invalid.');
                $('.requiredMessage').show();
            } else if (response == 'email') {
                $('.requiredMessage').html('This email is already in use.');
                $('.requiredMessage').show();
            } else if (response == 'password') {
                // reserved for if password is invalid. not sure if we're going to do this
                $('.requiredMessage').html('Password must something something something.');
                $('.requiredMessage').show();
            } else if (response == 'password mismatch') {
                $('.requiredMessage').html('The passwords do not match.');
                $('.requiredMessage').show();
            }
        },
        {
            'username': username,
            'email': email,
            'group': group,
            'password': password,
            'confirm_password': confirmPassword
        }
    );
}

function sendPasswordReset(username, sendToLoginPage) {
    sendToLoginPage = (typeof(sendToLoginPage) == 'undefined') ? false : sendToLoginPage;
    var resetUrl = $('#resetUrl').val();

    Dajaxice.administration.send_reset(
        function(response) {
            if (response == 'True') {
                if (sendToLoginPage) {
                    window.location = '/login/';
                }
            }
        },
        {
            'username': username,
            'reset_url': resetUrl
        }
    );
}

function changeEmail(newEmail) {
    Dajaxice.administration.change_email(
        function(response) {
            if (response == 'True') {
                $('.requiredMessage').html('Your email has been changed and a confirmation email has been sent. ' +
                    'If you do not get the email soon, check to make sure you entered your email correctly.');
                $('.requiredMessage').show();
            } else if (response == 'invalid email') {
                $('.requiredMessage').html('This email is invalid.');
                $('.requiredMessage').show();
            }
        },
        {
            'new_email': newEmail
        }
    );
}

function prepareUserManagement() {
    $('.removeUser').click(function(index, element) {
        var userToRemove = $($(this).parent().parent().children('td')[0]).html();

        $.jConfirm('Are you sure you want to remove the user "' + userToRemove + '"?', '',
            function(result) {
                if (result) {
                    removeUser(userToRemove);
                }
            }
        );
    });

    var oldGroup;

    $('.changeGroupSelect').focus(function() {
        oldGroup = $(this).val();
    }).change(function() {
        var newGroup = $(this).val();
        var userToChange = $($(this).parent().parent().children('td')[0]).html();

        $.jConfirm('Are you sure you want to change ' + userToChange +
                '\'s group from "' + oldGroup + '" to "' + newGroup + '"?', '',
            function(result) {
                if (result) {
                    changeUserGroup(userToChange, newGroup);
                } else {
                    $(this).val(oldGroup);
                }
            }
        );
    });

    $('#createUser').click(function() {
        var username = $('#username').val();
        var email = $('#email').val();
        var group = $('#setGroup').val();
        var password = $('#password').val();
        var confirmPassword = $('#confirmPassword').val();

        if (username === '' || email === '' ||
                password === '' || confirmPassword === '') {
            $('.requiredMessage').html('All fields are required.');
            $('.requiredMessage').show();

            return;
        } else if (password != confirmPassword) {
            $('.requiredMessage').html('Passwords do not match.');
            $('.requiredMessage').show();

            return;
        }

        createUser(username, email, group, password, confirmPassword);
    });

    $('.sendPasswordReset').click(function() {
        var user = $($(this).parent().parent().children('td')[0]).html();

        $.jConfirm('Are you sure you want to send a password reset to "' + user + '"?', '',
            function(result) {
                if (result) {
                    sendPasswordReset(user);
                }
            }
        );
    });

    $('#sendReset').click(function() {
        var user = $('#username').val();

        if (user === '') {
            $('.requiredMessage').html('Please enter a username.');
            $('.requiredMessage').show();

            return;
        }

        sendPasswordReset(user, true);
    });

    $('#userSendReset').click(function() {
        var user = $('#username').val();
        sendPasswordReset(user);
        $('.requiredMessage').html('A link to reset your password has been sent to your email.');
        $('.requiredMessage').show();
    });

    $('#addWarehouseWrapper').keydown(function (e){
        // detect enter key
        if(e.keyCode == 13){
            var buttonChildren = $(this).children('.button');
            buttonChildren[buttonChildren.length - 1].click();
        }
    });

    $('#changeEmail').click(function() {
        var email = $('#email').val();

        changeEmail(email);
    });
}

$(document).ready(function() {
    prepareWarehouseManagement();

    prepareUserManagement();
});
