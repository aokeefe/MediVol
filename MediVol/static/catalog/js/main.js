// Need these to update lists for box names and items.
var boxNameToChoose = '';
var itemToChoose = '';

var selected_catagory = '';
var selected_box_name = '';


/**
* Callback for get_box_names AJAX call.
*/
function getBoxNames(response) {
    $('#box_names').empty();
    $('#items').empty();
    
    // Add the box names to the list of box names.
    for (var i = 0; i < response.length; i++) {
        $('#box_names').append('<option>' + response[i] + '</option>');
    }
    
    // If this was a search, we have to select the right box name 
    // and trigger the change event so it will populate the items list.
    if (boxNameToChoose != '') {
        $('#box_names').val(boxNameToChoose);
        boxNameToChoose = '';
        $('#box_names').change();
    }
}

/**
* Callback for the get_items AJAX call. Does the same things as 
* the getBoxNames callback, just for items instead.
*/
function getItems(response) {
    $('#items').empty();
    
    for (var i = 0; i < response.length; i++) {
        $('#items').append('<option>' + response[i] + '</option>');
    }
    
    if (itemToChoose != '') {
        $('#items').val(itemToChoose);
        itemToChoose = '';
        $('#items').change();
    }
}

/**
* Callback for the create_items AJAX call.
*/
function createItem(response){
	alert(response.message);
}

$(document).ready(function() {
    
    $('#catagory_input').keypress(function(e) {
    	document.getElementById('box_name_input').value = "";
    	document.getElementById('item_input').value = "";
    	
    });
    
    $('#box_name_input').keypress(function(e) {
    	document.getElementById('item_input').value = "";
    	
    });
	
	$('#categories').change(function() {
		document.getElementById('box_name_input').value = "";
   		document.getElementById('item_input').value = "";
   	});
   	
   	$('#box_names').change(function() {
   		document.getElementById('item_input').value = "";
   	});
	
	// Set the 'on change' event for the categories list.
    $('#categories').click(function() {
        var selectedCategory = $('#categories option:selected').val();
        if(selectedCategory != undefined)
        {
        	var catagory_box = document.getElementById('catagory_input');
        	catagory_box.value = selectedCategory.split(" - ")[1];
        	var catagory_letter_box = document.getElementById('catagory_letter_input');
        	catagory_letter_box.value = selectedCategory.split(" - ")[0];
        	
        	// Get the list of box names for the selected category.
        	Dajaxice.inventory.get_box_names(getBoxNames, { 'category_name': selectedCategory.split(" - ")[1] });
        }
    });
    
    // Set the 'on change' event for the box names list.
    $('#box_names').click(function() {
        var selectedBoxName = $('#box_names option:selected').val();
        if(selectedBoxName != undefined)
        {
        	var box_name_box = document.getElementById('box_name_input');
       		box_name_box.value = selectedBoxName;
       		document.getElementById('catagory_input').value = $('#categories option:selected').val().split(" - ")[1];
       		document.getElementById('catagory_letter_input').value = $('#categories option:selected').val().split(" - ")[0];
       
        	// Get the list of items for the selected box name.
        	Dajaxice.inventory.get_items(getItems, { 'box_name': selectedBoxName });
        }
    });
    
    // Set the 'on change' event for the items list.
    $('#items').click(function() {
        var selectedItem = $('#items option:selected').val();
        if(selectedItem != undefined)
        {
        	var item_box = document.getElementById('item_input');
        	item_box.value = selectedItem;
        	document.getElementById('catagory_input').value = $('#categories option:selected').val().split(" - ")[1];
       		document.getElementById('catagory_letter_input').value = $('#categories option:selected').val().split(" - ")[0];
			document.getElementById('box_name_input').value = $('#box_names option:selected').val();
        }
    });
    
    //on click event for creating a new item
    $('#add_new_item').click(function(e) {
    	var name = $('input[name=item_input]').val();
    	var box_name = $('input[name=box_name_input]').val();
    	var description = $('input[name=item_description]').val();
    	
    	Dajaxice.catalog.create_item(createItem, 
            {
                'b_name': box_name,
                'item_name': name,
                'd': description
            }
        );
    });	
});