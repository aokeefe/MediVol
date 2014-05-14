// because JS is weird and doesn't have a startsWith method
if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (str){
        return this.slice(0, str.length) == str;
    };
}

// Template for adding new item to the table.
var ITEM_TEMPLATE = '<tr>' +
        '<td class="tagColumn">{tags}</td>' +
        '<td>{box_id}</td>' +
        '<td>{size}</td>' +
        '<td>{weight}</td>' +
        '<td>{contents}</td>' +
        '<td>{expiration}</td>' +
        '<td>{warehouse}</td>' +
        '<td><input type="checkbox" onclick="checkBoxClick({row})" {check}></td>' +
    '</tr>';

var ORDER_TAG_TEMPLATE = '<a class="orderTag" href="/orders/review/{order_id}"' +
    ' target="_blank">Order {order_id}</a>';

// Simple template used to insert a blank row below the table header
// when there are no items in the box.
var BLANK_ROW = "<tr id='placeholder_row'>" +
                    "<td class='tagColumn'></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td>&nbsp;</td>" +
                "</tr>";

var WAREHOUSE_SELECT = '<select id="{id}" class="warehouseChange"' +
    ' onchange="warehouseChange({row},&quot;{id}&quot;)">{options}</select>';

// Need these to update lists for box names and items.
var boxNameToChoose = '';
var itemToChoose = '';

var currentBoxes = [];
var filteredBoxes = [];
var currentSort = '';
var currentPage = 0;
var maxPerPage = $('#max_per_page option:selected').text();
var filtered = false;

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

function setWarehouses(response){
    var warehouses = '';

    for (var i = 0; i < response.length; i++) {
        warehouses = warehouses + '<option>' + response[i] + '</option>';
    }

    WAREHOUSE_SELECT = WAREHOUSE_SELECT.replace('{options}',warehouses);
}

//object to represent one row in the table
function boxRow(box_id, size, weight, contents, expiration, warehouse, order_id){
    this.box_id = box_id;
    this.contents = contents;
    this.expiration = expiration;
    this.size = size;
    this.weight = weight;
    this.warehouse = warehouse;
    this.order_id = order_id;
    this.check = '';
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

    for (var i = 0; i < response.length; i++){
        currentBoxes.push(new boxRow(response[i][0],
            response[i][1],
            response[i][2],
            response[i][3],
            response[i][4],
            response[i][5],
            response[i][6]
        ));
    }

    showTable();
}

function showTable() {
    var boxes;

    if (filtered) {
        boxes = filteredBoxes;
    } else {
        boxes = currentBoxes;
    }

    if (boxes.length > maxPerPage) {
        fillTable(boxes.slice(currentPage*maxPerPage,currentPage*maxPerPage+maxPerPage));
    } else {
        fillTable(boxes);
    }

    $('#page_numbers').html('Page ' + (currentPage + 1) + ' of ' + Math.ceil(boxes.length/maxPerPage));
}

function sortById(a, b){
    return compareString(a.box_id, b.box_id);
}

function sortBySize(a, b){
    return compareString(a.size, b.size);
}

function sortByWeight(a, b){
    return a.weight - b.weight;
}

function sortByContents(a, b){
    return compareString(a.contents, b.contents);
}

function sortByExp(a, b){
    if (a.expiration.toLowerCase() === 'never' || b.expiration.toLowerCase() === 'never') {
        return compareString(a.expiration,b.expiration);
    }

    var x = a.expiration.split("/");
    var y = b.expiration.split("/");
    var aDate = new Date(x[2], x[0], x[1]);
    var bDate = new Date(y[2], y[0], y[1]);

    if (aDate < bDate) {
      return 1;
    } else if (aDate > bDate) {
        return -1;
    } else {
        return 0;
    }
}

function sortByFilter(a, b){
    return compareString(a.check, b.check);
}

function sortByReverseFilter(a, b){
    return -1 * compareString(a.check, b.check);
}

function sortByWarehouse(a, b){
    return compareString(a.warehouse, b.warehouse);
}

function sortByReverseWarehouse(a, b){
    return -1 * compareString(a.warehouse, b.warehouse);
}

function compareString(a, b){
    var x = a.toLowerCase();
    var y = b.toLowerCase();

    if (x < y) {
      return 1;
    } else if (x > y) {
        return -1;
    } else {
        return 0;
    }
}

function checkBoxClick(row){
    var boxes;

    if (filtered) {
        boxes = filteredBoxes;
    } else {
        boxes = currentBoxes;
    }

    if (boxes[row].check === '') {
        boxes[row].check = 'checked';

        if (filteredBoxes.indexOf(boxes[row]) === -1) {
            filteredBoxes.push(currentBoxes[row]);
        }
    } else {
        boxes[row].check = '';
    }
}

function warehouseChange(row, id){
    var boxes;

    if (filtered) {
        boxes = filteredBoxes;
    } else {
        boxes = currentBoxes;
    }

    boxes[row].warehouse = $('#' + id + ' option:selected').text();

    Dajaxice.inventory.set_warehouse(warehouseChangeResponse,
        {'box_id': boxes[row].box_id, 'warehouse_abbreviation': boxes[row].warehouse});
}

function warehouseChangeResponse(response){
    if (response.message === 'False') {
        $.jAlert('There was a problem changing the warehouse.', 'error', null);
    }
}

