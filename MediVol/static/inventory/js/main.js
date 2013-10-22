$(document).ready(function() {
    $('#category').change(function() {
        var selectedCategory = $('#category option:selected').val();
        
        $.ajax({
            url: '/static/inventory/ajax/getBoxNames.py',
            type: 'POST',
            data: { category: selectedCategory },
            success: function(response){
                console.log(response);
            }
        });
    });
});