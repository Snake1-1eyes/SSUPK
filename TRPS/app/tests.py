from django.test import TestCase
import unittest
from datetime import datetime, timedelta

def isValidDate(dateStr):
    try:
        day, month, year = map(int, dateStr.split('.'))
        date = datetime(year, month, day)
        return date.day == day and date.month == month and date.year == year
    except ValueError:
        return False

def validateDates(startDateStr, endDateStr):
    minDate = datetime(2013, 1, 1)
    maxDate = datetime(2024, 6, 1)

    if not isValidDate(startDateStr):
        return "Неверный формат даты начала"
    if not isValidDate(endDateStr):
        return "Неверный формат даты окончания"

    startDay, startMonth, startYear = map(int, startDateStr.split('.'))
    endDay, endMonth, endYear = map(int, endDateStr.split('.'))

    if not (1 <= startMonth <= 12) or not (1 <= endMonth <= 12):
        return "Месяц должен быть от 1 до 12"

    startDate = datetime(startYear, startMonth, startDay)
    endDate = datetime(endYear, endMonth, endDay)

    if startDate < minDate:
        return "Дата начала не может быть ранее 2013 года"
    if endDate > maxDate:
        return "Дата окончания не может быть позднее 01.06.2024"

    if endDate <= startDate:
        return "Дата окончания должна быть позже даты начала"

    one_month_later = startDate.replace(day=28) + timedelta(days=4)
    one_month_later = one_month_later.replace(day=1)
    if endDate < one_month_later:
        return "Минимальный период - 1 месяц"

    totalMonthsDifference = (endDate.year - startDate.year) * 12 + (endDate.month - startDate.month)
    if totalMonthsDifference > 60:
        return "Разница годов не должна превышать 5 лет"

    return ""

class TestDateValidation(unittest.TestCase):

    def test_isValidDate_valid(self):
        self.assertTrue(isValidDate('01.01.2020'))
        self.assertTrue(isValidDate('31.12.2020'))
        self.assertTrue(isValidDate('29.02.2020'))  # Високосный год

    def test_isValidDate_invalid(self):
        self.assertFalse(isValidDate('32.01.2020'))
        self.assertFalse(isValidDate('31.13.2020'))
        self.assertFalse(isValidDate('29.02.2019'))  # Не високосный год

    def test_validateDates_valid(self):
        self.assertEqual(validateDates('01.01.2020', '01.02.2020'), '')
        self.assertEqual(validateDates('01.01.2015', '01.01.2020'), '')

    def test_validateDates_invalid_format(self):
        self.assertEqual(validateDates('01-01-2020', '01.02.2020'), 'Неверный формат даты начала')
        self.assertEqual(validateDates('01.01.2020', '01-02-2020'), 'Неверный формат даты окончания')

    def test_validateDates_invalid_month(self):
        self.assertEqual(validateDates('01.13.2020', '01.02.2020'), 'Неверный формат даты начала')
        self.assertEqual(validateDates('01.01.2020', '01.00.2020'), 'Неверный формат даты окончания')

    def test_validateDates_out_of_range(self):
        self.assertEqual(validateDates('31.12.2012', '01.01.2020'), 'Дата начала не может быть ранее 2013 года')
        self.assertEqual(validateDates('01.01.2020', '02.06.2024'), 'Дата окончания не может быть позднее 01.06.2024')

    def test_validateDates_end_before_start(self):
        self.assertEqual(validateDates('01.02.2020', '01.01.2020'), 'Дата окончания должна быть позже даты начала')

    def test_validateDates_minimum_period(self):
        self.assertEqual(validateDates('01.01.2020', '31.01.2020'), 'Минимальный период - 1 месяц')

    def test_validateDates_maximum_period(self):
        self.assertEqual(validateDates('01.01.2015', '01.02.2021'), 'Разница годов не должна превышать 5 лет')

if __name__ == '__main__':
    unittest.main()