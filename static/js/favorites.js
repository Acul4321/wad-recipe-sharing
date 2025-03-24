class FavoriteManager {
    constructor(options) {
        this.options = options;
        this.button = document.getElementById('favorite-btn');
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        this.initEvents();
    }

    initEvents() {
        this.button.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleFavorite();
        });
    }

    toggleFavorite() {
        const starUse = this.button.querySelector('use');
        const spanText = this.button.querySelector('span');
        
        fetch(this.options.submitUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (data.is_favorite) {
                    this.button.classList.remove('btn-outline-danger');
                    this.button.classList.add('btn-danger');
                    starUse.setAttribute('class', 'star-filled');
                    spanText.textContent = 'Unfavorite';
                } else {
                    this.button.classList.remove('btn-danger');
                    this.button.classList.add('btn-outline-danger');
                    starUse.setAttribute('class', 'star-empty');
                    spanText.textContent = 'Favorite';
                }
            }
        });
    }
}
