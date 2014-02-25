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
    
    $('.removeWarehouse').click(function(event) {
        // what has my life become?
        var abbreviation = $($(this).parent().parent().children('td')[0]).html();
        var name = $($(this).parent().parent().children('td')[1]).html();
        
        if (confirm('Are you sure you want to remove the "' + name + '" warehouse?')) { 
            removeWarehouse(abbreviation);
        }
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

function prepareUserManagement() {
    $('.removeUser').click(function() {
        var userToRemove = $($(this).parent().parent().children('td')[0]).html();
        
        if (confirm('Are you sure you want to remove the user "' + userToRemove + '"?')) {
            removeUser(userToRemove);
        }
    });
    
    var oldGroup;
    
    $('.changeGroupSelect').focus(function() {
        oldGroup = $(this).val()
    }).change(function() {
        var newGroup = $(this).val();
        var userToChange = $($(this).parent().parent().children('td')[0]).html();
        
        if (confirm('Are you sure you want to change ' + userToChange + 
                '\'s group from "' + oldGroup + '" to "' + newGroup + '"?')) {
            changeUserGroup(userToChange, newGroup);
        } else {
            $(this).val(oldGroup);
        }
    });
    
    $('#createUser').click(function() {
        var username = $('#username').val();
        var email = $('#email').val();
        var group = $('#setGroup').val();
        var password = $('#password').val();
        var confirmPassword = $('#confirmPassword').val();
        
        if (username == '' || email == '' || 
                password == '' || confirmPassword == '') {
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
}

$(document).ready(function() {
    prepareWarehouseManagement();
    
    prepareUserManagement();
});