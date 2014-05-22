/**
* Callback for get_label AJAX call.
*/
function print(response){
    if (response != 'False') {
        var iframe = document.createElement('iframe');
        iframe.src = response;
        iframe.width = 0;
        iframe.height = 0;
        document.body.appendChild(iframe);

        setTimeout(function() {
             location.reload();
        }, 100);
    }
}

function print_label(box_id){
    Dajaxice.inventory.get_label(print, {"box_id" : box_id});
}

function changeWarehouse(newWarehouse) {
    Dajaxice.inventory.set_warehouse(function(response) {
        if (response.message === 'True') {
            $('#unknownOption').remove();
        } else if (response.message === 'False') {
            $.jAlert('There was an error changing the warehouse.', 'error', null);
        }
    }, { 'box_id': boxId, 'warehouse_abbreviation': newWarehouse });
}

function deleteBox(box_id) {
    $.jConfirm('Are you sure you want to delete this box?', '',
        function(decision) {
            if (decision) {
                Dajaxice.inventory.delete_box(function(response) {
                    if (response.result === false) {
                        $.jAlert(response.message, 'error', null);
                    } else if (response.result === true) {
                        window.location = '/inventory/';
                    }
                }, { 'box_id': box_id });
            }
        }
    );
}

$(document).ready(function() {
    $('#warehouse').change(function() {
        var warehouseName = $('#warehouse option:selected').html();
        var warehouseAbbreviation = $('#warehouse option:selected').val();

        if (warehouseAbbreviation === 'unknown') {
            return;
        }

        $.jConfirm('Move this box to "' + warehouseName + '" warehouse?', '',
            function(result) {
                if (result) {
                    changeWarehouse(warehouseAbbreviation);
                }
            }
        );
    });
});
