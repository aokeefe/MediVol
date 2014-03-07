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
	if(response.success == 1){
		setChangeMessageSuccess(response.message);
	}
	else{
		setChangeMessageError(response.message);
	}
	Dajaxice.inventory.get_items(getItems, { 'box_name': $('#box_names option:selected').val() });
}

function updateDescription(response){
	document.getElementById('item_description').value = response.message;
}

//display success massage when new item is created
function setChangeMessageSuccess(message) {
	document.getElementById("changeMessage").className = "changeSuccess";
    $('#changeMessage').html(message);
}

//display error massage when new item can not be created
function setChangeMessageError(message) {
	document.getElementById("changeMessage").className = "changeError";
    $('#changeMessage').html(message);
}

//clear the message
function setChangeMessageClear() {
	document.getElementById("changeMessage").className = "noChangeMessage";
    $('#changeMessage').html('');
}


function setItemSelected(itemName) {
    $('#itemSelectedMessage').removeClass('noItemSelected');
    $('#itemSelectedMessage').addClass('itemSelected');
    $('#itemSelectedMessage').html('You have selected: <br /><b>' + itemName + '</b>');
}

function setItemNotSelected() {
    $('#itemSelectedMessage').removeClass('itemSelected');
    $('#itemSelectedMessage').addClass('noItemSelected');
    $('#itemSelectedMessage').html('Please select an item.');
}

$(document).ready(function() {
    
    // Set the 'on change' event for the items list.
    $('#items').change(function() {
        setItemSelected($('#items option:selected').val());
    });
    
    $('#catagory_input').keyup(function(e) {
    	document.getElementById('box_name_input').value = "";
    	document.getElementById('item_input').value = "";
    	
    });
    
    $('#box_name_input').keyup(function(e) {
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
        	document.getElementById('catagory_input').value = selectedCategory.split(" - ")[1];
        	document.getElementById('catagory_letter_input').value = selectedCategory.split(" - ")[0];
        	
        	// Get the list of box names for the selected category.
        	Dajaxice.inventory.get_box_names(getBoxNames, { 'category_name': selectedCategory.split(" - ")[1] });
        }
    });
    
    // Set the 'on change' event for the box names list.
    $('#box_names').click(function() {
        var selectedBoxName = $('#box_names option:selected').val();
        if(selectedBoxName != undefined)
        {
        	document.getElementById('box_name_input').value = selectedBoxName;
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
        	document.getElementById('item_input').value = selectedItem;
        	document.getElementById('catagory_input').value = $('#categories option:selected').val().split(" - ")[1];
       		document.getElementById('catagory_letter_input').value = $('#categories option:selected').val().split(" - ")[0];
			var box_name = $('#box_names option:selected').val();
			document.getElementById('box_name_input').value = box_name;
			Dajaxice.catalog.get_description(updateDescription, 
            {
                'box_name': box_name,
                'item_name': selectedItem,
            }
        );
        }
    });
    
    //on click event for creating a new item
    $('#add_new_item').click(function(e) {
    	var name = $('#item_input').val();
    	var box_name = $('#box_name_input').val();
    	var description = $('#item_description').val();
    	
    	Dajaxice.catalog.create_item(createItem, 
            {
                'box_name': box_name,
                'item_name': name,
                'description': description
            }
        );

    });
    
/*
    $('#edit_item').click(function(e) {
    	var new_name = $('#item_input').val();
    	var old_name = $('#items option:selected').val();
    	var new_box_name = $('#box_names option:selected').val();
    	var old_box_name = $('#box_name_input').val();
    	var description = $('#item_description').val();
    	var letter = $('#catagory_letter_input').val();
    	
    	Dajaxice.catalog.edit_item(editItem, 
            {
                'category_letter': letter,
                'new_box_name': new_box_name,
                'old_box_name': old_box_name,
                'new_item_name': new_name,
                'old_item_name': old_name,
                'd': description
            }
        );
    });
    
    $('#delete_item').click(function(e) {
    	var item_name = $('#items option:selected').val();
    	var box_name = $('#box_names option:selected').val();
    	if(item_name!= undefined){
    		Dajaxice.catalog.delete_item(deleteItem, 
            	{
                	'b_name': box_name,
                	'item_name': item_name,
            	}
        	);
        }
    });
*/
});