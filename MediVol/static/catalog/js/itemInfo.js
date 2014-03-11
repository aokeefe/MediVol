function hideEditControls() {
    $('#saveItem').hide();
    $('#cancelEdit').hide();
    $('#deleteItem').hide();
    $('#editItem').show();

    $('#itemNameValue').show();
    $('#boxNameValue').show();
    $('#descriptionValue').show();

    $('#name').hide();
    $('#boxName').hide();
    $('#description').hide();
}

function showEditControls() {
    $('#saveItem').show();
    $('#cancelEdit').show();
    $('#deleteItem').show();
    $('#editItem').hide();

    $('#itemNameValue').hide();
    $('#boxNameValue').hide();
    $('#descriptionValue').hide();

    $('#name').show();
    $('#boxName').show();
    $('#description').show();
}

function saveItem() {
    var categoryLetter = $('#categoryLetter').val();
    var oldItemName = $('#itemNameValue').html();
    var name = $('#name').val();
    var oldBoxName = $('#boxNameValue').html();
    var boxName = $('#boxName').val();
    var description = $('#description').val();

    var badOldBoxName = oldBoxName + ' does not exist';
    var badBoxName = boxName + ' does not exist';
    var badOldItemName = oldItemName + ' could not be found';
    var itemAlreadyExists = name + ' already exists';
    var expected = name + ' has been changed';

    Dajaxice.catalog.edit_item(
        function(returned) {
            if (returned.message === badOldBoxName) {
                $('.requiredMessage').html('Box Name "' + oldBoxName + '" does not exist.');
                $('.requiredMessage').show();
            } else if (returned.message === badBoxName) {
                $('.requiredMessage').html('Box Name "' + boxName + '" does not exist.');
                $('.requiredMessage').show();
            } else if (returned.message === badOldItemName) {
                $('.requiredMessage').html('Item "' + oldItemName + '" does not exist.');
                $('.requiredMessage').show();
            } else if (returned.message === itemAlreadyExists) {
                $('.requiredMessage').html('Item "' + name + '" already exists.');
                $('.requiredMessage').show();
            } else if (returned.message === expected) {
                window.location.reload();
            }
        },
        {
            'category_letter': categoryLetter,
            'new_box_name': boxName,
            'old_box_name': oldBoxName,
            'new_item_name': name,
            'old_item_name': oldItemName,
            'd': description
        }
    );
}

function discardChanges() {
    $('#name').val($('#itemNameValue').html());
    $('#boxName').val($('#boxNameValue').html());

    var description = $('#description').html();

    if (description !== '<i>no description</i>') {
        $('#description').val(description);
    } else {
        $('#description').val('');
    }
}

function deleteItem() {
    var item = $('#itemNameValue').html();
    var boxName = $('#boxNameValue').html();
    var expected = item + ' has been deleted';

    Dajaxice.catalog.delete_item(function(returned) {
        if (returned.message === expected) {
            window.location = '/catalog/';
        } else {
            // TODO: error message
        }
    }, { 'b_name': boxName, 'item_name': item });
}

$(document).ready(function() {
    // This sets up the google-style autocomplete field.
    $('#boxName').autocomplete(
        {
            autoFocus: true,
            // The 'source' attribute is a function that is called
            // which provides the data for the autocomplete. It passes
            // in request, which provides the search query, and the response
            // callback, which we are expected to give an array of relevant
            // search results.
            source: function(request, response) {
                // Call the get_search_results AJAX function.
                Dajaxice.catalog.search_box_names(function(returned) {
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
                // It is of the form:
                // Category > Box Name
                var query = $('#boxName').val();
                var actualQuery = query;

                // We want to get what the user was actually searching for, so we
                // find last term after the last '> '.
                if (query.lastIndexOf('> ') != -1) {
                    actualQuery = query.substr(query.lastIndexOf('> ') + 2, query.length);
                }

                // Then we put the actual query back into the field.
                $('#boxName').val(actualQuery);
            }
        }
    );

    $('#editItem').click(function() {
        showEditControls();
    });

    $('#saveItem').click(function() {
        saveItem();
    });

    $('#cancelEdit').click(function() {
        hideEditControls();
        discardChanges();
    });

    $('.deleteDialog').easyconfirm({ dialog: $('#deleteQuestion') });
    $('.deleteDialog').click(function() {
        deleteItem();
    });

    $('#expandBoxes').click(function() {
        $('#boxes').slideToggle();

        if ($(this).html() === '[+]') {
            $(this).html('[-]');
        } else {
            $(this).html('[+]');
        }
    });

    $('#expandOrders').click(function() {
        $('#orders').slideToggle();

        if ($(this).html() === '[+]') {
            $(this).html('[-]');
        } else {
            $(this).html('[+]');
        }
    });
});
