var ORDER_REVIEW_TEMPLATE =
    "<tr id='box_info'>" +
        "<td>{box_id}</td>" +
        "<td>{box_size}</td>" +
        "<td>{box_weight}</td>" +
        "<td>" +
            "<input type='text' class='textField' id='box_{box_id}_price'" +
                "name='box_{box_id}_price'" +
                "onchange='displayTotalPrice()'>" +
        "</td>" +
    "</tr>";

function populateOrderReviewTable() {
    $('#review_boxes tr').each(function(index, element) {
        element = $(element);

        if (element.attr('id') != 'placeholder_row' &&
                element.attr('id') != 'table_header') {
            element.remove();
        }
    });

    $('#boxes_added tr').each(function(index, element) {
        element = $(element);

        if (element.attr('id') != 'placeholder_row' &&
                element.attr('id') != 'table_header') {
            var itemInfo = element.children('td');
            var boxId = $(itemInfo[0]).html();
            var boxSize = $(itemInfo[1]).html();
            var boxWeight = $(itemInfo[2]).html();

            $('#review_boxes').append(
                ORDER_REVIEW_TEMPLATE.replace(/\{box_id\}/g, boxId)
                .replace(/\{box_size\}/g, boxSize)
                .replace(/\{box_weight\}/g, boxWeight)
            );
        }
    });
}

function calculateTotalPrice(callback) {
    var totalPrice = 0.0;

    $('#review_boxes tr td :input').each(function() {
        var price = $(this).val();
        totalPrice += parseFloat(price);
    });

    callback(totalPrice);
}

function displayTotalPrice() {
    calculateTotalPrice(function (totalPrice) {
        $('#total_price').empty();
        $('#total_price').append(totalPrice);
    });
}
