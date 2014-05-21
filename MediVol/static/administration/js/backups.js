function doDownload(response) {
    if (response.result === true) {
        var a = document.createElement('a');
        a.href = 'data:text/sql;charset=UTF-8,' + encodeURIComponent(response.sql_contents);
        a.target = '_blank';
        a.download = response.filename;

        document.body.appendChild(a);
        a.click();
    } else if (response.result === false) {
        $.jAlert(response.message, 'error', null);
    }
}

$(document).ready(function() {
    $('.backupLink').click(function() {
        var filename = $(this).html();

        Dajaxice.administration.download_sql(doDownload, { 'filename': filename });
    });
});
