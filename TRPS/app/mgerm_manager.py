from dateutil.relativedelta import relativedelta
from django.db import connections


class MgermManager:
    def __init__(self):
        self._cursor = connections['mgerm'].cursor()

    def get_patients_count(self):
        execute_query = """
            SELECT DISTINCT COUNT(pl.patientID)
            FROM patients_list pl;
            """
        self._cursor.execute(execute_query)
        result = self._cursor.fetchone()
        return result[0]

    def get_cards_count(self):
        execute_query = """
            SELECT DISTINCT COUNT(sct.patientID)
            FROM stat_cards_table sct
            JOIN patients_list pl
            ON pl.patientID = sct.patientID;
            """
        self._cursor.execute(execute_query)
        result = self._cursor.fetchone()
        return result[0]

    def get_incorrect_cards_count(self):
        execute_query = """
            SELECT DISTINCT COUNT(sct.hystoryNumber)
            FROM stat_cards_table sct
            WHERE
                sct.in_date IS NULL
                OR sct.out_date IS NULL
                OR sct.Diagnoz IS NULL
                OR sct.ageIN IS NULL
                OR sct.ageOUT IS NULL
                OR sct.ageOUT < sct.ageIN;
            """
        self._cursor.execute(execute_query)
        result = self._cursor.fetchone()
        return result[0]

    def get_observation_time(self):
        execute_query = """
            SELECT
                sct.patientID,
                MIN(sct.in_date) AS min_in_date,
                MAX(sct.out_date) AS max_out_date
            FROM
                stat_cards_table sct
            GROUP BY
                sct.patientID;
            """
        self._cursor.execute(execute_query)
        result = self._cursor.fetchall()

        data = dict()
        for row in result:
            delta = relativedelta(row[2], row[1])

            if delta.years in data.keys():
                data[delta.years] += 1
            else:
                data[delta.years] = 1

        return data

    def get_age_gender_distribution(self):
        execute_query = """
            SELECT
                di.sx,
                di.age,
                COUNT(*) AS counter
            FROM
                department_income di
            GROUP BY
                di.sx,
                di.age;
            """
        self._cursor.execute(execute_query)
        result = self._cursor.fetchall()

        ages = [f'От {age * 10} до {age * 10 + 9}' for age in range(0, 10)]
        distribution = {0: {key: 0 for key in ages}, 1: {key: 0 for key in ages}}
        for row in result:
            gender = row[0]
            age = row[1]
            count = row[2]
            age_title = f'От {age // 10 * 10} до {age // 10 * 10 + 9}'

            distribution[gender][age_title] += count

        return distribution
