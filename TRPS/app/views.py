from collections import Counter
from textwrap import wrap
from django.shortcuts import render
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from .mgerm_manager import MgermManager
import io
import urllib, base64
from datetime import datetime
from matplotlib.patches import ConnectionPatch
import pandas as pd
from .models import VmhDbManager, StatCard, DepartmentIncome, DepartmentOutcome
from django.db.models.functions import Cast
from django.db.models import DateTimeField
# Create your views here.

def index(request):
    return render(request, "index.html")


def sociodemographic(request):

    vmh_db_manager = VmhDbManager()
    education_stats = vmh_db_manager.get_education_stats()
    family_stats = vmh_db_manager.get_family_history()
    kids_stats = vmh_db_manager.get_kids_count()
    work_stats = vmh_db_manager.get_work_relations()

    fig = plt.figure(figsize=(12, 10), layout="tight")

    spec = fig.add_gridspec(2, 2)

    ax_up_left = fig.add_subplot(spec[0, 0])
    ax_up_right = fig.add_subplot(spec[0, 1])
    ax_down_left = fig.add_subplot(spec[1, 0])
    ax_down_right = fig.add_subplot(spec[1, 1])

    ax_up_left.pie(family_stats.values(), autopct='%1.1f%%', startangle=-180)
    ax_up_left.legend(family_stats.keys(), loc="upper right", fontsize=8)
    ax_up_left.set_title("Семейное положение", fontsize=14, fontweight="bold", pad=10)

    ax_up_right.pie(kids_stats.values(), autopct='%1.1f%%', startangle=-180)
    ax_up_right.legend(kids_stats.keys(), loc="upper right", fontsize=8)
    ax_up_right.set_title("Количество детей в семье", fontsize=14, fontweight="bold", pad=10)

    ax_down_left.pie(education_stats.values(), autopct='%1.1f%%', startangle=-180)
    ax_down_left.legend(education_stats.keys(), loc="upper right", fontsize=8)
    ax_down_left.set_title("Продолжительность образования", fontsize=14, fontweight="bold", pad=10)

    ax_down_right.pie(work_stats.values(), autopct='%1.1f%%', startangle=-180)
    ax_down_right.legend(work_stats.keys(), loc="upper right", fontsize=8)
    ax_down_right.set_title("Трудовой анамнез", fontsize=14, fontweight="bold", pad=10)

    plt.subplots_adjust(top=0.92, hspace=0.5)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    del vmh_db_manager


    mgerm_manager = MgermManager()
    age_gender_data = mgerm_manager.get_age_gender_distribution()
    age_gender_weight_count = {
        "Женщины": np.array(list(age_gender_data[0].values())),
        "Мужчины": np.array(list(age_gender_data[1].values())),
    }

    fig, ax = plt.subplots(nrows=1, figsize=(10, 6))

    bottom = np.zeros(len(age_gender_data[0].keys()))
    for boolean, weight_count in age_gender_weight_count.items():
        ax.bar(np.arange(len(age_gender_data[0].keys())), weight_count, 0.5, label=boolean, bottom=bottom,
            edgecolor="black", linewidth=0.5)
        bottom += weight_count

    ax.grid(axis='both', which='major', linewidth=0.5, color='grey', alpha=0.5)
    ax.set_title("Распределение пациентов по возрасту и полу", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Возраст пациентов, лет", labelpad=10)
    ax.set_ylabel("Количество пациентов", labelpad=10)
    ax.legend(loc="upper right")
    ax.set_xticks(range(len(age_gender_data[0].keys())))
    ax.set_xticklabels(age_gender_data[0].keys(), rotation=15)

    plt.subplots_adjust(top=0.92, bottom=0.15)
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    string1 = base64.b64encode(buf1.read())
    uri1 = urllib.parse.quote(string1)

    del mgerm_manager


    vmh_db_manager = VmhDbManager()
    genetic_diseases = vmh_db_manager.get_genetic_diseases()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, 8))

    pie_chart_params = {
        "Есть наследственная отягощенность": 0,
        "Нет наследственной отягощенности": genetic_diseases["Нет наследственной отягощенности"],
        "Отрицает психические заболевания родственников": genetic_diseases[
            "Отрицает психические заболевания родственников"]
    }
    bar_chart_params = dict()
    for key, val in genetic_diseases.items():
        if key not in pie_chart_params.keys():
            pie_chart_params["Есть наследственная отягощенность"] += val
            bar_chart_params[key] = val

    bottom = 1
    width = .2
    angle = -180 * pie_chart_params["Есть наследственная отягощенность"] / sum(pie_chart_params.values())

    for j, (height, label) in enumerate(reversed([*zip(bar_chart_params.values(), bar_chart_params.keys())])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom, color="C0", label=label,
                    alpha=0.1 + 0.25 * j)
        ax2.bar_label(bc, labels=[f"{height}"], label_type="center")

    ax2.set_title("Причины")
    ax2.legend(loc="lower right")
    ax2.axis("off")
    ax2.set_xlim(-2.5 * width, 2.5 * width)

    wedges, *_ = ax1.pie(pie_chart_params.values(), autopct="%1.1f%%", startangle=angle,
                        labels=pie_chart_params.keys(), explode=[0.1, 0.0, 0.0])
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r
    bar_height = sum(bar_chart_params.values())

    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(3)
    ax2.add_artist(con)

    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, -bar_height), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(3)

    fig.suptitle("Наследственная отягощенность у пациентов", fontsize=14, fontweight="bold")
    plt.subplots_adjust(left=0.05, right=0.95, top=0.86, wspace=0)
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    string2 = base64.b64encode(buf2.read())
    uri2 = urllib.parse.quote(string2)
    return render(request,  "sociodemographic.html", {'data': uri, 'data1': uri1, 'data2': uri2})

