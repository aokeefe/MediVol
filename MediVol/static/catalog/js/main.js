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

    $('#item_details').click(function(e) {
        e.preventDefault();
        var win = window.open('/catalog/item_info/' + response.item_id, '_blank');
        win.focus();
    });

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
    // Set the 'on change' event for the categories list.
    $('#categories').change(function() {
        setItemNotSelected();
        $('#boxNameField').html('<i>choose a box name above</i>');
        var selectedCategory = $('#categories option:selected').val();
        if(selectedCategory !== undefined) {
            // Get the list of box names for the selected category.
            Dajaxice.inventory.get_box_names(getBoxNames, { 'category_name': selectedCategory.split(" - ")[1] });
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
