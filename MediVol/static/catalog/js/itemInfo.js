function hideEditControls() {
    $('#saveItem').hide();
    $('#cancelEdit').hide();
    $('#editItem').show();

    $('#itemNameValue').show();
    $('#boxNameValue').show();
    $('#descriptionValue').show();

    $('#name').hide();
    $('#boxName').hide();
    $('#description').hide();
}

function showEditControls() {
    $('#saveItem').show();
    $('#cancelEdit').show();
    $('#editItem').hide();

    $('#itemNameValue').hide();
    $('#boxNameValue').hide();
    $('#descriptionValue').hide();

    $('#name').show();
    $('#boxName').show();
    $('#description').show();
}

function saveItem() {

}

function discardChanges() {
    $('#name').val($('#itemNameValue').html());
    $('#boxName').val($('#boxNameValue').html());

    var description = $('#description').html();

    if (description !== '<i>no description</i>') {
        $('#description').val(description);
    } else {
        $('#description').val('');
    }
}

$(document).ready(function() {
    // This sets up the google-style autocomplete field.
    $('#boxName').autocomplete(
        {
            autoFocus: true,
            // The 'source' attribute is a function that is called
            // which provides the data for the autocomplete. It passes
            // in request, which provides the search query, and the response
            // callback, which we are expected to give an array of relevant
            // search results.
            source: function(request, response) {
                // Call the get_search_results AJAX function.
                Dajaxice.catalog.search_box_names(function(returned) {
                    // 'returned' is passed to us from the AJAX function.
                    // It is an array of relevant search results which we pass
                    // to the 'response' callback.
                    response(returned);
                }, { 'query': request.term });
            },
            // This is just a setting so that the autocomplete plugin doesn't
            // add any messages next to our search field.
            messages: {
                noResults: '',
                results: function() {}
            },
            // This is a callback that says what to do when the autocomplete
            // dropdown is closed.
            close: function() {
                // This is the search result given by the AJAX function.
                // It is of one of the following forms:
                // Category > Box Name > Item
                // Category > Box Name
                // Category
                var query = $('#itemSearch').val();
                var actualQuery = query;

                // We want to get what the user was actually searching for, so we
                // find last term after the last '> '.
                if (query.lastIndexOf('> ') != -1) {
                    actualQuery = query.substr(query.lastIndexOf('> ') + 2, query.length);
                }

                // Then we put the actual query back into the field.
                $('#itemSearch').val(actualQuery);
            }
        }
    );

    $('#editItem').click(function() {
        showEditControls();
    });

    $('#saveItem').click(function() {
        hideEditControls();
    });

    $('#cancelEdit').click(function() {
        hideEditControls();
        discardChanges();
    });
});
