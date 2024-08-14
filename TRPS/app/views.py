from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
from .mgerm_manager import MgermManager
import io
import urllib, base64
from matplotlib.patches import ConnectionPatch
from .vmh_manager import VmhDbManager
# Create your views here.

def index(request):
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
    # Сохранение графика в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

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
    return render(request, "index.html", {'data': uri, 'data2': uri2})