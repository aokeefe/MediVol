// Template for adding new item to the table.
var ITEM_TEMPLATE = '<tr>' + 
        '<td>{box_id}</td>' + 
        '<td>{box_size}</td>' + 
        '<td>{weight}</td>' + 
        '<td><a class="remove_item" href="javascript:void(0)">Remove</a></td>' + 
    '</tr>';
    
// Simple template used to insert a blank row below the table header 
// when there are no items in the box.
var BLANK_ROW = "<tr id='placeholder_row'>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td>&nbsp;</td>" + 
                "</tr>";

// Need these to update lists for box names and items.
var boxNameToChoose = '';
var itemToChoose = '';
var boxToChoose = '';
var boxesToOrder = []

/**
* Function for getting a specific box information
*/ 

function getBoxInfo(response) { 

  var boxId = response[0];
  var boxSize = response[1];
  var boxWeight = response[2];

    $('#boxes_added').append(
        ITEM_TEMPLATE.replace('{box_id}', boxId)
            .replace('{box_size}', boxSize)
            .replace('{weight}', boxWeight)
    );
  
}
/**
* Callback for get_box_names AJAX call.
*/
function getBoxNames(response) {
    $('#box_names').empty();
    $('#items').empty();
    
    // Add the box names to the list of box names.
    for (var i = 0; i < response.length; i++) {
        $('#box_names').append('<option>' + response[i] + '</option>');
    }
    
    // If this was a search, we have to select the right box name 
    // and trigger the change event so it will populate the items list.
    if (boxNameToChoose != '') {
        $('#box_names').val(boxNameToChoose);
        boxNameToChoose = '';
        $('#box_names').change();
    }
}

/**
* Callback for the get_items AJAX call. Does the same things as 
* the getBoxNames callback, just for items instead.
*/
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

/**
* Callback for the get_items AJAX call. Does the same things as 
* the getItems callback, just for Boxes instead.
*/
function getBoxes(response) { 

  $('#boxes').empty();
  
  for (var i = 0; i < response.length; i++) { 
    $('#boxes').append('<option>' + response[i] + '</option>');
  }
  
  if (boxToChoose != '') { 
    $('#boxes').val(boxToChoose);
    boxToChoose = '';
    $('#boxes').change();
  }
}

/**
* Callback for create_box AJAX call.
*/
function createOrder(response) {
    if (response != 'False') {
        var orderNumber = response[0];
        window.location.href = "/orders/review/" + orderNumber; 
    }
}

/**
* Sets the event for clicking the remove button next to an item.
*/
function setRemoveButton() {
    $('.remove_item').click(function() {
        // Remove the row for the item.
        $(this).parent().parent().remove();
        
        // If there are no items, append the empty placeholder row.
        if ($('#items_added tr').length == 1) {
            $('#items_added').append(BLANK_ROW);
        }
    });
}

/**
 * Returns an array of the items that have been added to the box.
 */
function getAddedItems() {
    var items = [];
        
    // Go through each item in the table and add it to the items array. 
    // Each item is added as an array with the following format: 
    // [ item_name, item_expiration, item_count ]
    $('#boxes_added tr').each(function(index, element) {
        element = $(element);
        
        if (element.attr('id') != 'placeholder_row' && 
                element.attr('id') != 'table_header') {
            var itemInfo = element.children('td');
            var boxId = $(itemInfo[0]).html();
            
            items.push(boxId);
        }
    });
    return items;
}

/**
 * Returns true if all the required fields have been filled in, 
 * false if not. Does not check if item count is greater than 0.
 */
function requiredFieldsAreFilledIn() {
    var initials = $('input[name=initials]').val();
    var weight = $('input[name=weight]').val();
    var size = $('input[name=size]:checked').val();

    return (initials != '' && weight != '' && typeof(size) != 'undefined');
}

function goBack() {
    $('#stepTwo').hide();
    $('#stepOne').show();
    $('#stepNumber').html(1);
}

function goForward() {
  
  boxesToOrder = getAddedItems();
  
    if (boxesToOrder.length == 0) {
        $('#emptyBoxMessage').show();
    
        return;
    }
        
    $('#stepOne').hide();
    $('#stepTwo').show();
    $('#stepNumber').html(2);
    
    $('input[name=company').focus();
}

