// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    // FAQ accordion functionality
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const header = item.querySelector('.faq-header');
        const content = item.querySelector('.faq-content');
        
        header.addEventListener('click', () => {
            // Toggle current item
            content.classList.toggle('show');
            header.querySelector('.toggle-icon').classList.toggle('rotate');
            
            // Close other items
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.querySelector('.faq-content').classList.remove('show');
                    otherItem.querySelector('.toggle-icon').classList.remove('rotate');
                }
            });
        });
    });
    
    // Mentor filtering functionality
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(filterForm);
            const params = new URLSearchParams(formData);
            window.location.href = `${window.location.pathname}?${params.toString()}`;
        });
    }
    
    // Rating stars functionality
    const ratingInputs = document.querySelectorAll('.rating-input');
    const ratingStars = document.querySelectorAll('.rating-star');
    
    if (ratingStars.length > 0) {
        ratingStars.forEach((star, index) => {
            star.addEventListener('click', () => {
                // Update hidden input value
                document.querySelector('input[name="rating"]').value = index + 1;
                
                // Update star display
                ratingStars.forEach((s, i) => {
                    if (i <= index) {
                        s.classList.add('active');
                    } else {
                        s.classList.remove('active');
                    }
                });
            });
        });
    }
});