function calculateTotalPrice(cb) { 

    var totalPrice = 0.0;
  
    $('#boxes_added tr td :input').each(function() { 
         
        var price =$(this).val();
        totalPrice = totalPrice + parseFloat(price);
    }); 

    cb(totalPrice);
}

function displayTotalPrice() { 

    calculateTotalPrice(function (totalPrice) { 
    
        $('#total_price').empty();
        $('#total_price').append(totalPrice);
    });
}
