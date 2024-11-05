from django.db import models
from django.db.models import Count, F, ExpressionWrapper, fields
from datetime import timedelta
from .ml import *

class StatCard(models.Model):
    patientID = models.IntegerField()
    hystoryNumber = models.IntegerField()
    in_date = models.DateTimeField(null=True)
    out_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'stat_cards_table'
        app_label = 'mgerm'

    @classmethod
    def get_duration_distribution(cls):
        """Получение распределения длительности лечения"""
        # Вычисляем duration как разницу между out_date и in_date в днях
        duration_expression = ExpressionWrapper(
            F('out_date') - F('in_date'),
            output_field=fields.DurationField()
        )
        # Аннотация с вычислением длительности
        annotated = cls.objects.annotate(
            duration=duration_expression
        ).exclude(duration__isnull=True)

        # Преобразуем длительность в дни
        annotated = annotated.annotate(
            duration_days=ExpressionWrapper(
                F('duration') / timedelta(days=1),
                output_field=fields.FloatField()
            )
        )
        return annotated

    @classmethod
    def get_days_distribution(cls):
        """Получение распределения пациентов по дням (1-30 дней)"""
        annotated = cls.get_duration_distribution()
        # Фильтруем по длительности от 0 до 30 дней
        filtered = annotated.filter(
            duration_days__gte=0,
            duration_days__lte=30
        )
        # Группируем по длительности и считаем количество пациентов
        result = filtered.values('duration_days').annotate(
            count=Count('patientID')
        ).order_by('duration_days')
        return result

    @classmethod
    def get_months_distribution(cls):
        """Получение распределения пациентов по месяцам (30-365 дней)"""
        annotated = cls.get_duration_distribution()
        filtered = annotated.filter(
            duration_days__gt=30,
            duration_days__lt=365
        )
        # Преобразуем дни в месяцы
        filtered = filtered.annotate(
            duration_months=ExpressionWrapper(
                F('duration_days') / 30.44,  # Среднее количество дней в месяце
                output_field=fields.FloatField()
            )
        )
        result = filtered.values('duration_months').annotate(
            count=Count('patientID')
        ).order_by('duration_months')
        return result

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
        result = AnaVitae.objects.filter(family_hyst__isnull=False).values_list('family_hyst', flat=True)
        data = list(result)
        predictions = predict_family_relations(data)

        return predictions

    def get_kids_count(self):
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
        result = AnaVitae.objects.filter(working__isnull=False).values_list('working', flat=True)
        data = list(result)

        predictions = predict_work_relations(data)

        return predictions