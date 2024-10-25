from django.db import models
from django.db.models import Count
from django.db import connections
from .ml import *

class StatCard(models.Model):
    patientID = models.IntegerField()
    hystoryNumber = models.IntegerField()

    class Meta:
        db_table = 'stat_cards_table'
        app_label = 'mgerm'

    @classmethod
    def get_visit_counts(self):
        visit_counts = (
            StatCard.objects
            .values('patientID')
            .annotate(count=Count('hystoryNumber', distinct=True))  # Считаем уникальные обращения
        )
        return visit_counts

class AnaVitae(models.Model):
    genetic_diseases = models.TextField(null=True, blank=True, db_column='genetic_deseases')
    family_hyst = models.TextField(null=True, blank=True)
    working = models.TextField(null=True, blank=True)

    class Meta:
        db_table = '3_ana_vitae'
        app_label = 'vmh'

class DopolnitelnieStatisticheskieDannye(models.Model):
    obrazovanie_dlitelnost = models.IntegerField(null=True, blank=True, db_column='Obrazovanie_(dlitelnost)')
    kolichestvo_detey = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'dopolnitelnie_statisticheskie_dannie'
        app_label = 'vmh'

class VmhDbManager:
    def get_genetic_diseases(self):
        result = AnaVitae.objects.filter(genetic_diseases__isnull=False).values_list('genetic_diseases', flat=True)
        sentences = list(result)

        predictions = predict_genetic_diseases(sentences)

        return predictions


    def get_education_stats(self):
        # Использование ORM для получения данных
        result = DopolnitelnieStatisticheskieDannye.objects.filter(
            obrazovanie_dlitelnost__isnull=False
        ).values('obrazovanie_dlitelnost').annotate(
            count=Count('obrazovanie_dlitelnost')
        ).order_by('obrazovanie_dlitelnost')

        education_duration = {
            "Меньше 1 года": result[0]['count'],
            "1 год": result[1]['count'],
            "2 года": result[2]['count'],
            "3 года": result[3]['count'],
            "4 года": result[4]['count'],
            "5 лет": result[5]['count'],
        }

        return education_duration

    def get_family_history(self):
        # Использование ORM для получения данных
        result = AnaVitae.objects.filter(family_hyst__isnull=False).values_list('family_hyst', flat=True)
        data = list(result)
        predictions = predict_family_relations(data)

        return predictions

    def get_kids_count(self):
        # Использование ORM для получения данных
        result = DopolnitelnieStatisticheskieDannye.objects.filter(
            kolichestvo_detey__isnull=False,
            kolichestvo_detey__gt=0
        ).values('kolichestvo_detey').annotate(count=models.Count('kolichestvo_detey')).order_by('kolichestvo_detey')

        kids_count = {
            "1 ребенок": result[0]['count'],
            "2 ребенка": result[1]['count'],
            "3 ребенка": result[2]['count'],
            "4 ребенка": result[3]['count'],
            "5 детей": result[4]['count'],
        }

        return kids_count

    def get_work_relations(self):
        # Использование ORM для получения данных
        result = AnaVitae.objects.filter(working__isnull=False).values_list('working', flat=True)
        data = list(result)

        predictions = predict_work_relations(data)

        return predictions