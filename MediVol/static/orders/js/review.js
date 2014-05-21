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
            'order_id': orderId,
            'order_status': statusChar
        }
    );
}

function deleteOrder() {
    $.jConfirm('Are you sure you want to delete this order?', '',
        function(decision) {
            if (decision) {
                Dajaxice.orders.delete_order(
                    function(response) {
                        if (response.result === true) {
                            window.location = '/orders/';
                        } else if (response.result === false) {
                            $.jAlert('There was a problem deleting this order.', 'error', null);
                        }
                    },
                    {
                        'order_id': orderId
                    }
                );
            }
        }
    );
}

function dontShowAgain() {
    Dajaxice.orders.delete_locked_box_notifications(
        function(response) {
            if (response.result === true) {
                $('#boxNotification').slideUp();
            } else if (response.result === false) {
                $.jAlert(response.message, 'error', null);
            }
        },
        { 'order_id': orderId }
    );
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

    $('.deleteOrderButton').click(deleteOrder);

    $('#dontShowAgain').click(dontShowAgain);
});
