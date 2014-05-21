// Template for adding new item to the table.
var ORDER_TEMPLATE = '<tr>' +
        '<td>{order_id}</td>' +
        '<td>{status}</td>' +
        '<td>{order_for}</td>' +
        '<td>{date}</td>' +
        '<td>{price}</td>' +
        '<td>{weight}</td>' +
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
       
function orderRow(order_id, order_name, status, order_for, date, price, weight){
    this.order_id = order_id;
    this.order_name = order_name;
    this.status = status;
    this.order_for = order_for;
    this.date = date;
    this.price = price;
    this.weight = weight;
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

function showTable(){
    var orders = currentOrders;
    $('#orders_body').remove();
    $('#orders_found').append('<tbody id="orders_body"></tbody>');
    if(orders.length==0){
        $('#orders_body').append(BLANK_ROW);
    }
    else{
        for(var i=0;i<orders.length;i++){
            var rowString = ORDER_TEMPLATE.replace('{order_id}', '<a href="/orders/review/' + orders[i].order_id + '">' + orders[i].order_name + '</a>')
                .replace('{status}', orders[i].status)
                .replace('{order_for}', orders[i].order_for)
                .replace('{date}', orders[i].date)
                .replace('{price}', orders[i].price)
                .replace('{weight}', orders[i].weight);
            $('#orders_body').append(rowString);
        }
    }
}

$(document).ready(function() {
        $('#statusSelect').change(function() {
            var selected = $('#statusSelect').find(":selected").val();
            if(selected ==="All Open"){
                Dajaxice.orders.get_all_open_orders(setTable);
            }
            else if(selected ==="All Orders"){
                Dajaxice.orders.get_all_orders(setTable);
            }
            else{
                Dajaxice.orders.get_all_orders_with_status(setTable,{'status': selected});
            }
            
    });
});