$(document).ready(function() {
    // This sets up the google-style autocomplete field.
    $('#itemSearch').autocomplete(
        {
            // The 'source' attribute is a function that is called 
            // which provides the data for the autocomplete. It passes 
            // in request, which provides the search query, and the response 
            // callback, which we are expected to give an array of relevant 
            // search results.
            source: function(request, response) {
                // Call the get_search_results AJAX function.
                Dajaxice.orders.get_search_results(function(returned) {
                    // 'returned' is passed to us from the AJAX function. 
                    // It is an array of relevant search results which we pass 
                    // to the 'response' callback.
                    response(returned);
                }, { 'query': request.term });
            },
            // This is just a setting so that the autocomplete plugin doesn't 
            // add any messages next to our search field.
            messages: {
                noResults: '',
                results: function() {}
            },
            // This is a callback that says what to do when the autocomplete 
            // dropdown is closed.
            close: function() {
                // This is the search result given by the AJAX function. 
                // It is of one of the following forms: 
                // Category > Box Name > Item
                // Category > Box Name
                // Category
                var query = $('#itemSearch').val();
                var actualQuery = query;
                
                // We want to get what the user was actually searching for, so we 
                // find last term after the last '> '.
                if (query.lastIndexOf('> ') != -1) {
                    actualQuery = query.substr(query.lastIndexOf('> ') + 2, query.length);
                }
                
                // Then we put the actual query back into the field.
                $('#itemSearch').val(actualQuery);
                
                // Here we want to split up the returned search result so 
                // we can find the category, box name, and item.
                var queryArray = query.split(' > ');
                var category = queryArray[0];
                var boxName = '';
                var item = '';
        var box = '';
                
                // If the array has two phrases, then it has a Category and 
                // Box Name, so we set the box name. We also set the boxNameToChoose 
                // so the box name can be autoselected in the list.
                if (queryArray.length > 1) {
                    boxName = queryArray[1];
                    boxNameToChoose = boxName;
                }
                
                // If it has three phrases, it also has an item so we 
                // can set the item name too. We also set the itemToChoose so 
                // the item can be autoselected in the list.
                if (queryArray.length > 2) {
                    item = queryArray[2];
                    itemToChoose = item;
                }
                
        //If it has four phrases, it also has a box_id so we can set the box_id too. 
        //We can set the boxToChoose tso the item can be autoselected in the list 
        if (queryArray.length > 3) { 
          box = queryArray[3];
          boxToChoose = item;
          $('#count').focus();
        }
        
                // Now we set the selected category in the list and trigger the 
                // change event for the categories list, so the box name field will be 
                // autopopulated and that will cascade down to the item list if necessary.
                $('#categories').val(category).change();
            }
        }
    );
    
    $('#itemSearch').focus();
    
    // Set the 'on change' event for the categories list.
    $('#categories').change(function() {
        var selectedCategory = $('#categories option:selected').val();
    
        // Get the list of box names for the selected category.
        Dajaxice.orders.get_box_names(getBoxNames, { 'category_name': selectedCategory });
    });
    
    // Set the 'on change' event for the box names list.
    $('#box_names').change(function() {
        var selectedBoxName = $('#box_names option:selected').val();
           
        // Get the list of items for the selected box name.
        Dajaxice.orders.get_items(getItems, { 'box_name': selectedBoxName });
    });
    
    // Set the 'on change' event for the items list.
    $('#items').change(function() {
        var selectedItemName = $('#items option:selected').val();
     
        // Get the list of items for the selected box name.
        Dajaxice.orders.get_box_ids(getBoxes, { 'item': selectedItemName });
    })
  
    // Set the 'on change' event for the boxes list.
    $('#boxes').change(function() {
        
    })
    
    // Set the 'on click' event for the add item button.
    $('#add_box').click(function(e) {
        // Prevent button from submitting form.
        e.preventDefault();
        
    var boxId = $('#boxes option:selected').val();
        
        
        // Remove the placeholder row if it's there.
        $('#placeholder_row').remove();
        
        // Reset the count and expiration fields.
        $('#count').val('');
        $('#expiration').val('');
        
        // Add the item to the list using the boxsAdded.
    
    Dajaxice.orders.get_info(getBoxInfo, {'boxid': boxId});

        $('#emptyBoxMessage').hide();
        
        // Set the remove button again. We need to do this every time we 
        // add another remove button.
        setRemoveButton();
    });
    
    $('#next').click(function(e) {
        e.preventDefault();
        
        goForward();
    });
    
    $('#back').click(function(e) {
        e.preventDefault();
       
        goBack();
    });
    
    $(document).keydown(function(e){
        if (e.keyCode == 37) {
            // left pressed
            
            goBack();
        } else if (e.keyCode == 39) {
            // right pressed
            
            goForward();
        }
    });
    
    $('input[name=company]').on('input', function() {
        $('input[name=company]').removeClass('requiredTextField');
        
        if (requiredFieldsAreFilledIn()) {
            $('#requiredFieldsMessage').hide();
        }
    });
    
    $('input[name=contact_name]').on('input', function() {
        $('input[name=contact_name]').removeClass('requiredTextField');
        
        if (requiredFieldsAreFilledIn()) {
            $('#requiredFieldsMessage').hide();
        }
    });
    
    $('input[name=phone_number]').change(function() {
        $('input[name=phone_number]').parent().removeClass('requiredText');
        
        if (requiredFieldsAreFilledIn()) {
            $('#requiredFieldsMessage').hide();
        }
    });
  
    $('input[name=email]').change(function() {
        $('input[name=email]').parent().removeClass('requiredText');
        
        if (requiredFieldsAreFilledIn()) {
            $('#requiredFieldsMessage').hide();
        }
    });
    
    // Set the 'on click' event for creating a box.
    $('#submit').click(function(e) {
        e.preventDefault();
        
        var company = $('input[name=company]').val();
        var missingRequired = false;
        
        // Required fields.
        var contact_name = $('input[name=contact_name]').val();
        if (contact_name == '') {
            $('input[name=contact_name]').addClass('requiredTextField');
            missingRequired = true;
        }
        
        // Can't have 0 items.
        if (items.length == 0) {
            // TODO: add some sort of alert
            return;
        }

        // Call the create_order AJAX function.
        Dajaxice.orders.create_order(createOrder,
            {
                'ship_to': contact_name,
                'reserved_for': contact_name,
                'box_ids': boxesToOrder
            }
        );
    });
});
