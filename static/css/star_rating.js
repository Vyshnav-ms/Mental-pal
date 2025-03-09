document.addEventListener('DOMContentLoaded', function() {
    const ratingInputs = document.querySelectorAll('.star-rating input[type="radio"]');
    ratingInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Optional: Add any dynamic behavior on rating change
        });
    });
});