def general(request):
    mgerm_manager = MgermManager()

    patients_count = mgerm_manager.get_patients_count()
    cards_count = mgerm_manager.get_cards_count()
    incorrect_cards_count = mgerm_manager.get_incorrect_cards_count()
    observation_time = mgerm_manager.get_observation_time()

    common_stats_values = [patients_count, cards_count, incorrect_cards_count, cards_count - incorrect_cards_count]
    common_stats_labels = ["Число пациентов", "Число амбулаторных карт", "Число неверно заполненных карт",
                        "Число верно заполненных карт"]

    fig, (ax_top, ax_bottom) = plt.subplots(nrows=2, figsize=(10, 8))

    ax_bottom.bar(observation_time.keys(), observation_time.values(), color="green", edgecolor="black", linewidth=0.5)
    ax_bottom.grid(axis='both', which='major', linewidth=0.5, color='grey', alpha=0.5)
    ax_bottom.set_xlabel("Время наблюдения, лет")
    ax_bottom.set_ylabel("Количество пациентов", labelpad=10)
    ax_bottom.set_yscale("log")
    ax_bottom.set_title("Длительность наблюдения в стационаре", fontsize=14, fontweight="bold", pad=20)

    ax_top.bar(common_stats_labels, common_stats_values, color="indianred", edgecolor="black", linewidth=0.5)
    ax_top.set_xticks(range(len(common_stats_labels)))
    ax_top.set_xticklabels(['\n'.join(wrap(label, 20)) for label in common_stats_labels])
    ax_top.grid(axis='both', which='major', linewidth=0.5, color='grey', alpha=0.5)
    ax_top.set_ylabel("Количество пациентов", labelpad=10)
    ax_top.set_yscale("linear")
    ax_top.set_title("Общая статистика", fontsize=14, fontweight="bold", pad=20)
    plt.subplots_adjust(top=0.92, hspace=0.5)
    del mgerm_manager

    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png')
    buf3.seek(0)
    string3 = base64.b64encode(buf3.read())
    uri3 = urllib.parse.quote(string3)


    visit_counts = StatCard.get_visit_counts()
    counts = [entry['count'] for entry in visit_counts]
    patient_count_by_count = Counter(counts)
    plt.figure(figsize=(8, 6))
    bars = plt.bar(patient_count_by_count.keys(), patient_count_by_count.values())
    plt.xlabel('Количество обращений')
    plt.ylabel('Количество пациентов')
    plt.title('Количество пациентов по количеству обращений')
    plt.xlim(0, 15)
    plt.grid(True, zorder=0)
    # Добавление значений над колонками
    for i, bar in enumerate(bars):
        if i < 14:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    buf4 = io.BytesIO()
    plt.savefig(buf4, format='png')
    buf4.seek(0)
    string4 = base64.b64encode(buf4.read())
    uri4 = urllib.parse.quote(string4)

    return render(request,  "general.html", {'data3': uri3, 'data4': uri4})


