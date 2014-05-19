function changeOrderStatus(statusChar) {
    Dajaxice.orders.change_order_status(
        function(response) {
            if (response.result === 'True') {
                window.location.reload();
            } else if (response.result == 'False') {
                $.jAlert('There was a problem changing the status of this order.', 'error', null);
            }
        },
        {
            'order_number': orderNumber,
            'order_status': statusChar
        }
    );
}

function downloadCVS(response){
    alert(response);
    var csvString = response.join("\r\n");
    alert(csvString);
    var a = document.createElement('a');
    a.href = 'data:text/csv;charset=UTF-8,' + encodeURIComponent(csvString);
    a.target = '_blank';
    a.download = orderNumber + 'PackingList.csv';

    document.body.appendChild(a);
    a.click();
}

$(document).ready(function() {
    $('#orderStatus').change(function() {
        var statusChar = $('#orderStatus option:selected').val();
        var status = $('#orderStatus option:selected').html();

        $.jConfirm('Change the status of this order to "' + status + '"?', '',
            function(result) {
                if (result) {
                    changeOrderStatus(statusChar);
                }
            }
        );
    });
    
    $('#downloadOrder').click(function() {
        Dajaxice.orders.get_order_packing_list(downloadCVS, { 'order_id': orderNumber });
    });
});
