function deleteCategory(cell, letter, name) {
    Dajaxice.administration.delete_category(function(response) {
        if (response.result === true) {
            cell.remove();
        } else if (response.result === false) {
            $.jAlert(response.message, 'error', null);
        }
    }, { 'letter': letter, 'name': name });
}

function setDeleteCategoryButtons() {
    $('.deleteCategory').unbind('click').click(function() {
        var cell = $(this).parent().parent();
        var letter = cell.find('.letterColumn .letterInput').val();
        var name = cell.find('.nameColumn .nameInput').val();

        $.jConfirm(
            'Are you sure you want to delete the "' + letter + ' - ' + name + '" category?',
            '',
            function(answer) {
                if (answer) {
                    deleteCategory(cell, letter, name);
                }
            }
        );
    });
}

function saveCategory(cell, originalLetter, originalName, letter, name) {
    Dajaxice.administration.save_category(
        function(response) {
            if (response.result === true) {
                cell.find('.letterColumn .letterInput').attr('original', letter);
                cell.find('.nameColumn .nameInput').attr('original', name);
                cell.find('.saveColumn').html('');
            } else if (response.result === false) {
                $.jAlert(response.message, 'error', null);
            }
        },
        {
            'original_letter': originalLetter,
            'original_name': originalName,
            'letter': letter,
            'name': name
        }
    );
}

function setSaveButtons() {
    $('.saveChanges').unbind('click').click(function() {
        var cell = $(this).parent().parent();
        var letter = cell.find('.letterColumn .letterInput').val();
        var originalLetter = cell.find('.letterColumn .letterInput').attr('original');

        var name = cell.find('.nameColumn .nameInput').val();
        var originalName = cell.find('.nameColumn .nameInput').attr('original');

        var message = 'Change "' + originalLetter + ' - ' + originalName +
            '" to "' + letter + ' - ' + name + '"?';

        $.jConfirm(message, '',
            function(answer) {
                if (answer) {
                    saveCategory(cell, originalLetter, originalName, letter, name);
                }
            }
        );
    });
}

function setFieldChangeListener() {
    $('.letterInput, .nameInput').unbind('input').bind('input',
        function() {
            var cell = $(this).parent().parent();
            var letter = cell.find('.letterColumn .letterInput').val();
            var originalLetter = cell.find('.letterColumn .letterInput').attr('original');

            var name = cell.find('.nameColumn .nameInput').val();
            var originalName = cell.find('.nameColumn .nameInput').attr('original');

            var saveColumn = cell.find('.saveColumn');

            if (saveColumn.html() === '') {
                saveColumn.html('<a href="javascript:void(0)" class="saveChanges">Save Changes</a>');
                setSaveButtons();
            } else if (cell.find('.saveChanges').length === 1 &&
                    letter === originalLetter && name === originalName) {
                saveColumn.html('');
            }
        }
    );
}

$(document).ready(function() {
    setDeleteCategoryButtons();
    setFieldChangeListener();
});
