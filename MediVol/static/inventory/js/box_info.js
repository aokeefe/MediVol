/**
* Callback for get_label AJAX call.
*/
function print(response){
    if (response != 'False') {
        var iframe = document.createElement('iframe');
        var html = '<head><script type"text/javascript">window.print();</script></head>' +
                '<body>' + response + '</body>';
        iframe.src = 'data:text/html;charset=utf-8,' + encodeURI(html);
        iframe.width = 0;
        iframe.height = 0;
        document.body.appendChild(iframe);

        setTimeout(function() {
            location.reload();
        }, 1);
    }
}


function print_label(box_id){
    Dajaxice.inventory.get_label(print, {"box_id" : box_id});
}
