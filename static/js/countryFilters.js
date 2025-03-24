$(document).ready(function () {
    // pass the country URL dynamically from the data-url attribute
    var countryUrl = $('#ajax-url').data('url');

    // When meal type changes
    $('#meal-type').change(function () {
        var meal_type = $(this).val();
        
        $.ajax({
            url: countryUrl,  // countr url wl change dynamically
            data: {
                'meal_type': meal_type,
                'sort_by': $('#sort-by').val()
            },
            success: function (response) {
                $('#recipe-list').html($(response).find('#recipe-list').html());

                var newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?meal_type=' + meal_type + '&sort_by=' + $('#sort-by').val();
                window.history.pushState({ path: newUrl }, '', newUrl);
            }
        });
    });

    // when sort option changes
    $('#sort-by').change(function () {
        var sort_by = $(this).val();

        $.ajax({
            url: countryUrl,  // country name dynamic again
            data: {
                'meal_type': $('#meal-type').val(),
                'sort_by': sort_by
            },
            success: function (response) {
                $('#recipe-list').html($(response).find('#recipe-list').html());

                var newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?meal_type=' + $('#meal-type').val() + '&sort_by=' + sort_by;
                window.history.pushState({ path: newUrl }, '', newUrl);
            }
        });
    });
});

