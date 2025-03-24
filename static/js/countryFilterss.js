class CountryFilters {
    constructor() {
        this.mealTypeSelect = $('#meal-type');
        this.sortBySelect = $('#sort-by');
        this.recipeList = $('#recipe-list');
        this.bindEvents();
    }

    bindEvents() {
        this.mealTypeSelect.change(() => this.updateFilters());
        this.sortBySelect.change(() => this.updateFilters());
    }

    updateFilters() {
        const params = {
            'meal_type': this.mealTypeSelect.val(),
            'sort_by': this.sortBySelect.val()
        };

        $.ajax({
            url: window.COUNTRY_URL,
            data: params,
            success: (response) => {
                this.recipeList.html($(response).find('#recipe-list').html());
                this.updateUrl(params);
            }
        });
    }

    updateUrl(params) {
        const newUrl = new URL(window.location.href);
        Object.entries(params).forEach(([key, value]) => {
            newUrl.searchParams.set(key, value);
        });
        window.history.pushState({path: newUrl.toString()}, '', newUrl.toString());
    }
}

// init filters when DOM is ready
$(document).ready(() => new CountryFilters());