def stationary_outpatient(request):
    F = False
    # График для дней (1-30 дней)
    plt.figure(figsize=(16, 8))
    days_data = StatCard.get_days_distribution()
    durations = [int(d['duration_days']) for d in days_data]
    counts = [d['count'] for d in days_data]

    bars = plt.bar(durations, counts)
    plt.title('Распределение амбулаторных пациентов по дням')
    plt.xlabel('Количество дней')
    plt.ylabel('Количество пациентов')
    plt.xlim(0, 30)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval,
                int(yval), ha='center', va='bottom')

    # Сохранение первого графика
    buf5 = io.BytesIO()
    plt.savefig(buf5, format='png')
    buf5.seek(0)
    string5 = base64.b64encode(buf5.read())
    uri5 = urllib.parse.quote(string5)
    plt.close()

    # График для месяцев (30-365 дней)
    plt.figure(figsize=(16, 8))
    months_data = StatCard.get_months_distribution()
    durations = [int(d['duration_months']) for d in months_data]
    counts = [d['count'] for d in months_data]

    bars = plt.bar(durations, counts)
    plt.title('Распределение амбулаторных пациентов по месяцам')
    plt.xlabel('Месяц')
    plt.ylabel('Количество пациентов')
    plt.xlim(0, 11)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval,
                int(yval), ha='center', va='bottom')

    # Сохранение второго графика
    buf6 = io.BytesIO()
    plt.savefig(buf6, format='png')
    buf6.seek(0)
    string6 = base64.b64encode(buf6.read())
    uri6 = urllib.parse.quote(string6)
    plt.close()

    if request.method == 'POST':
        F = True
        start_date = datetime.strptime(request.POST.get('start_date'), '%d.%m.%Y')
        end_date = datetime.strptime(request.POST.get('end_date'), '%d.%m.%Y')

        # Получаем данные с преобразованием date в datetime
        income_data = DepartmentIncome.objects.filter(
            department__in=["1 дн. ст.", "2 дн. ст.", "3 дн. ст."],
            date__range=[start_date, end_date]
        ).annotate(
            datetime_field=Cast('date', DateTimeField())
        ).values('hystoryNumber', 'datetime_field', 'patientID')

        outcome_data = DepartmentOutcome.objects.filter(
            department__in=["1 дн. ст.", "2 дн. ст.", "3 дн. ст."]
        ).annotate(
            datetime_field=Cast('out_date', DateTimeField())
        ).values('hystoryNumber', 'datetime_field')

        # Преобразуем в DataFrame
        income_df = pd.DataFrame(list(income_data))
        income_df = income_df.rename(columns={'datetime_field': 'date'})

        outcome_df = pd.DataFrame(list(outcome_data))
        outcome_df = outcome_df.rename(columns={'datetime_field': 'out_date'})

        # Группировка по месяцам
        admissions_per_month = income_df.groupby(pd.to_datetime(income_df['date']).dt.to_period('M')).size()

        # Подсчет длительности пребывания
        merged_df = pd.merge(income_df[['hystoryNumber', 'date']],
                           outcome_df[['hystoryNumber', 'out_date']],
                           on='hystoryNumber')
        merged_df['duration'] = (merged_df['out_date'] - merged_df['date']).dt.days + 1

        # Построение графиков
        plt.figure(figsize=(15, 10))

        # График поступлений по месяцам
        plt.subplot(2, 1, 1)
        admissions_per_month.plot(kind='bar', color='skyblue')
        plt.title('Количество поступлений пациентов по месяцам')
        plt.xlabel('Месяц')
        plt.ylabel('Количество поступлений')
        plt.grid(True, zorder=0)
        # График длительности пребывания
        plt.subplot(2, 1, 2)
        bars = plt.hist(merged_df['duration'],
                       bins=range(0, int(merged_df['duration'].max()) + 1),
                       color='salmon', edgecolor='black', align='left', width=0.8)
        plt.title('Длительность пребывания пациентов')
        plt.xlabel('Длительность (дни)')
        plt.ylabel('Количество пациентов')

        # Добавление значений над столбцами
        for bar in bars[2]:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height,
                    int(height), ha='center', va='bottom')

        # Настройка осей
        ax = plt.gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xticks(range(0, int(merged_df['duration'].max()) + 1, 1))
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)

        plt.tight_layout()
        # Сохранение графика в буфер
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        plt.close()
    if F:
        return render(request, "stationary_outpatient.html", {'data5': uri5, 'data6': uri6, 'data7': uri})
    else:
        return render(request, "stationary_outpatient.html", {'data5': uri5, 'data6': uri6})
