var ITEM_TEMPLATE = '<tr>' + 
        '<td style="border: 1px solid black">{category}</td>' + 
        '<td style="border: 1px solid black">{box_name}</td>' + 
        '<td style="border: 1px solid black">{item}</td>' + 
        '<td style="border: 1px solid black">{expiration}</td>' + 
        '<td style="border: 1px solid black">{count}</td>' + 
        '<td style="border: 1px solid black"><a class="remove_item" href="javascript:void(0)">Remove</a></td>' + 
    '</tr>';
    
var BLANK_ROW = "<tr id='placeholder_row'>" + 
                    "<td style='border: 1px solid black'></td>" + 
                    "<td style='border: 1px solid black'></td>" + 
                    "<td style='border: 1px solid black'></td>" + 
                    "<td style='border: 1px solid black'></td>" + 
                    "<td style='border: 1px solid black'>&nbsp;</td>" + 
                "</tr>";

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
    
    $('#add_item').click(function(e) {
        e.preventDefault();
        
        var category = $('#categories option:selected').val();
        var boxName = $('#box_names option:selected').val();
        var item = $('#items option:selected').val();
        var expiration = ($('#expiration').val() == '') ? 'Never' : $('#expiration').val();
        var count = $('#count').val();
        
        if (typeof(category) == 'undefined' || 
                typeof(boxName) == 'undefined' || 
                typeof(item) == 'undefined' || 
                count == '') {
            return;
        }
        
        $('#placeholder_row').remove();
        
        $('#items_added').append(
            ITEM_TEMPLATE.replace('{category}', category)
                .replace('{box_name}', boxName)
                .replace('{item}', item)
                .replace('{expiration}', expiration)
                .replace('{count}', count)
        );
        
        $('.remove_item').click(function() {
            $(this).parent().parent().remove();
            
            if ($('#items_added tr').length == 1) {
                $('#items_added').append(BLANK_ROW);
            }
        });
    });
});