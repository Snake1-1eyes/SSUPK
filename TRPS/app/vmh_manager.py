# from collections import Counter
# from django.db import connections
# from .ml import *


# class VmhDbManager:
#     def __init__(self):
#         self._cursor = connections['vmh_mgerm'].cursor()

    # def get_genetic_diseases(self):
    #     execute_query = """
    #         SELECT genetic_deseases
    #         FROM 3_ana_vitae
    #         WHERE genetic_deseases IS NOT NULL;
    #         """

    #     self._cursor.execute(execute_query)
    #     result = self._cursor.fetchall()
    #     sentences = [row[0] for row in result]

    #     predictions = predict_genetic_diseases(sentences)

    #     return predictions

    # def get_education_stats(self):
    #     execute_query = """
    #         SELECT
    #             dsd.`Obrazovanie_(dlitelnost)`,
    #             COUNT(*)
    #         FROM
    #             dopolnitelnie_statisticheskie_dannie dsd
    #         WHERE
    #             dsd.`Obrazovanie_(dlitelnost)` IS NOT NULL
    #         GROUP BY
    #             dsd.`Obrazovanie_(dlitelnost)`
    #         ORDER BY
    #             dsd.`Obrazovanie_(dlitelnost)`;
    #         """

    #     self._cursor.execute(execute_query)
    #     result = self._cursor.fetchall()

    #     education_duration = {
    #         "Меньше 1 года": result[0][1],
    #         "1 год": result[1][1],
    #         "2 года": result[2][1],
    #         "3 года": result[3][1],
    #         "4 года": result[4][1],
    #         "5 лет": result[5][1],
    #     }

    #     return education_duration

    # def get_family_history(self):
    #     execute_query = """
    #         SELECT av.family_hyst
    #         FROM 3_ana_vitae av
    #         WHERE av.family_hyst IS NOT NULL;
    #         """
    #     self._cursor.execute(execute_query)
    #     result = self._cursor.fetchall()
    #     data = [row[0] for row in result]

    #     predictions = predict_family_relations(data)

    #     return predictions

#     def get_kids_count(self):
#         execute_query = """
#             SELECT
#                 dsd.Kolichestvo_detey,
#                 COUNT(*)
#             FROM
#                 dopolnitelnie_statisticheskie_dannie dsd
#             WHERE
#                 dsd.Kolichestvo_detey IS NOT NULL
#                 AND dsd.Kolichestvo_detey > 0
#             GROUP BY
#                 dsd.Kolichestvo_detey
#             ORDER BY
#                 dsd.Kolichestvo_detey;
#             """
#         self._cursor.execute(execute_query)
#         result = self._cursor.fetchall()
#         kids_count = {
#             "1 ребенок": result[0][1],
#             "2 ребенка": result[1][1],
#             "3 ребенка": result[2][1],
#             "4 ребенка": result[3][1],
#             "5 детей": result[4][1],
#         }

#         return kids_count

#     def get_work_relations(self):
#         execute_query = """
#             SELECT av.working
#             FROM 3_ana_vitae av
#             WHERE av.working IS NOT NULL;
#             """
#         self._cursor.execute(execute_query)
#         result = self._cursor.fetchall()
#         data = [row[0] for row in result]

#         predictions = predict_work_relations(data)

#         return predictions
