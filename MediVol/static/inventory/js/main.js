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
                
var boxNameToChoose = '';
var itemToChoose = '';

function getBoxNames(response) {
    $('#box_names').empty();
    $('#items').empty();
    
    for (var i = 0; i < response.length; i++) {
        $('#box_names').append('<option>' + response[i] + '</option>');
    }
    
    if (boxNameToChoose != '') {
        $('#box_names').val(boxNameToChoose);
        boxNameToChoose = '';
        $('#box_names').change();
    }
}

function getItems(response) {
    $('#items').empty();
    
    for (var i = 0; i < response.length; i++) {
        $('#items').append('<option>' + response[i] + '</option>');
    }
    
    if (itemToChoose != '') {
        $('#items').val(itemToChoose);
        itemToChoose = '';
        $('#items').change();
    }
}

function createBox(response) {
    console.log(response);
}

function setRemoveButton() {
    $('.remove_item').click(function() {
        $(this).parent().parent().remove();
        
        if ($('#items_added tr').length == 1) {
            $('#items_added').append(BLANK_ROW);
        }
    });
}

function getAutocompleteCallback(response){
    var object = {
        response: response, 
        theCallback: function(returned) {
            response(returned);
        }
    };
    
    return object;
}

function autocompleteCallback(request, response) {
    dajaxiceAutocomplete = getAutocompleteCallback(response);
    
    Dajaxice.inventory.get_search_results(dajaxiceAutocomplete.theCallback, { 'query': request.term });
}

$(document).ready(function() {
    $('#itemSearch').autocomplete(
        {
            source: autocompleteCallback,
            messages: {
                noResults: '',
                results: function() {}
            },
            close: function() {
                var query = $('#itemSearch').val();
                var actualQuery = query;
                
                if (query.lastIndexOf('> ') != -1) {
                    actualQuery = query.substr(query.lastIndexOf('> ') + 2, query.length);
                }
                
                $('#itemSearch').val(actualQuery);
                
                var queryArray = query.split(' > ');
                var category = queryArray[0];
                var boxName = '';
                var item = '';
                
                if (queryArray.length > 1) {
                    boxName = queryArray[1];
                }
                
                if (queryArray.length > 2) {
                    item = queryArray[2];
                }
                
                $('#categories').val(category).change();
                
                if (boxName != '') {
                    boxNameToChoose = boxName;
                }
                
                if (item != '') {
                    itemToChoose = item;
                }
            }
        }
    );

    $('#categories').change(function() {
        var selectedCategory = $('#categories option:selected').val();
        
        Dajaxice.inventory.get_box_names(getBoxNames, { 'category_name': selectedCategory });
    });
    
    $('#box_names').change(function() {
        var selectedBoxName = $('#box_names option:selected').val();
       
        Dajaxice.inventory.get_items(getItems, { 'box_name': selectedBoxName });
    });
    
    $('#items').change(function() {
        
    })
    
    $('#add_item').click(function(e) {
        // Prevent button from submitting form.
        e.preventDefault();
        
        var category = $('#categories option:selected').val();
        var boxName = $('#box_names option:selected').val();
        var item = $('#items option:selected').val();
        var expiration = ($('#expiration').val() == '') ? 'Never' : $('#expiration').val();
        var count = $('#count').val();
        
        // Required fields to add an item.
        if (typeof(category) == 'undefined' || 
                typeof(boxName) == 'undefined' || 
                typeof(item) == 'undefined' || 
                count == '' || 
                count < 1) {
            return;
        }
        
        $('#placeholder_row').remove();
        
        $('#count').val('');
        $('#expiration').val('');
        
        $('#items_added').append(
            ITEM_TEMPLATE.replace('{category}', category)
                .replace('{box_name}', boxName)
                .replace('{item}', item)
                .replace('{expiration}', expiration)
                .replace('{count}', count)
        );
        
        setRemoveButton();
    });
    
    $('#submit').click(function(e) {
        e.preventDefault();
        
        var initials = $('input[name=initials]').val();
        var weight = $('input[name=weight]').val();
        var size = $('input[name=size]:checked').val();
        var note = $('textarea[name=note]').val();
        
        // Required fields.
        if (initials == '' || weight == '' || typeof(size) == 'undefined') {
            return;
        }
        
        var items = [];
        
        $('#items_added tr').each(function(index, element) {
            element = $(element);
            
            if (element.attr('id') != 'placeholder_row' && 
                    element.attr('id') != 'table_header') {
                var itemInfo = element.children('td');
                var itemName = $(itemInfo[2]).html();
                var expiration = $(itemInfo[3]).html();
                var count = $(itemInfo[4]).html();
                
                items.push([ itemName, expiration, count ]);
            }
        });
        
        // Can't have 0 items.
        if (items.length == 0) {
            return;
        }
        
        Dajaxice.inventory.create_box(createBox, 
            {
                'initials': initials,
                'weight': weight,
                'size': size,
                'items': items,
                'note': note
            }
        );
    });
});