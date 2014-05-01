var ROW_TEMPLATE = "<tr>" +
        "<td>{box_id}</td>" +
        "<td>{warehouse}</td>" +
        "<td>{weight}</td>" +
        "<td>{size}</td>" +
        "<td>{expiration}</td>" +
        "<td><a href='javascript:void(0)' class='removeBox'>Remove</a></td>" +
    "</tr>";

var BLANK_ROW = "<tr id='placeholder_row'>" +
        "<td></td>" +
        "<td></td>" +
        "<td>&nbsp;</td>" +
    "</tr>";

function getAddedBoxes() {
    var boxes = [];

    // Go through each item in the table and add it to the items array.
    // Each item is added as an array with the following format:
    // [ item_name, item_expiration, item_count ]
    $('#boxes_added tr').each(function(index, element) {
        element = $(element);

        if (element.attr('id') != 'placeholder_row' &&
                element.attr('id') != 'table_header') {
            var boxInfo = element.children('td');

            var boxId = $(boxInfo[0]).html();

            boxes.push(boxId);
        }
    });

    return boxes;
}

function boxAlreadyAdded(boxId) {
    return (getAddedBoxes().indexOf(boxId) != -1);
}

function setRemoveButton() {
    $('.removeBox').unbind('click').click(function() {
        // Remove the row for the item.
        $(this).parent().parent().remove();

        // If there are no items, append the empty placeholder row.
        if ($('#boxes_added tr').length == 1) {
            $('#boxes_added').append(BLANK_ROW);
        }
    });
}

function addBox(response) {
    if (response.result === true) {
        $('#boxNotFoundMessage').hide();
        $('#boxTransferBarcode').val('');

        if (boxAlreadyAdded(response.box_id)) {
            return;
        }

        var newRow = ROW_TEMPLATE
            .replace('{box_id}', response.box_id)
            .replace('{warehouse}', response.warehouse)
            .replace('{weight}', response.weight + ' lbs')
            .replace('{size}', response.size)
            .replace('{expiration}', response.expiration);

        $('#placeholder_row').remove();

        $('#boxes_added').append(newRow);

        setRemoveButton();
    } else {
        $('#boxNotFoundMessage').show();
    }
}

$(document).ready(function() {

    $('#boxTransferBarcode').focus().bind(
        'input',
        function() {
            var barcode = $(this).val();

            if (barcode.length === 8) {
                Dajaxice.inventory.get_box_by_barcode(addBox, { 'barcode': barcode });
            }
        }
    );

    $('#transferBoxes').click(function() {
        var boxes = getAddedBoxes();
        var warehouse = $('#toWarehouse option:selected').val();
        var fullWarehouseName = $('#toWarehouse option:selected').html();

        if (boxes.length > 0) {
            $.jConfirm('Transfer these boxes to the "' + fullWarehouseName + '" warehouse?', '',
                function(result) {
                    if (result) {
                        Dajaxice.inventory.transfer_boxes(
                            function(response) {
                                if (response.result === true) {
                                    window.location.reload();
                                } else if (response.result === false) {
                                    $.jAlert('There was a problem transferring these boxes.', 'error', null);
                                }
                            },
                            {
                                'boxes': boxes,
                                'warehouse_abbreviation': warehouse
                            }
                        );
                    }
                }
            );
        }
    });
});
