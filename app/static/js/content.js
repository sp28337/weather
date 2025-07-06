const track = document.querySelector('.slider-track');
const slides = document.querySelectorAll('.slide');
const first = document.querySelector('.first');
const second = document.querySelector('.second');
const third = document.querySelector('.third');
let current = 0;

// Кнопки
first.onclick = () => goToSlide(0);
second.onclick = () => goToSlide(1);
third.onclick = () => goToSlide(2);

function goToSlide(idx) {
    // Обновляем классы активных кнопок
    if (idx === 0) {
        first.classList.add('active');
        second.classList.remove('active');
        third.classList.remove('active');
    } else if (idx === 1) {
        first.classList.remove('active');
        second.classList.add('active');
        third.classList.remove('active');
    } else {
        first.classList.remove('active');
        second.classList.remove('active');
        third.classList.add('active');
    }

    // Ограничиваем индекс, чтобы не было зацикливания
    if (idx < 0) idx = 0;
    if (idx >= slides.length) idx = slides.length - 1;

    current = idx;
    track.style.transition = 'transform 0.4s ease';
    track.style.transform = `translateX(-${current * 100}%)`;
}

// Свайп
let startX = 0;
let currentTranslate = 0;
let isDragging = false;

track.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
    isDragging = true;
    currentTranslate = -current * track.clientWidth; // текущий сдвиг в px
    track.style.transition = ''; // отключаем плавность для перетаскивания
});

track.addEventListener('touchmove', (e) => {
    if (!isDragging) return;

    const touchX = e.touches[0].clientX;
    let diff = touchX - startX;

    // Логика ограничения оттягивания:
    // Ограничение для первого слайда
    if (current === 0 && diff > 0) {
        diff = Math.min(diff, 50);
    }
    // Ограничение для центрального слайда (например, если current === centralIndex)
    const centralIndex = Math.floor(slides.length / 2);
    if (current === centralIndex && (diff > 0 || diff < 0)) {
        diff = Math.min(Math.max(diff, -50), 50);
    }
    // Ограничение для последнего слайда
    if (current === slides.length - 1 && diff < 0) {
        diff = Math.max(diff, -50);
    }

    // Смещаем трек на текущий сдвиг + разницу свайпа
    track.style.transform = `translateX(${currentTranslate + diff}px)`;
});

track.addEventListener('touchend', (e) => {
    if (!isDragging) return;
    isDragging = false;
    const endX = e.changedTouches[0].clientX;
    const diff = endX - startX;

    // Порог для переключения слайда
    const threshold = 50;

    // Если свайп вправо и не первый слайд — переключаемся назад
    if (diff > threshold && current > 0) {
        goToSlide(current - 1);
    }
    // Если свайп влево и не последний слайд — переключаемся вперед
    else if (diff < -threshold && current < slides.length - 1) {
        goToSlide(current + 1);
    }
    // Иначе — возвращаемся к текущему слайду с анимацией (bounce back)
    else {
        track.style.transition = 'transform 0.3s ease';
        track.style.transform = `translateX(-${current * 100}%)`;
    }
});
