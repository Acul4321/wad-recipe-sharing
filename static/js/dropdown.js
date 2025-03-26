document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.querySelector('.dropdown');
    if (dropdown) {
        dropdown.addEventListener('click', function() {
            const content = this.querySelector('.dropdown-content');
            content.hidden = !content.hidden;
        });
    }
});
