function isValidDate(dateStr) {
    const [day, month, year] = dateStr.split('.').map(Number);
    const date = new Date(year, month - 1, day);
    return date.getDate() === day &&
        date.getMonth() === month - 1 &&
        date.getFullYear() === year;
}

function validateDates(startDateStr, endDateStr) {
    const [startDay, startMonth, startYear] = startDateStr.split('.').map(Number);
    const [endDay, endMonth, endYear] = endDateStr.split('.').map(Number);

    const startDate = new Date(startYear, startMonth - 1, startDay);
    const endDate = new Date(endYear, endMonth - 1, endDay);
    const minDate = new Date(2013, 0, 1);
    const maxDate = new Date(2024, 5, 1); // 1 июня 2024

    if (!isValidDate(startDateStr)) {
        return "Неверный формат даты начала";
    }
    if (!isValidDate(endDateStr)) {
        return "Неверный формат даты окончания";
    }

    // Проверяем месяцы
    if (startMonth < 1 || startMonth > 12 || endMonth < 1 || endMonth > 12) {
        return "Месяц должен быть от 1 до 12";
    }

    // Проверяем диапазон дат
    if (startDate < minDate) {
        return "Дата начала не может быть ранее 2013 года";
    }
    if (endDate > maxDate) {
        return "Дата окончания не может быть позднее 01.06.2024";
    }

    // Проверяем, что конечная дата больше начальной
    if (endDate <= startDate) {
        return "Дата окончания должна быть позже даты начала";
    }

    // Проверяем минимальную разницу в один месяц
    const oneMonthLater = new Date(startDate);
    oneMonthLater.setMonth(startDate.getMonth() + 1);
    if (endDate < oneMonthLater) {
        return "Минимальный период - 1 месяц";
    }

    const yearDifference = endDate.getFullYear() - startDate.getFullYear();
    const monthDifference = endDate.getMonth() - startDate.getMonth();
    const totalMonthsDifference = yearDifference * 12 + monthDifference;

    if (totalMonthsDifference > 60) { // 5 лет * 12 месяцев
        return "Разница годов не должна превышать 5 лет";
    }

    return ""; // Пустая строка означает отсутствие ошибок
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('dateForm').addEventListener('submit', function (e) {
        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;

        const errorMessage = validateDates(startDate, endDate);

        if (errorMessage) {
            e.preventDefault(); // Отменяем отправку формы
            document.getElementById('start_date_error').textContent = errorMessage;
            document.getElementById('start_date_error').style.display = 'block';
            document.getElementById('start_date').classList.add('is-invalid');
        }
    });

    document.querySelectorAll('input[type="text"]').forEach(input => {
        input.addEventListener('input', function () {
            let value = this.value.replace(/\D/g, ''); // Оставляем только цифры
            if (value.length > 8) value = value.substr(0, 8);

            if (value.length >= 4) {
                value = value.substr(0, 2) + '.' + value.substr(2, 2) + '.' + value.substr(4);
            } else if (value.length >= 2) {
                value = value.substr(0, 2) + '.' + value.substr(2);
            }

            this.value = value;
        });
    });
});