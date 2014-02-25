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

$(document).ready(function() {
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
});