function fillTable(boxes) {
    $('#boxes_body').remove();
    $('#boxes_found').append('<tbody id="boxes_body"></tbody>');

    if(boxes.length === 0) {
        $('#boxes_body').append(BLANK_ROW);
    } else {
        for (var i = 0; i < boxes.length; i++) {
            var order = false;

            if(boxes[i].order_id !== ''){
                order = boxes[i].order_id;
            }

            var rowString = ITEM_TEMPLATE
                .replace('{contents}', boxes[i].contents)
                .replace('{expiration}', boxes[i].expiration)
                .replace('{size}', boxes[i].size)
                .replace('{weight}', boxes[i].weight)
                .replace('{check}',boxes[i].check)
                .replace('{row}',i+(currentPage*maxPerPage));

            var tags = '';

            if (order !== false && groupName === 'Admin') {
                tags += ORDER_TAG_TEMPLATE.replace(/{order_id}/gi,order);
            }

            rowString = rowString.replace('{tags}', tags);

            if (groupName === 'Admin' || groupName === 'Box Transfer') {
                rowString = rowString.replace('{warehouse}',WAREHOUSE_SELECT
                    .replace('<option>' + boxes[i].warehouse + '</option>',
                    '<option selected>' + boxes[i].warehouse + '</option>')
                    .replace('{row}',(i+currentPage*maxPerPage))
                    .replace(/{id}/gi,'select' + (i+currentPage*maxPerPage))
                )
                .replace('{box_id}', '<a href="/inventory/view_box_info/' +
                    boxes[i].box_id + '">' + boxes[i].box_id + '</a>');
            } else {
                rowString = rowString.replace('{warehouse}', boxes[i].warehouse).replace('{box_id}', boxes[i].box_id);
            }

            $('#boxes_body').append(rowString);
        }
    }
}


$(document).ready(function() {
    Dajaxice.inventory.get_warehouse_abbreviations(setWarehouses);

    $('#max_per_page').change(function() {
        maxPerPage = $('#max_per_page option:selected').text();
        showTable();
    });

    $('#filter_button').click(function() {
        filtered = true;

        for(var i = 0; i < filteredBoxes.length; i++){
            if(filteredBoxes[i].check === ''){
                filteredBoxes.splice(i,1);
                i--;
            }
        }

        showTable();
    });

    $('#unfilter_button').click(function() {
        filtered = false;
        showTable();
    });

    $('#next_button').click(function() {
        var boxes;

        if (filtered) {
            boxes = filteredBoxes;
        } else {
            boxes = currentBoxes;
        }

        if (currentPage + 1 < boxes.length / maxPerPage) {
            currentPage = currentPage + 1;
            showTable();
        }
    });

    $('#previous_button').click(function() {
        if(currentPage > 0) {
            currentPage = currentPage - 1;
            showTable();
        }
    });

    $('#idHeader').click(function() {
        if (currentSort === 'id') {
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        } else {
            currentSort = 'id';
            currentBoxes = currentBoxes.sort(sortById);
            filteredBoxes = filteredBoxes.sort(sortById);
            showTable();
        }

    });

    $('#sizeHeader').click(function() {
        if (currentSort === 'size') {
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        } else {
            currentSort = 'size';
            currentBoxes = currentBoxes.sort(sortBySize);
            filteredBoxes = filteredBoxes.sort(sortBySize);
            showTable();
        }
    });

    $('#weightHeader').click(function() {
        if (currentSort === 'weight') {
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        } else {
            currentSort = 'weight';
            currentBoxes = currentBoxes.sort(sortByWeight);
            filteredBoxes = filteredBoxes.sort(sortByWeight);
            showTable();
        }
    });

    $('#contentHeader').click(function() {
        if (currentSort === 'content') {
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        } else {
            currentSort = 'content';
            currentBoxes = currentBoxes.sort(sortByContents);
            filteredBoxes = filteredBoxes.sort(sortByContents);
            showTable();
        }
    });

    $('#expHeader').click(function() {
        if (currentSort === 'exp') {
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        } else {
            currentSort = 'exp';
            currentBoxes = currentBoxes.sort(sortByExp);
            filteredBoxes = filteredBoxes.sort(sortByExp);
            showTable();
        }
    });

    $('#warehouseHeader').click(function(){
        if (currentSort === 'warehouse') {
            currentSort = 'warehouse2';
            currentBoxes = currentBoxes.sort(sortByReverseWarehouse);
            filteredBoxes = filteredBoxes.sort(sortByReverseWarehouse);
            showTable();
        } else {
            currentSort = 'warehouse';
            currentBoxes = currentBoxes.sort(sortByWarehouse);
            filteredBoxes = filteredBoxes.sort(sortByWarehouse);
            showTable();
        }
    });

    $('#filterHeader').click(function(){
        if (currentSort === 'filter') {
            currentSort = 'filter2';
            currentBoxes = currentBoxes.sort(sortByReverseFilter);
            filteredBoxes = filteredBoxes.sort(sortByReverseFilter);
            showTable();
        } else {
            currentSort = 'filter';
            currentBoxes = currentBoxes.sort(sortByFilter);
            filteredBoxes = filteredBoxes.sort(sortByFilter);
            showTable();
        }
    });

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
        var selectedBoxName = $('#box_names option:selected').val();
        Dajaxice.inventory.get_boxes_with_item(setTableList, { 'item_name': selectedItemName,'box_name' : selectedBoxName });
    });
});
