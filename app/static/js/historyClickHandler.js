document.querySelectorAll('.historyRow').forEach(function(row) {
    row.addEventListener('click', function() {
        const city = this.getAttribute('data-city');
        // Преобразуем в URL-friendly (например, если нужны пробелы заменить на %20)
        const encodedCity = encodeURIComponent(city);
        // Переход на страницу прогноза
        window.location.href = `/?city=${encodedCity}`; // или другой ваш маршрут
    });
});
