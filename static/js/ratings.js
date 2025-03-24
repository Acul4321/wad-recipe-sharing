class RatingManager {
    constructor(options) {
        this.options = options;
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        this.displayStars = document.querySelector('.current-rating .stars').children;
        this.updateStars(this.displayStars, options.initialRating);
        if (options.isAuthenticated) {
            this.initRatingEvents();
        }
    }

    initRatingEvents() {
        const ratingStars = document.querySelectorAll('.rating-star');
        
        ratingStars.forEach(star => {
            star.addEventListener('mouseover', () => {
                this.highlightStars(ratingStars, star.dataset.rating);
            });
        });

        document.querySelector('.rating-stars').addEventListener('mouseout', () => {
            ratingStars.forEach(star => {
                star.querySelector('use').setAttribute('class', 'star-empty');
            });
        });

        ratingStars.forEach(star => {
            star.addEventListener('click', () => {
                this.submitRating(star.dataset.rating);
            });
        });
    }

    updateStars(stars, rating) {
        for(let i = 0; i < stars.length; i++) {
            const use = stars[i].querySelector('use');
            if(i < Math.floor(rating)) {
                use.setAttribute('class', 'star-filled');
            } else if(i === Math.floor(rating) && rating % 1 > 0) {
                use.setAttribute('class', 'star-half');
            } else {
                use.setAttribute('class', 'star-empty');
            }
        }
    }

    highlightStars(stars, rating) {
        stars.forEach((star, index) => {
            const use = star.querySelector('use');
            use.setAttribute('class', index < rating ? 'star-filled' : 'star-empty');
        });
    }

    submitRating(rating) {
        fetch(this.options.submitUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
            },
            body: JSON.stringify({ rating: rating })
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                document.querySelector('.rating-value').textContent = `(${data.new_average.toFixed(1)})`;
                this.updateStars(this.displayStars, data.new_average);
            }
        });
    }
}
