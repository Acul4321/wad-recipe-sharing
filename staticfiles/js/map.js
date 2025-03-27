function initMap() {
    // wait for DOM to be ready
    if (!document.getElementById('recipe-map')) {
        console.error('Map container not found');
        return;
    }

    // Map config
    const mapOptions = {
        zoom: 2,
        center: { lat: 20, lng: 0 },
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: true,
        streetViewControl: false
    };

    const map = new google.maps.Map(document.getElementById('recipe-map'), mapOptions);
    
    if (!window.recipeData) {
        console.error('Recipe data not found');
        return;
    }

    // process recipes and create markers
    const uniqueCountries = groupRecipesByCountry(window.recipeData);
    createCountryMarkers(map, uniqueCountries);
}

function groupRecipesByCountry(recipes) {
    const seenRecipes = new Set();
    return recipes.reduce((acc, recipe) => {
        if (!seenRecipes.has(recipe.slug)) {
            seenRecipes.add(recipe.slug);
            if (!acc.has(recipe.country)) {
                acc.set(recipe.country, []);
            }
            acc.get(recipe.country).push(recipe);
        }
        return acc;
    }, new Map());
}

function createCountryMarkers(map, uniqueCountries) {
    uniqueCountries.forEach((recipes, country) => {
        const geocoder = new google.maps.Geocoder();
        
        geocoder.geocode({ address: country }, (results, status) => {
            if (status === 'OK' && results[0]) {
                const marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    title: country,
                    animation: google.maps.Animation.DROP
                });

                const countrySlug = slugify(country);
                const infoWindow = createInfoWindow(country, countrySlug, recipes);

                marker.addListener('click', () => {
                    infoWindow.open(map, marker);
                });
            } else {
                console.error(`Geocoding failed for ${country}: ${status}`);
            }
        });
    });
}

function createInfoWindow(country, countrySlug, recipes) {
    const recipesList = recipes.map(recipe => 
        `<li><a href="${recipe.url}">${recipe.title}</a></li>`
    ).join('');

    const contentString = `
        <div class="map-info-window">
            <h3>${country}</h3>
            <p>Available Recipes:</p>
            <ul>${recipesList}</ul>
            <a href="/world-recipe/recipe/${countrySlug}/">View All Recipes from ${country}</a>
        </div>
    `;

    return new google.maps.InfoWindow({
        content: contentString,
        maxWidth: 300
    });
}

function slugify(text) {
    return text.toLowerCase().replace(/\s+/g, '-');
}

// init map when the page loads
document.addEventListener('DOMContentLoaded', initMap);