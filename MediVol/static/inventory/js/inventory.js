// Template for adding new item to the table.
var ITEM_TEMPLATE = '<tr>' + 
        '<td>{box_id}</td>' + 
        '<td>{size}</td>' + 
        '<td>{weight}</td>' + 
        '<td>{contents}</td>' + 
        '<td>{expiration}</td>' + 
        "<td>{warehouse}</td>" + 
        '<td><input type="checkbox" onclick="checkBoxClick({row})" {check}></td>' + 
    '</tr>';
    
// Simple template used to insert a blank row below the table header 
// when there are no items in the box.
var BLANK_ROW = "<tr id='placeholder_row'>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>" +
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td>&nbsp;</td>" + 
                "</tr>";

var WAREHOUSE_SELECT = "<select>{options}</select>";

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

function setTableList(response) {
    currentBoxes = response;
    showTable();
}

function showTable() {
    var boxes;
    if(filtered){
        boxes = filteredBoxes;
    }
    else{
        boxes = currentBoxes;
    }
    if (boxes.length > maxPerPage){
        fillTable(boxes.slice(currentPage*maxPerPage,currentPage*maxPerPage+maxPerPage));
        
    }
    else{
        fillTable(boxes);
    }
    $('#page_numbers').html('Page ' + (currentPage + 1) + ' of ' + Math.ceil(boxes.length/maxPerPage));
}

function sortById(a,b){
    var x = a[0].toLowerCase(), y = b[0].toLowerCase();
    return x < y ? -1 : x > y ? 1 : 0;
}

function sortBySize(a,b){
    var x = a[3].toLowerCase(), y = b[3].toLowerCase();
    return x < y ? -1 : x > y ? 1 : 0;
}

function sortByWeight(a,b){
    return a[4] - b[4];
}

function sortByContents(a,b){
    var x = a[1].toLowerCase(), y = b[1].toLowerCase();
    return x < y ? -1 : x > y ? 1 : 0;
}

function sortByExp(a,b){
    var x = a[2].split("/");
    var y = b[2].split("/");
    var aDate = new Date(x[2],x[0],x[1]);
    var bDate = new Date(y[2],y[0],y[1]);
    return aDate < bDate ? -1 : aDate > bDate ? 1 : 0;
}

function sortByFilter(a,b){
    var x = a[5].toLowerCase(), y = b[5].toLowerCase();
    return x < y ? 1 : x > y ? -1 : 0;
}

function checkBoxClick(row){
    var boxes;
    if(filtered){
        boxes = filteredBoxes;
    }
    else{
        boxes = currentBoxes;
    }
    if (boxes[row][5] === ''){
        boxes[row][5] = 'checked';
        filteredBoxes.push(currentBoxes[row]);
        
    }
    else{
        boxes[row][5] = '';
        filteredBoxes.splice(filteredBoxes.indexOf(boxes[row]),1);
    }
}

function fillTable(boxes) {
    $('#boxes_body').remove();
    $('#boxes_found').append('<tbody id="boxes_body"></tbody>');
    if(boxes.length==0){
        $('#boxes_body').append(BLANK_ROW);
    }
    else{
        for(var i=0;i<boxes.length;i++) {
            $('#boxes_body').append(
                ITEM_TEMPLATE.replace('{box_id}', '<a href="/inventory/view_box_info/' + 
                    boxes[i][0].substr(1) + '">' + boxes[i][0] + '</a>')
                    .replace('{contents}', boxes[i][1])
                    .replace('{expiration}', boxes[i][2])
                    .replace('{size}', boxes[i][3])
                    .replace('{weight}', boxes[i][4])
                    .replace('{warehouse}',WAREHOUSE_SELECT)
                    .replace('{check}',boxes[i][5])
                    .replace('{row}',i+(currentPage*maxPerPage))
            );
        }
    }
}


$(document).ready(function() {
    //need to change when warehouse model is changed
    WAREHOUSE_SELECT.replace('{options}','');
    
    $('#max_per_page').change(function() {
        maxPerPage = $('#max_per_page option:selected').text();
        showTable();
    });
    
    $('#filter_button').click(function() {
        filtered = true;
        showTable();
    });
    
    $('#unfilter_button').click(function() {
        filtered = false;
        showTable();
    });
    
    $('#next_button').click(function() {
        var boxes;
        if(filtered){
            boxes = filteredBoxes;
        }
        else{
            boxes = currentBoxes;
        }
        if(currentPage + 1 < boxes.length/maxPerPage){
            currentPage = currentPage + 1;
            showTable(); 
        }
    });
    
    $('#previous_button').click(function() {
        if(currentPage > 0){
            currentPage = currentPage - 1;
            showTable(); 
        }
    });
    
    $('#idHeader').click(function() {
        if (currentSort === 'id'){
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        }
        else{
            currentSort = 'id';
            currentBoxes = currentBoxes.sort(sortById);
            filteredBoxes = filteredBoxes.sort(sortById);
            showTable();
        }
        
    });
    
    $('#sizeHeader').click(function() {
        if (currentSort === 'size'){
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        }
        else{
            currentSort = 'size';
            currentBoxes = currentBoxes.sort(sortBySize);
            filteredBoxes = filteredBoxes.sort(sortBySize);
            showTable();
        }
    });
    
    $('#weightHeader').click(function() {
        if (currentSort === 'weight'){
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        }
        else{
            currentSort = 'weight';
            currentBoxes = currentBoxes.sort(sortByWeight);
            filteredBoxes = filteredBoxes.sort(sortByWeight);
            showTable();
        }
    });
    
    $('#contentHeader').click(function() {
        if (currentSort === 'content'){
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        }
        else{
            currentSort = 'content';
            currentBoxes = currentBoxes.sort(sortByContents);
            filteredBoxes = filteredBoxes.sort(sortByContents);
            showTable();
        }
    });
    
    $('#expHeader').click(function() {
        if (currentSort === 'exp'){
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        }
        else{
            currentSort = 'exp';
            currentBoxes = currentBoxes.sort(sortByExp);
            filteredBoxes = filteredBoxes.sort(sortByExp);
            showTable();
        }
    });
    
    $('#filterHeader').click(function() {
        if (currentSort === 'filter'){
            currentBoxes = currentBoxes.reverse();
            filteredBoxes = filteredBoxes.reverse();
            showTable();
        }
        else{
            currentSort = 'filter';
            currentBoxes = currentBoxes.sort(sortByFilter);
            filteredBoxes = filteredBoxes.sort(sortByFilter);
            showTable();
        }
    });
    
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
        
        // Get the list of box names for the selected category.
        Dajaxice.inventory.get_box_names(getBoxNames, { 'category_name': selectedCategory });
    });
    
    // Set the 'on change' event for the box names list.
    $('#box_names').change(function() {
        var selectedBoxName = $('#box_names option:selected').val();
       
        // Get the list of items for the selected box name.
        Dajaxice.inventory.get_items(getItems, { 'box_name': selectedBoxName });
    });
    
    // Set the 'on change' event for the items list.
    $('#items').change(function() {
    	var selectedItemName = $('#items option:selected').val();
    	var selectedBoxName = $('#box_names option:selected').val();
        Dajaxice.inventory.get_boxes_with_item(setTableList, { 'item_name': selectedItemName,'box_name' : selectedBoxName });
    });
});