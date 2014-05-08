var CATEGORY_TEMPLATE = "<tr>" +
    "<td class='letterColumn'>" +
        "<input class='letterInput textField' type='text'" +
            "original='{letter}' value='{letter}' />" +
    "</td>" +
    "<td class='nameColumn'>" +
        "<input class='nameInput textField' type='text'" +
            "original='{name}' value='{name}' />" +
    "</td>" +
    "<td class='deleteColumn'>" +
        "<a href='javascript:void(0)' class='deleteCategory'>Delete</a>" +
    "</td>" +
    "<td class='saveColumn'></td>" +
"</tr>";

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

function addCategory(letter, name) {
    Dajaxice.administration.add_category(function(response) {
        if (response.result === true) {
            $('.requiredMessage').hide();

            var newRow = CATEGORY_TEMPLATE
                .replace(/{letter}/gi, letter)
                .replace(/{name}/gi, name);

            $('table').append(newRow);

            setDeleteCategoryButtons();
            setFieldChangeListener();
        } else if (response.result === false) {
            $('.requiredMessage').html(response.message);
            $('.requiredMessage').show();
        }
    }, { 'letter': letter, 'name': name });
}

function setAddCategoryButton() {
    $('#addCategory').unbind('click').click(function() {
        var letter = $('#categoryLetter').val();
        var name = $('#categoryName').val();

        addCategory(letter, name);
    });
}

$(document).ready(function() {
    setDeleteCategoryButtons();
    setFieldChangeListener();
    setAddCategoryButton();
});
