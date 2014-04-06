// Template for adding new item to the table.
var ITEM_TEMPLATE = '<tr>' +
        '<td>{category}</td>' +
        '<td>{box_name}</td>' +
        '<td>{item}</td>' +
        '<td>{expiration}</td>' +
        '<td>{count}</td>' +
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
* Callback for create_box AJAX call.
*/
function createBox(response) {
    if (response != 'False') {
        var iframe = document.createElement('iframe');
        var html = '<head><script type"text/javascript">window.print();</script></head>' +
                '<body>' + response.label + '</body>';
        iframe.src = 'data:text/html;charset=utf-8,' + encodeURI(html);
        iframe.width = 0;
        iframe.height = 0;
        document.body.appendChild(iframe);

        var orderId = $('#orderId').val();

        setTimeout(function() {
            if (orderId === '0') {
                location.reload();
            } else {
                window.location = '/orders/create/' + orderId + '/2/' + response.box_id;
            }
        }, 1);
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
    $('#items_added tr').each(function(index, element) {
        element = $(element);

        if (element.attr('id') != 'placeholder_row' &&
                element.attr('id') != 'table_header') {
            var itemInfo = element.children('td');
            var itemName = $(itemInfo[2]).html();
            var boxName = $(itemInfo[1]).html();
            var expiration = $(itemInfo[3]).html();
            var count = 0;

            if ($(itemInfo[4]).html() != 'No count') {
                count = $(itemInfo[4]).html();
            }

            if (expiration != 'Never') {
                console.log(expiration);
                var expirationArray = expiration.split('/');
                expiration = expirationArray[1] + '-' + expirationArray[0] + '-01';
            }

            items.push([ itemName, expiration, count, boxName ]);
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
    if (getAddedItems().length == 0) {
        $('#emptyBoxMessage').html('Cannot create an empty box.');
        $('#emptyBoxMessage').show();
        $('html, body').animate({
            scrollTop: $('#emptyBoxMessage').offset().top
        }, 500);

        return;
    }

    $('#stepOne').hide();
    $('#stepTwo').show();
    $('#stepNumber').html(2);

    $('input[name=initials').focus();
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
        var selectedCategory = $('#categories option:selected').val();

        setItemNotSelected();

        // Get the list of box names for the selected category.
        Dajaxice.inventory.get_box_names(getBoxNames, { 'category_name': selectedCategory });
    });

    // Set the 'on change' event for the box names list.
    $('#box_names').change(function() {
        var selectedBoxName = $('#box_names option:selected').val();

        setItemNotSelected();

        // Get the list of items for the selected box name.
        Dajaxice.inventory.get_items(getItems, { 'box_name': selectedBoxName });
    });

    // Set the 'on change' event for the items list.
    $('#items').change(function() {
        setItemSelected($('#items option:selected').val());
    });

    var expirationCleared = false;

    $('#expiration').click(function() {
        if (expirationCleared) {
            expirationCleared = false;
            return;
        }

        var date = $('#expiration').val();
        if (date == '') {
            var datePlusOneYear = new Date();
            datePlusOneYear.setYear(datePlusOneYear.getFullYear() + 1);

            var newDateString = datePlusOneYear.getFullYear() + '-' +
                    ('0' + (datePlusOneYear.getMonth() + 1)).slice(-2);

            $('#expiration').val(newDateString);
        }
    });

    $('#expiration').change(function() {
        if ($('#expiration').val() == '') {
            expirationCleared = true;
        }
    });

    // Set the 'on click' event for the add item button.
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
                typeof(item) == 'undefined') {
            return;
        }

        if (count < 0) {
            $('#emptyBoxMessage').html('Item count cannot be less than zero.');
            $('#emptyBoxMessage').show();
            $('html, body').animate({
                scrollTop: $('#emptyBoxMessage').offset().top
            }, 500);
            return;
        }

        if (count == '' || count == 0) {
            count = 'No count';
        }

        if (expiration != 'Never') {
            var expirationArray = expiration.split('-');
            expiration = expirationArray[1] + '/' + expirationArray[0];
        }

        // Remove the placeholder row if it's there.
        $('#placeholder_row').remove();

        // Reset the count and expiration fields.
        $('#count').val('');
        $('#expiration').val('');

        // Add the item to the list using the ITEM_TEMPLATE.
        $('#items_added').append(
            ITEM_TEMPLATE.replace('{category}', category)
                .replace('{box_name}', boxName)
                .replace('{item}', item)
                .replace('{expiration}', expiration)
                .replace('{count}', count)
        );

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

    $('input[name=initials]').on('input', function() {
        $('input[name=initials]').removeClass('requiredTextField');

        if (requiredFieldsAreFilledIn()) {
            $('#requiredFieldsMessage').hide();
        }
    });

    $('input[name=weight]').on('input', function() {
        $('input[name=weight]').removeClass('requiredTextField');

        if (requiredFieldsAreFilledIn()) {
            $('#requiredFieldsMessage').hide();
        }
    });

    $('input[name=size]').change(function() {
        $('input[name=size]').parent().removeClass('requiredText');

        if (requiredFieldsAreFilledIn()) {
            $('#requiredFieldsMessage').hide();
        }
    });

    // Set the 'on click' event for creating a box.
    $('#submit').click(function(e) {
        e.preventDefault();

        var initials = $('input[name=initials]').val();
        var weight = $('input[name=weight]').val();
        var size = $('input[name=size]:checked').val();
        var note = $('textarea[name=note]').val();
        var missingRequired = false;

        // Required fields.
        if (initials == '') {
            $('input[name=initials]').addClass('requiredTextField');
            missingRequired = true;
        }

        if (weight == '') {
            $('input[name=weight]').addClass('requiredTextField');
            missingRequired = true;
        }

        if (typeof(size) == 'undefined') {
            $('input[name=size]').parent().addClass('requiredText');
            missingRequired = true;
        }

        if (missingRequired) {
            $('#requiredFieldsMessage').show();
            return;
        }

        var items = getAddedItems();

        // Can't have 0 items.
        if (items.length == 0) {
            return;
        }

        // Call the create_box AJAX function.
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
