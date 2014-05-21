// because JS is weird and doesn't have a startsWith method
if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (str){
        return this.slice(0, str.length) == str;
    };
}

// Need these to update lists for box names and items.
var boxNameToChoose = '';
var itemToChoose = '';

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


$(document).ready(function() {
    // This sets up the google-style autocomplete field.
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
                Dajaxice.orders.get_search_results(function(returned) {

                    for (var i = 0; i < returned.length; i++) {
                        if (returned[i].startsWith('Box')) {
                            var box = returned[i].split(' ');
                            var boxId = box[1];
                        }
                    }

                    // 'returned' is passed to us from the AJAX function.
                    // It is an array of relevant search results which we pass
                    // to the 'response' callback.
                    response(returned);
                }, { 'query': request.term, 'for_inventory': true });
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

                // If it has four phrases, it also has a box_id so we can set the box_id too.
                // We can set the boxToChoose to the item can be autoselected in the list.
                if (queryArray.length > 3) {
                    box = queryArray[3];
                    boxToChoose = box;
                }

                // Now we set the selected category in the list and trigger the
                // change event for the categories list, so the box name field will be
                // autopopulated and that will cascade down to the item list if necessary.
                if (!category.startsWith('Box')) {
                    $('#categories').val(category).change();
                } else {
                    box = category.split(' ');
                    var boxId = box[1];
                    Dajaxice.inventory.get_box_by_id(addSingleBox, { 'box_id': boxId });
                }
            }
        }
    );

    $('#itemSearch').focus();

    // Set the 'on change' event for the categories list.
    $('#categories').change(function() {
        var selectedCategory = $('#categories option:selected').val();

        // Get the list of box names for the selected category.
        Dajaxice.orders.get_box_names(getBoxNames, { 'category_name': selectedCategory });

        if (boxNameToChoose === '' && itemToChoose === '') {
            Dajaxice.inventory.get_boxes_with_category(setTableList, {'category_name': selectedCategory });
        }
    });

    // Set the 'on change' event for the box names list.
    $('#box_names').change(function() {
        var selectedBoxName = $('#box_names option:selected').val();

        // Get the list of items for the selected box name.
        Dajaxice.orders.get_items(getItems, { 'box_name': selectedBoxName });

        if (itemToChoose === '') {
            Dajaxice.inventory.get_boxes_with_box_name(setTableList, {'box_name' : selectedBoxName });
        }
    });

    // Set the 'on change' event for the items list.
    $('#items').change(function() {
        var selectedItemName = $('#items option:selected').val();
        var selectedBoxName = $('#box_names option:selected').val();
        Dajaxice.inventory.get_boxes_with_item(setTableList, { 'item_name': selectedItemName,'box_name' : selectedBoxName });
    });
});
