// Template for adding new item to the table.
var ITEM_TEMPLATE = '<tr>' + 
        '<td>{order_id}</td>' + 
        '<td>{box_id}</td>' + 
        '<td>{size}</td>' + 
        '<td>{weight}</td>' + 
        '<td>{contents}</td>' + 
        '<td>{expiration}</td>' + 
        '<td>{warehouse}</td>' + 
        '<td><input type="checkbox" onclick="checkBoxClick({row})" {check}></td>' + 
    '</tr>';
    
// Simple template used to insert a blank row below the table header 
// when there are no items in the box.
var BLANK_BOX_ROW = "<tr id='placeholder_row'>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>" +
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td>&nbsp;</td>" + 
                "</tr>";

var WAREHOUSE_SELECT = '<select id="{id}" onchange="warehouseChange({row},&quot;{id}&quot;)">{options}</select>';

// Need these to update lists for box names and items.
var boxNameToChoose = '';
var itemToChoose = '';

var currentBoxes = [];
var filteredBoxes = [];
var currentSort = '';
var currentPage = 0;
var maxPerPage = $('#max_per_page option:selected').text();
var filtered = false;


function setWarehouses(response){
    var warehouses = '';
    for(var i=0;i<response.length;i++){
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

function get_current_boxes(){
    if(filtered){
        return filteredBoxes;
    }
    else{
        return currentBoxes;
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
    var boxes = get_current_boxes();
    if (boxes.length > maxPerPage){
        fillTable(boxes.slice(currentPage*maxPerPage,currentPage*maxPerPage+maxPerPage));
    }
    else{
        fillTable(boxes);
    }
    $('#page_numbers').html('Page ' + (currentPage + 1) + ' of ' + Math.ceil(boxes.length/maxPerPage));
}

function sortById(a,b){
    return compareString(a.box_id,b.box_id);
}

function sortBySize(a,b){
    return compareString(a.size,b.size);
}

function sortByWeight(a,b){
    return a.weight - b.weight;
}

function sortByContents(a,b){
    return compareString(a.contents,b.contents);
}

function sortByExp(a,b){
    if(a.expiration.toLowerCase() === 'never' || b.expiration.toLowerCase() === 'never'){
        return compareString(a.expiration,b.expiration);
    }
    var x = a.expiration.split("/");
    var y = b.expiration.split("/");
    var aDate = new Date(x[2],x[0],x[1]);
    var bDate = new Date(y[2],y[0],y[1]);
    if(aDate < bDate){
      return 1;
    }
    else if(aDate > bDate){
        return -1;
    }
    else{
        return 0;
    }
}

function sortByFilter(a,b){
    return compareString(a.check,b.check);
}

function sortByReverseFilter(a,b){
    return -1*compareString(a.check,b.check);
}

function sortByWarehouse(a,b){
    return compareString(a.warehouse,b.warehouse);
}

function sortByReverseWarehouse(a,b){
    return -1*compareString(a.warehouse,b.warehouse);
}

function compareString(a,b){
    var x = a.toLowerCase();
    var y = b.toLowerCase();
    if(x < y){
      return 1;
    }
    else if(x > y){
        return -1;
    }
    else{
        return 0;
    }
}

function checkBoxClick(row){
    var boxes = get_current_boxes();
    if (boxes[row].check === ''){
        boxes[row].check = 'checked';
        if(filteredBoxes.indexOf(boxes[row]) === -1){
            filteredBoxes.push(currentBoxes[row]);
        }      
    }
    else{
        boxes[row].check = '';
    }
}

function warehouseChange(row,id){
    var boxes = get_current_boxes();
    boxes[row].warehouse = $('#' + id + ' option:selected').text();
    Dajaxice.inventory.set_warehouse(warehouseChangeResponse,
        {'box_id':boxes[row].box_id, 'warehouse_abbreviation':boxes[row].warehouse});
}

function warehouseChangeResponse(response){
    if(response.message === 'False'){
        alert('could not save warehouse');
    }
}

function fillTable(boxes) {
    $('#boxes_body').remove();
    $('#boxes_found').append('<tbody id="boxes_body"></tbody>');
    if(boxes.length==0){
        $('#boxes_body').append(BLANK_BOX_ROW);
    }
    else{
        for(var i=0;i<boxes.length;i++) {
            var order = '';
            if(boxes[i].order_id !== ''){
                order = '<a href="/orders/review/' + boxes[i].order_id + '">' + boxes[i].order_id + '</a>';
            }
            $('#boxes_body').append(
                ITEM_TEMPLATE.replace('{box_id}', '<a href="/inventory/view_box_info/' + 
                    boxes[i].box_id + '">' + boxes[i].box_id + '</a>')
                    .replace('{contents}', boxes[i].contents)
                    .replace('{expiration}', boxes[i].expiration)
                    .replace('{size}', boxes[i].size)
                    .replace('{weight}', boxes[i].weight)
                    .replace('{warehouse}',WAREHOUSE_SELECT
                        .replace('<option>' + boxes[i].warehouse + '</option>',
                        '<option selected>' + boxes[i].warehouse + '</option>')
                        .replace('{row}',(i+currentPage*maxPerPage))
                        .replace(/{id}/gi,'select' + (i+currentPage*maxPerPage))
                        )
                    .replace('{check}',boxes[i].check)
                    .replace('{row}',i+(currentPage*maxPerPage))
                    .replace('{order_id}',order)
            );
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
        for(var i=0;i<filteredBoxes.length;i++){
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
    
    $('#warehouseHeader').click(function(){
        if (currentSort === 'warehouse'){
            currentSort = 'warehouse2';
            currentBoxes = currentBoxes.sort(sortByReverseWarehouse);
            filteredBoxes = filteredBoxes.sort(sortByReverseWarehouse);
            showTable();
        }
        else{
            currentSort = 'warehouse';
            currentBoxes = currentBoxes.sort(sortByWarehouse);
            filteredBoxes = filteredBoxes.sort(sortByWarehouse);
            showTable();
        }
    });
    
    $('#filterHeader').click(function(){
        if (currentSort === 'filter'){
            currentSort = 'filter2';
            currentBoxes = currentBoxes.sort(sortByReverseFilter);
            filteredBoxes = filteredBoxes.sort(sortByReverseFilter);
            showTable();
        }
        else{
            currentSort = 'filter';
            currentBoxes = currentBoxes.sort(sortByFilter);
            filteredBoxes = filteredBoxes.sort(sortByFilter);
            showTable();
        }
    });
});