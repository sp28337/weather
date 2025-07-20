document.querySelectorAll('.historyRow').forEach(function(row) {
    row.addEventListener('click', function() {
        const city = this.getAttribute('data-city');
        if (!city) {
            return
        }
        const encodedCity = encodeURIComponent(city);
        // Переход на страницу прогноза
        window.location.href = `/?city=${encodedCity}`;
    });
});
