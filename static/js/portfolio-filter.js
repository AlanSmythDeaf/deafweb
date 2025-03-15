document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('category-select');
    const portfolioItems = document.querySelectorAll('.portfolio-item');

    categorySelect.addEventListener('change', function() {
        const selectedCategory = this.value;

        portfolioItems.forEach(item => {
            if (selectedCategory === 'all' || item.dataset.category === selectedCategory) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
});
