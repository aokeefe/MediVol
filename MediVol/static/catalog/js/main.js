// Need these to update lists for box names and items.
var boxNameToChoose = '';
var itemToChoose = '';

var selected_category = '';
var selected_box_name = '';


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
    if (boxNameToChoose !== '') {
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

    if (itemToChoose !== '') {
        $('#items').val(itemToChoose);
        itemToChoose = '';
        $('#items').change();
    }
}

/**
* Callback for the create_items AJAX call.
*/
function createItem(response){
    if(response.success == 1) {
        setChangeMessageSuccess(response.message);
        $('#item_input').val('');
        $('#item_description').val('');
        Dajaxice.inventory.get_items(getItems, { 'box_name': $('#box_names option:selected').val() });
    } else {
        setChangeMessageError(response.message);
    }
}

function updateDescription(response){
    var category = $('#categories option:selected').val();
    var boxName = $('#box_names option:selected').val();
    var item = $('#items option:selected').val();
    var description = response.message;

    /*$('#item_details').unbind('click');
    $('#item_details').click(function(e) {
        e.preventDefault();
        var win = window.open('/catalog/item_info/' + response.item_id, '_blank');
        win.focus();
    });*/

    $('#item_details').parent().attr('href', '/catalog/item_info/' + response.item_id);
    $('#item_details').show();

    $('#category').html(category);
    $('#boxName').html(boxName);

    if (description === '') {
        $('#description').html('<i>no description</i>');
    } else {
        $('#description').html(description);
    }
}

//display success massage when new item is created
function setChangeMessageSuccess(message) {
    $('#changeMessage').html(message);
    $('#changeMessage').show();
}

//display error massage when new item can not be created
function setChangeMessageError(message) {
    $('#changeMessage').html(message);
    $('#changeMessage').show();
}

//clear the message
function setChangeMessageClear() {
    $('#changeMessage').html('');
    $('#changeMessage').hide();
}


function setItemSelected(itemName) {
    $('#itemSelectedMessage').removeClass('noItemSelected');
    $('#itemSelectedMessage').addClass('itemSelected');
    $('#itemSelectedMessage').html('You have selected: <br /><b>' + itemName + '</b>');
}

function setItemNotSelected() {
    $('#itemSelectedMessage').removeClass('itemSelected');
    $('#itemSelectedMessage').addClass('noItemSelected');
    $('#itemSelectedMessage').html('Please select an item.');

    $('#item_details').hide();

    $('#category').html('');
    $('#boxName').html('');
    $('#description').html('');
}

$(document).ready(function() {
    // This sets up the google-style autocomplete field.
    $('#itemSearch').autocomplete(
        {
            autoFocus: true,
            // The 'source' attribute is a function that is called
            // which provides the data for the autocomplete. It passes
            // in request, which provides the search query, and the response
            // callback, which we are expected to give an array of relevant
            // search results.
            source: function(request, response) {
                // Call the get_search_results AJAX function.
                Dajaxice.inventory.get_search_results(function(returned) {
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
        setItemNotSelected();
        $('#boxNameField').html('<i>choose a box name above</i>');
        var selectedCategory = $('#categories option:selected').val();
        if(selectedCategory !== undefined) {
            // Get the list of box names for the selected category.
            Dajaxice.inventory.get_box_names(getBoxNames, { 'category_name': selectedCategory });
        }
    });

    // Set the 'on change' event for the box names list.
    $('#box_names').change(function() {
        setItemNotSelected();
        var selectedBoxName = $('#box_names option:selected').val();
        if(selectedBoxName !== undefined) {
            $('#boxNameField').html(selectedBoxName);
            // Get the list of items for the selected box name.
            Dajaxice.inventory.get_items(getItems, { 'box_name': selectedBoxName });
        }
    });

    // Set the 'on change' event for the items list.
    $('#items').change(function() {
        var selectedItem = $('#items option:selected').val();

        if(selectedItem !== undefined) {
            setItemSelected(selectedItem);
            var box_name = $('#box_names option:selected').val();

            Dajaxice.catalog.get_description(updateDescription,
                {
                    'box_name': box_name,
                    'item_name': selectedItem,
                }
            );
        }
    });

    //on click event for creating a new item
    $('#add_new_item').click(function(e) {
        e.preventDefault();
        var name = $('#item_input').val();
        var box_name = $('#box_names option:selected').val();
        var description = $('#item_description').val();

        if (box_name === undefined) {
            box_name = '';
        }

        if (name === '' || box_name === '') {
            setChangeMessageError('Box Name and item name are required.');
            return;
        }

        Dajaxice.catalog.create_item(createItem,
            {
                'box_name': box_name,
                'item_name': name,
                'description': description
            }
        );

    });
});
