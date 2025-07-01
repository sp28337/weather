async function fetchWeather() {
        const inputField = document.getElementById("input");
        const resultWrapper = document.getElementById("suggestions");
        const query = inputField.value;
        const queryParams = new URLSearchParams({
            query: inputField.value
        })

        if (query.length < 3) {
            resultWrapper.innerHTML = "";
            return;
        }

        try {
            const response = await fetch(`/result?${queryParams.toString()}`);
            const data = await response.json();

            if (response.ok && Array.isArray(data)) {
                resultWrapper.innerHTML = "";
                data.forEach(city => {
                    const item = document.createElement("li");
                    item.textContent = `${city.name} (${city.country})`;
                    item.onclick = () => {
                        inputField.value = city.name; // Подставляем выбранное значение
                        resultWrapper.innerHTML = ""; // Очищаем список подсказок

                    };
                    resultWrapper.appendChild(item);
                });
            } else {
                resultWrapper.innerHTML = "<li>No result found.</li>";
            }
        } catch (e) {
            console.error("Error fetching result:", e);
        }
    }