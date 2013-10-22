function getBoxNames(response) {
    console.log(response.message);
}

$(document).ready(function() {
    $('#category').change(function() {
        var selectedCategory = $('#category option:selected').val();
        Dajaxice.inventory.get_box_names(getBoxNames);
    });
});