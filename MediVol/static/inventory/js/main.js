function getBoxNames(response) {
    $('#box_names').empty();
    $('#items').empty();
    
    for (var i = 0; i < response.length; i++) {
        $('#box_names').append('<option>' + response[i] + '</option>');
    }
}

function getItems(response) {
    $('items').empty();
    
    for (var i = 0; i < response.length; i++) {
        $('#items').append('<option>' + response[i] + '</option>');
    }
}

$(document).ready(function() {
    $('#categories').change(function() {
        var selectedCategory = $('#categories option:selected').val();
        Dajaxice.inventory.get_box_names(getBoxNames, { 'category_name': selectedCategory });
    });
    
    $('#box_names').change(function() {
        var selectedBoxName = $('#box_names option:selected').val();
       
        Dajaxice.inventory.get_items(getItems, { 'box_name': selectedBoxName });
    });
});