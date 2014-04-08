// because JS is weird and doesn't have a startsWith method
if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (str){
        return this.slice(0, str.length) == str;
    };
}

// Template for adding new item to the table.
var BOX_TEMPLATE = '<tr>' +
        '<td>{box_id}</td>' +
        '<td>{box_size}</td>' +
        '<td>{weight}</td>' +
        '<td class="priceRow">$ <input type="text" class="textField boxPrice" step="any" min="0" /></td>' +
        '<td><a class="remove_item" href="javascript:void(0)">Remove</a></td>' +
    '</tr>';

// Simple template used to insert a blank row below the table header
// when there are no items in the box.
var BLANK_ROW = '<tr id="placeholder_row">' +
                    '<td></td>' +
                    '<td></td>' +
                    '<td></td>' +
                    '<td>&nbsp;</td>' +
                '</tr>';

// Need these to update lists for box names and items.
var boxNameToChoose = '';
var itemToChoose = '';
var boxToChoose = '';
var boxesToOrder = [];
var boxesInOrder = [];

/**
* Function for getting a specific box information
*/

function getBoxInfo(response) {
    var boxId = response[2];
    var boxSize = response[1];
    var boxWeight = response[0];

    $('#boxes_added').append(
        BOX_TEMPLATE.replace('{box_id}', boxId)
            .replace('{box_size}', boxSize)
            .replace('{weight}', boxWeight + ' lbs')
    );

    $('#boxes_added tr td :input').unbind('input paste');
    $('#boxes_added tr td :input').bind('input paste', displayTotalPrice);

    displayTotalPrice();

    // Set the remove button again. We need to do this every time we
    // add another remove button.
    setRemoveButton();
}
/**
* Callback for get_box_names AJAX call.
*/
function getBoxNames(response) {
    setSelectedBox(false);

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
    setSelectedBox(false);

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

function boxIsInOrder(boxIdToAdd) {
    var boxesAdded = $('#boxes_added tr');

    for (var j = 0; j < boxesAdded.length; j++) {
        var element = $(boxesAdded[j]);

        if (element.attr('id') != 'placeholder_row' &&
                element.attr('id') != 'table_header') {
            var boxInfo = element.children('td');
            var boxId = $(boxInfo[0]).html();

            if (boxId == boxIdToAdd) {
                return true;
            }
        }
    }

    return false;
}

/**
* Callback for the get_items AJAX call. Does the same things as
* the getItems callback, just for Boxes instead.
*/
function getBoxes(response) {
    setSelectedBox(false);

    $('#boxes').empty();

    for (var i = 0; i < response.length; i++) {
        var boxAlreadyInUse = false;
        var boxIdToAdd = response[i];

        if (!boxIsInOrder(boxIdToAdd)) {
            $('#boxes').append('<option>' + boxIdToAdd + '</option>');
        }
    }

    if (boxToChoose !== '') {
        var splitBoxName = boxToChoose.split(' ');
        boxToChoose = splitBoxName[1];
        $('#boxes').val(boxToChoose);
        boxToChoose = '';
        $('#boxes').change();
    }
}

/**
* Callback for the get_items AJAX call. Does the same things as
* the getItems callback, just for Boxes instead.
*/
function getBoxDetails(response) {
    var box_weight = response[0];
    var box_size = response[1];
    var box_id = response[2];
    var box_contents = response[3];
    var box_expires = response[4];

    $('#boxDetails').html('<p class="sizeLabel">Size</p><p class="size">' + box_size + '</p>' +
        '<p class="weightLabel">Weight</p><p class="weight">' + box_weight + ' lbs</p>' +
        '<p class="contentsLabel">Contents</p><p class="contents">' + box_contents + '</p>' +
        '<p class="expiresLabel">Expires</p><p class="expires">' + box_expires + '</p>');
}

/**
* Callback for create_box AJAX call.
*/
function createOrder(response) {
    orderNumber = response.order_number;
    $('#create_box_link').attr('href', '/inventory/create/' + orderNumber);
}

/**
* Sets the event for clicking the remove button next to an item.
*/
function setRemoveButton(){
    $('.remove_item').unbind('click').click(function() {
        // Remove the row for the item.
        var id = $(this).parent().children([0]).text();
        $(this).parent().parent().remove();

        // If there are no items, append the empty placeholder row.
        if ($('#boxes_added tr').length == 1) {
            $('#boxes_added').append(BLANK_ROW);
        }

        var selectedItemName = $('#items option:selected').val();
        var selectedBoxName = $('#box_names option:selected').val();
        boxesInOrder.splice(boxesInOrder.indexOf(id),1);
        
        if (selectedItemName !== '') {
            Dajaxice.inventory.get_boxes_with_item(setTableList, { 'item_name': selectedItemName,'box_name' : selectedBoxName });
        }
    });
}

/**
 * Returns an array of the items that have been added to the box.
 */
function getAddedBoxes() {
    var boxes = [];

    // Go through each item in the table and add it to the items array.
    // Each item is added as an array with the following format:
    // [ item_name, item_expiration, item_count ]
    $('#boxes_added tr').each(function(index, element) {
        element = $(element);

        if (element.attr('id') != 'placeholder_row' &&
                element.attr('id') != 'table_header') {
            var itemInfo = element.children('td');
            var boxId = $(itemInfo[0]).html();

            boxes.push(boxId);
        }
    });

    return boxes;
}

function goBack() {
    if (stepNum == 1) {
        return;
    } else if (stepNum == 2) {
        stepNum--;
        $('#stepTwo').hide();
        $('#stepOne').show();
        $('#contact_name').focus();
        $('#stepNumber').html(stepNum);
    }
}

function goForward() {
    if (stepNum == 1) {
        stepNum++;

        $('#stepOne').hide();
        $('#stepTwo').show();
        $('#itemSearch').focus();
        $('#stepNumber').html(stepNum);
    } else if (stepNum == 2) {
        return;
    }
}

function setSelectedBox(selectedBox, clearBoxes) {
    clearBoxes = (typeof(clearBoxes) == 'undefined') ? true : clearBoxes;

    if (selectedBox !== false) {
        $('#itemSelectedMessage').html('You have selected Box ' + selectedBox + '.');
        $('#itemSelectedMessage').removeClass('noItemSelected');
        $('#itemSelectedMessage').addClass('itemSelected');
    } else {
        $('#itemSelectedMessage').html('Please select a box.');
        $('#itemSelectedMessage').removeClass('itemSelected');
        $('#itemSelectedMessage').addClass('noItemSelected');

        if (clearBoxes) {
            $('#boxes').empty();
        }

        $('#boxDetails').html('');
    }
}

function displayTotalPrice() {
    var totalPrice = 0.0;

    $('#boxes_added tr td :input').each(function() {
        var price = 0.00;
        var rawValue = $(this).val();

        if (isNaN(rawValue) && rawValue !== '') {
            $(this).addClass('requiredTextField');
            return;
        } else if (rawValue !== '') {
            price = parseFloat(rawValue);
        }

        totalPrice += price;
        $(this).removeClass('requiredTextField');
    });

    $('#totalPrice').html(totalPrice.toFixed(2));
}

function pricesHaveErrors() {
    var hasErrors = false;

    $('#boxes_added tr td :input').each(function() {
        var rawValue = $(this).val();

        if (isNaN(rawValue) && rawValue !== '') {
            hasErrors = true;
            return false;
        }
    });

    return hasErrors;
}

function autofillCustomerInfo(contactName, orgName) {
    Dajaxice.orders.get_customer_info(function(returned) {
        if (returned == 'False') {
            $('#shippingAddressesWrapper').html('<i>no shipping addresses saved</i>');
            return;
        }

        var contactEmail = returned.contact_email;
        var orgAddress = returned.organization_address;
        var shippingAddresses = returned.shipping_addresses;

        if (shippingAddresses.length > 0) {
            $('#shippingAddressesWrapper').html('<select id="shippingAddresses"></select>');

            for (var i = 0; i < shippingAddresses.length; i++) {
                var shippingAddress = shippingAddresses[i];

                $('#shippingAddresses').append('<option value="' + shippingAddress + '">' +
                    shippingAddress + '</option');
            }
        } else {
            $('#shippingAddressesWrapper').html('<i>no shipping addresses saved</i>');
        }

        $('#contact_email').val(contactEmail).removeClass('requiredTextField');

        $('#organization_name').val(orgName).removeClass('requiredTextField');

        $('#organization_address').val(orgAddress).removeClass('requiredTextField');
    }, { 'contact_name': contactName, 'organization_name': orgName });
}

function get_selected_boxes(){
    var boxes = get_current_boxes();
    var selected_boxes = [];
    for(var i=0;i<boxes.length;i++){
        if(boxes[i].check !== ''){
            selected_boxes.push(boxes[i].box_id);
            }
        }
    return selected_boxes;
}

function remove_selected_rows(){
    var boxes = get_current_boxes();
    var selected_rows = [];
    for(var i=0;i<boxes.length;i++){
        if(boxes[i].check !== ''){
            boxes.splice(i,1);
            i--;
        }
    }
}

function addSingleBox(response){
    currentBoxes.length = 0;
    currentBoxes.push(new boxRow(response[0],
        response[1],
        response[2],
        response[3],
        response[4],
        response[5],
        response[6]
    ));
    showTable();
}

function setTableList(response) {
    currentBoxes.length = 0;
    for(var i=0;i<response.length;i++){
        if(boxesInOrder.indexOf(response[i][0]) === -1){
            currentBoxes.push(new boxRow(response[i][0],
            response[i][1],
            response[i][2],
            response[i][3],
            response[i][4],
            response[i][5],
            response[i][6]
            ));
        }

    }
    showTable();
}

function checkBoxClick(row){
    var boxes;
    if(filtered){
        boxes = filteredBoxes;
    }
    else{
        boxes = currentBoxes;
    }
    if (boxes[row].check === ''){
        boxes[row].check = 'checked';
        setSelectedBox(get_selected_boxes().join(' , '));
        if(filteredBoxes.indexOf(boxes[row]) === -1){
            filteredBoxes.push(currentBoxes[row]);
        }      
    }
    else{
        boxes[row].check = '';
        box_ids = get_selected_boxes();
        if(box_ids.length != 0){
            setSelectedBox(get_selected_boxes().join(' , '));
        }
        else{
            setSelectedBox(false);
        }
    }
}

$(document).ready(function() {
    setRemoveButton();
    $('#boxes_added tr td :input').bind('input paste', displayTotalPrice);

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
                    var toRemove = [];

                    for (var i = 0; i < returned.length; i++) {
                        if (returned[i].startsWith('Box')) {
                            var box = returned[i].split(' ');
                            var boxId = box[1];

                            if (boxIsInOrder(boxId)) {
                                toRemove.push(i);
                            }
                        }
                    }

                    for (var i = 0; i < toRemove.length; i++) {
                        returned.splice(toRemove[i], 1);
                    }

                    toRemove.length = 0;

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

    $('#contact_name').autocomplete(
        {
            autoFocus: true,
            source: function(request, response) {
                Dajaxice.orders.get_customer_search_results(function(returned) {
                    response(returned);
                }, { 'query': request.term });
            },
            messages: {
                noResults: '',
                results: function() {}
            },
            close: function() {
                // This is the search result given by the AJAX function.
                // It is of the form:
                // Customer (Organization)
                var query = $('#contact_name').val();
                var splitQuery = query.split(' (');
                var contactName = splitQuery[0];

                $('#contact_name').val(contactName).removeClass('requiredTextField');

                if (splitQuery.length < 2) {
                    $('#shippingAddressesWrapper').html('<i>no shipping addresses saved</i>');
                    return;
                }

                var orgName = splitQuery[1].substring(0, splitQuery[1].length - 1);

                autofillCustomerInfo(contactName, orgName);
            }
        }
    );

    $('#contact_name').focus();

    // Set the 'on change' event for the categories list.
    $('#categories').change(function() {
        var selectedCategory = $('#categories option:selected').val();

        // Get the list of box names for the selected category.
        Dajaxice.orders.get_box_names(getBoxNames, { 'category_name': selectedCategory });
        setSelectedBox(false);
    });

    // Set the 'on change' event for the box names list.
    $('#box_names').change(function() {
        var selectedBoxName = $('#box_names option:selected').val();

        // Get the list of items for the selected box name.
        Dajaxice.orders.get_items(getItems, { 'box_name': selectedBoxName });
        setSelectedBox(false);
    });

    // Set the 'on change' event for the items list.
    $('#items').change(function() {
        var selectedItemName = $('#items option:selected').val();

        // Get the list of items for the selected box name.
        //Dajaxice.orders.get_box_ids(getBoxes, { 'item': selectedItemName });
        var selectedItemName = $('#items option:selected').val();
        var selectedBoxName = $('#box_names option:selected').val();
        Dajaxice.inventory.get_boxes_with_item(setTableList, { 'item_name': selectedItemName,'box_name' : selectedBoxName });
        setSelectedBox(false);
    });

    // Set the 'on change' event for the boxes list.
    $('#boxes').change(function() {
        var selectedBoxId = $('#boxes option:selected').val();
        
        setSelectedBox(selectedBoxId);

        // Get the details of the box for the selected box id.
        Dajaxice.orders.get_info(getBoxDetails, {'boxid': selectedBoxId});
    });

    // Set the 'on change' event for the box details list.
    $('#boxDetails').change(function() {

    });

    // Set the 'on click' event for the add item button.
    $('#add_box').click(function(e) {
        // Prevent button from submitting form.
        e.preventDefault();
        
        var boxIds = get_selected_boxes();
        
        // Remove the placeholder row if it's there.
        $('#placeholder_row').remove();

        var boxes = get_current_boxes();
        // Add the items to the list using the boxsAdded.
        for(var i = 0;i<boxIds.length;i++){
            boxesInOrder.push(boxIds[i]);
            Dajaxice.orders.get_info(getBoxInfo, {'boxid': boxIds[i]});
        }
        remove_selected_rows();
        showTable();
        
        setSelectedBox(false, false);

        $('#emptyBoxMessage').hide();
    });

    $('.next').click(function(e) {
        e.preventDefault();

        if (!$(this).hasClass('createButton')) {
            goForward();
        }
    });

    $('.back').click(function(e) {
        e.preventDefault();

        goBack();
    });

    $('#contact_name').bind('keyup input paste', function() {
        $('#contact_name').removeClass('requiredTextField');
    });

    $('#contact_email').bind('keyup input paste', function() {
        $('#contact_email').removeClass('requiredTextField');
    });

    $('#organization_name').bind('keyup input paste', function() {
        $('#organization_name').removeClass('requiredTextField');
    });

    $('#same_as_business').change(function() {
        if ($(this).is(':checked')) {
            $('#shipping_address').attr('disabled', 'disabled');
            $('#shipping_address').css('opacity', '0.5');
            $('#shipping_address').val($('#organization_address').val());
        } else {
            $('#shipping_address').css('opacity', '1');
            $('#shipping_address').removeAttr('disabled');
        }
    });

    $('#organization_address').bind('input propertychange', function() {
        $('#organization_address').removeClass('requiredTextField');

        if ($('#same_as_business').is(':checked')) {
            $('#shipping_address').removeClass('requiredTextField');
            $('#shipping_address').val($('#organization_address').val());
        }
    });

    $('#shipping_address').bind('input propertychange', function() {
        $('#shipping_address').removeClass('requiredTextField');
    });

    $('.createButton').click(function() {
        var missingRequired = false;

        // Required fields.
        var contact_name = $('#contact_name').val();
        if (contact_name === '') {
            $('#contact_name').addClass('requiredTextField');
            missingRequired = true;
        }

        var contact_email = $('#contact_email').val();
        if (contact_email === '') {
            $('#contact_email').addClass('requiredTextField');
            missingRequired = true;
        }

        var organization_name = $('#organization_name').val();
        if (organization_name === '') {
            $('#organization_name').addClass('requiredTextField');
            missingRequired = true;
        }

        var organization_address = $('#organization_address').val();
        if (organization_address === '') {
            $('#organization_address').addClass('requiredTextField');
            missingRequired = true;
        }

        var new_shipping_address = $('#shipping_address').val();
        var shipping_address = '';

        if ($('#shippingAddressesWrapper').html() !== '<i>no shipping addresses saved</i>') {
            shipping_address = $('#shippingAddresses option:selected').val();
        }

        if (missingRequired) {
            return;
        }

        // Call the create_order AJAX function.
        Dajaxice.orders.create_order(createOrder,
            {
                'customer_name': contact_name,
                'customer_email': contact_email,
                'business_name':  organization_name,
                'business_address': organization_address,
                'new_shipping_address': new_shipping_address,
                'shipping_address': shipping_address,
                'order_number': orderNumber
            }
        );

        if ($('#shippingAddressesWrapper').html() !== '<i>no shipping addresses saved</i>' &&
                new_shipping_address !== '') {
            $('#shippingAddressesWrapper').append('<option value="' + new_shipping_address +
                '" selected="selected">' + new_shipping_address + '</option>');
        } else if (new_shipping_address !== '') {
            $('#shippingAddressesWrapper').html('<select id="shippingAddresses"></select>');
            $('#shippingAddresses').append('<option value="' + new_shipping_address +
                '">' + new_shipping_address + '</option>');
        }

        $('.createButton').val('Save Order \u2192');

        goForward();
    });

    // Set the 'on click' event for creating a box.
    $('#submit').click(function(e) {
        e.preventDefault();

        if (pricesHaveErrors()) {
            return;
        }

        var price = $('#price').val();

        if (price !== '') {
            price = parseFloat(price).toFixed(2);
        }

        var boxes = {};

        $('#boxes_added tr').each(function(index, element) {
            element = $(element);

            if (element.attr('id') != 'placeholder_row' &&
                    element.attr('id') != 'table_header') {
                var boxInfo = element.children('td');
                var boxId = $(boxInfo[0]).html();
                var boxPrice = $($(boxInfo[3]).children('input')[0]).val();

                boxes[boxId] = boxPrice;
            }
        });

        Dajaxice.orders.add_boxes_to_order(
            function(returned) {
                console.log(returned);
                if (returned.result == 1) {
                    window.location = '/orders/review/' + orderNumber;
                }
            },
            {
                'order_number': orderNumber,
                'boxes': boxes,
                'custom_price': price
            }
        );
    });
});
