// Функция для получения значения куки по имени
function getCookie(name) {
    const cookieString = document.cookie;
    const cookies = cookieString.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return null;
}

// Асинхронная функция для создания истории
async function createHistoryClient(city) {
    const user_id = getCookie('user_id');
    if (!user_id) {
        console.error('user_id cookie not found');
        return false;
    }

    const url = "http://localhost:8000/api/v1/histories/";
    const data = {
        city: city,
        user_id: user_id,
    };

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('Success:', responseData);
        return true;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}

// Обработчик отправки формы
document.getElementById('cityForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы

    const cityInput = document.getElementById('input');
    const city = cityInput.value.trim();

    const success = await createHistoryClient(city);

    if (success) {
        // Отправляем форму традиционно после успешного fetch
        this.submit();
    };
});
