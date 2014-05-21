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

function restoreCallback(response) {
    if (response.result === true) {
        $.jAlert('The backup restore was successful', '', null);
    } else {
        $.jAlert('There was a problem restoring this backup.', 'error', null);
    }
}

$(document).ready(function() {
    $('.downloadBackupLink').click(function() {
        var filename = $(this).attr('filename');

        Dajaxice.administration.download_sql(doDownload, { 'filename': filename });
    });

    $('.restoreBackupLink').click(function() {
        var filename = $(this).attr('filename');
        var backup_date = filename.split('.')[0];

        $.jConfirm('Are you sure you want to do this? All of your data with be DELETED and replaced with ' +
            'the data from ' + backup_date + '.', 'highlight',
            function(decision) {
                if (decision) {
                    $.jConfirm('Are you REALLY SURE? All of your data since ' + backup_date + ' WILL BE ' +
                        'DELETED FOREVER!', 'error',
                        function(decision) {
                            if (decision) {
                                Dajaxice.administration.restore_backup(restoreCallback, { 'filename': filename });
                            }
                        }
                    );
                }
            }
        );
    });

    $('#customRestoreButton').click(function() {
        $.jConfirm('Are you sure you want to do this? All of your data with be DELETED and replaced with ' +
            'the data from your backup file.', 'highlight',
            function(decision) {
                if (decision) {
                    $.jConfirm('Are you REALLY SURE? All of your data since the backup file was created WILL BE ' +
                        'DELETED FOREVER!', 'error',
                        function(decision) {
                            if (decision) {
                                $('#restoreCustomForm').submit();
                            }
                        }
                    );
                }
            }
        );
    });
});
