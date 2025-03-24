document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('recipe-search');
    const searchResults = document.getElementById('search-results');
    let timeoutId;

    function updateSearchResults(data) {
        searchResults.innerHTML = '';
        if (data.recipes.length > 0) {
            data.recipes.forEach(recipe => {
                const div = document.createElement('div');
                div.className = 'search-result-item';
                div.innerHTML = `
                    <a href="/world-recipe/recipe/${recipe.country}/${recipe.meal_type}/${recipe.slug}/">
                        <img src="${recipe.image || '/static/images/default.png'}" alt="${recipe.title}">
                        <div>
                            <h4>${recipe.title}</h4>
                            <p>${recipe.country}</p>
                        </div>
                    </a>
                `;
                searchResults.appendChild(div);
            });
            searchResults.style.display = 'block';
        } else {
            searchResults.innerHTML = '<div class="no-results">No recipes found</div>';
            searchResults.style.display = 'block';
        }
    }

    function performSearch(query) {
        fetch(`/world-recipe/search/?q=${encodeURIComponent(query)}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(updateSearchResults);
    }

    searchInput.addEventListener('input', function() {
        clearTimeout(timeoutId);
        
        if (this.value.length < 2) {
            searchResults.style.display = 'none';
            return;
        }

        timeoutId = setTimeout(() => performSearch(this.value), 300);
    });

    // hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
});
