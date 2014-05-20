var BOX_NAME_TEMPLATE = "<tr>" +
    "<td class='categoryColumn'>" +
        "<input class='originalCategory' type='hidden'" +
            "value='{category_letter}' />" +
        "<select class='categoryInput'>" +
            "{categories}" +
        "</select>" +
    "</td>" +
    "<td class='nameColumn'>" +
        "<input class='nameInput textField' type='text'" +
            "original='{name}' value='{name}' />" +
    "</td>" +
    "<td class='deleteColumn'>" +
        "<a href='javascript:void(0)' class='deleteBoxName'>Delete</a>" +
    "</td>" +
    "<td class='saveColumn'></td>" +
"</tr>";

function deleteBoxName(cell, letter, name) {
    Dajaxice.administration.delete_box_name(function(response) {
        if (response.result === true) {
            cell.remove();
        } else if (response.result === false) {
            $.jAlert(response.message, 'error', null);
        }
    }, { 'letter': letter, 'name': name });
}

function setDeleteBoxNameButtons() {
    $('.deleteBoxName').unbind('click').click(function() {
        var cell = $(this).parent().parent();
        var letter = cell.find('.categoryColumn .categoryInput option:selected').val();
        var name = cell.find('.nameColumn .nameInput').val();

        $.jConfirm(
            'Are you sure you want to delete the "' + name + '" box name?',
            '',
            function(answer) {
                if (answer) {
                    deleteBoxName(cell, letter, name);
                }
            }
        );
    });
}

function saveBoxName(cell, originalLetter, originalName, letter, name) {
    Dajaxice.administration.save_box_name(
        function(response) {
            if (response.result === true) {
                cell.find('.categoryColumn .originalCategory').val(letter);
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
        var cell = $(event.target).parent().parent();

        var letter = cell.find('.categoryColumn .categoryInput option:selected').val();
        var originalLetter = cell.find('.categoryColumn .originalCategory').val();

        var name = cell.find('.nameColumn .nameInput').val();
        var originalName = cell.find('.nameColumn .nameInput').attr('original');

        var saveColumn = cell.find('.saveColumn');

        var message = 'Change "' + originalLetter + ' - ' + originalName +
            '" to "' + letter + ' - ' + name + '"?';

        $.jConfirm(message, '',
            function(answer) {
                if (answer) {
                    saveBoxName(cell, originalLetter, originalName, letter, name);
                }
            }
        );
    });
}

function fieldChanged(event) {
    var cell = $(event.target).parent().parent();

    var letter = cell.find('.categoryColumn .categoryInput option:selected').val();
    var originalLetter = cell.find('.categoryColumn .originalCategory').val();

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

function setFieldChangeListener() {
    $('.categoryInput').unbind('change').change(fieldChanged);

    $('.nameInput').unbind('input').bind('input', fieldChanged);
}

function addBoxName(letter, name) {
    Dajaxice.administration.add_box_name(function(response) {
        if (response.result === true) {
            $('.requiredMessage').hide();

            var categories = $($('.categoryInput')[0]).clone();
            categories.find('[value=' + letter + ']').attr('selected', 'selected');

            var newRow = BOX_NAME_TEMPLATE
                .replace(/{categories}/gi, categories.html())
                .replace(/{category_letter}/gi, letter)
                .replace(/{name}/gi, name);

            $('table').append(newRow);

            $($('#categorySelect option')[0]).attr('selected', 'selected');
            $('#boxNameName').val('');

            setDeleteBoxNameButtons();
            setFieldChangeListener();
        } else if (response.result === false) {
            $('.requiredMessage').html(response.message);
            $('.requiredMessage').show();
        }
    }, { 'letter': letter, 'name': name });
}

function setAddBoxNameButton() {
    $('#addBoxName').unbind('click').click(function() {
        var letter = $('#categorySelect option:selected').val();
        var name = $('#boxNameName').val();

        addBoxName(letter, name);
    });
}

$(document).ready(function() {
    setDeleteBoxNameButtons();
    setFieldChangeListener();
    setAddBoxNameButton();
});
