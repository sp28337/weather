async function fetchSuggestions() {
        const inputField = document.getElementById("input");
        const suggestionsWrapper = document.getElementById("suggestions");
        const query = inputField.value;
        const queryParams = new URLSearchParams({
            query: inputField.value
        })

        // Очищаем подсказки, если ничего не введено
        if (query.length < 3) {
            suggestionsWrapper.style.display = "none";
            suggestionsWrapper.innerHTML = "";
            return;
        }

        try {
            const response = await fetch(`/autocomplete?${queryParams.toString()}`);
            const data = await response.json();

            if (response.ok && Array.isArray(data)) {
                suggestionsWrapper.innerHTML = "";

                if (data.length === 0) {
                    suggestionsWrapper.style.display = "none";
                    return;
                }

                suggestionsWrapper.style.display = "block";

                data.forEach(city => {
                    const item = document.createElement("li");
                    item.textContent = `${city.name} (${city.country})`;
                    item.onclick = () => {
                        inputField.value = city.name; // Подставляем выбранное значение
                        suggestionsWrapper.style.display = "none";
                        suggestionsWrapper.innerHTML = ""; // Очищаем список подсказок
                    };
                    suggestionsWrapper.appendChild(item);
                });
            } else {
                suggestionsWrapper.innerHTML = "<li>No suggestions found.</li>";
            }
        } catch (e) {
            console.error("Error fetching autocomplete suggestions:", e);
            suggestionsWrapper.style.display = "none";
        }
    }