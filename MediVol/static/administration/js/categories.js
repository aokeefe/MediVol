function deleteCategory(element, letter, name) {
    Dajaxice.administration.delete_category(function(response) {
        if (response.result === true) {
            element.remove();
        } else if (response.result === false) {
            $.jAlert(response.message, 'error', null);
        }
    }, { 'letter': letter, 'name': name });
}

$(document).ready(function() {
    $('.deleteCategory').click(function() {
        var element = $(this).parent().parent();
        var letter = element.find('.letterColumn .letterInput').val();
        var name = element.find('.nameColumn .nameInput').val();

        $.jConfirm(
            'Are you sure you want to delete the "' + letter + ' - ' + name + '" category?',
            '',
            function(answer) {
                if (answer) {
                    deleteCategory(element, letter, name);
                }
            }
        );
    });
});
