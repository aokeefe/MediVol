// Template for adding new item to the table.
var ORDER_TEMPLATE = '<tr>' +
        '<td>{order_id}</td>' +
        '<td>{status}</td>' +
        '<td>{content}</td>' +
        '<td>{order_for}</td>' +
        '<td>{date}</td>' +
        '<td>{price}</td>' +
        '<td>{weight}</td>' +
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
                    "<td></td>" +
                    "<td>&nbsp;</td>" +
                "</tr>";

var STATUS_DROP_DOWN = '<select>{options}</select>';

var STATUS_SELECT = '<select id="{id}" onchange="statusChange({row},&quot;{id}&quot;)">{options}</select>';




var currentOrders = [];
var filteredOrders = [];
var filtered = false;
       
function orderRow(order_id, status, contents, order_for, date, price, weight){
    this.order_id = order_id;
    this.status = status;
    this.contents = contents;
    this.order_for = order_for;
    this.date = date;
    this.price = price;
    this.weight = weight;
    this.check = '';
}

function setTable(response){
    currentOrders.length = 0;
    for(var i=0;i<response.length;i++){
        currentOrders.push(new orderRow(response[i][0],
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

function getCurrentOrders(){
    if(filtered){
        return filteredOrders;
    }
    else{
        return currentOrders;
    }
}

function showTable(){
    var orders = getCurrentOrders();
    $('#orders_body').remove();
    $('#orders_found').append('<tbody id="orders_body"></tbody>');
    if(orders.length==0){
        $('#orders_body').append(BLANK_ROW);
    }
    else{
        for(var i=0;i<orders.length;i++){
            var rowString = ORDER_TEMPLATE.replace('{order_id}', '<a href="/orders/review/' + orders[i].order_id + '">' + orders[i].order_id + '</a>')
                .replace('{status}', orders[i].status)
                .replace('{content}', getBoxIdHtml(orders[i].contents))
                .replace('{order_for}', orders[i].order_for)
                .replace('{date}', orders[i].date)
                .replace('{price}', orders[i].price)
                .replace('{weight}', orders[i].weight)
                .replace('{check}', orders[i].check);
            $('#orders_body').append(rowString);
        }
    }
}

function getBoxIdHtml(box_ids){
    var htmlString = '';
    for(var i=0;i<box_ids.length;i++){
        htmlString += '<a href="/inventory/view_box_info/' +
                box_ids[i] + '">' + box_ids[i] + '</a>';
        if(i+1!=box_ids.length){
            htmlString += ', ';
        }
    }
    return htmlString;
}

$(document).ready(function() {
    Dajaxice.orders.get_orders(setTable);
});

