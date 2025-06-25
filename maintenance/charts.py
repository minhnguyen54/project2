import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns
from django.db.models import Count, Sum
from .models import MaintenanceLog

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def get_service_frequency_chart():
    data = MaintenanceLog.objects.values('service').annotate(count=Count('id'))
    labels = [entry['service'] for entry in data]
    counts = [entry['count'] for entry in data]

    fig, ax = plt.subplots()
    ax.bar(labels, counts, color='skyblue')
    ax.set_title('Service Frequency')
    ax.set_ylabel('Count')
    ax.set_xlabel('Service')
    plt.xticks(rotation=30, ha='right')
    fig.tight_layout()
    return fig_to_base64(fig)

def get_cost_by_service_chart():
    data = MaintenanceLog.objects.values('service').annotate(total_cost=Sum('cost'))
    labels = [entry['service'] for entry in data]
    costs = [entry['total_cost'] for entry in data]

    fig, ax = plt.subplots()
    sns.barplot(x=labels, y=costs, ax=ax, palette='Blues_d')
    ax.set_title('Total Cost by Service')
    ax.set_ylabel('Total Cost ($)')
    ax.set_xlabel('Service')
    plt.xticks(rotation=30, ha='right')
    fig.tight_layout()
    return fig_to_base64(fig)

def get_cost_over_time_chart():
    data = MaintenanceLog.objects.values('date').annotate(total_cost=Sum('cost')).order_by('date')
    dates = [entry['date'] for entry in data]
    costs = [entry['total_cost'] for entry in data]

    fig, ax = plt.subplots()
    ax.plot(dates, costs, marker='o', linestyle='-', color='green')
    ax.set_title('Cost Over Time')
    ax.set_ylabel('Cost ($)')
    ax.set_xlabel('Date')
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    return fig_to_base64(fig)

def get_service_counts_by_vehicle():
    data = MaintenanceLog.objects.values('vehicle').annotate(count=Count('id'))
    labels = [entry['vehicle'] for entry in data]
    counts = [entry['count'] for entry in data]

    fig, ax = plt.subplots()
    ax.bar(labels, counts, color='orange')
    ax.set_title('Services Per Vehicle')
    ax.set_ylabel('Count')
    ax.set_xlabel('Vehicle')
    plt.xticks(rotation=30, ha='right')
    fig.tight_layout()
    return fig_to_base64(fig)
