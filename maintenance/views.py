from django.shortcuts import render, redirect
from .models import MaintenanceLog
from .charts import (
    get_service_counts_by_vehicle,
    get_service_frequency_chart,
    get_cost_by_service_chart,
    get_cost_over_time_chart
)
from .forms import CSVUploadForm
import csv, io
from django.contrib import messages
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def dashboard(request):
    logs = MaintenanceLog.objects.all()

    # CSV upload logic
    if request.method == 'POST' and 'file' in request.FILES:
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded_file))

            count = 0
            for row in reader:
                MaintenanceLog.objects.create(
                    date=row['Date'],
                    vehicle=row['Vehicle'],
                    mileage=row['Mileage'],
                    service=row['Service'],
                    cost=row['Cost'],
                    notes=row.get('Notes', '')
                )
                count += 1
            messages.success(request, f"Imported {count} records successfully.")
            return redirect('dashboard')
    else:
        form = CSVUploadForm()

    # Filters
    vehicle = request.GET.get('vehicle')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    service_type = request.GET.get('service_type')
    user_question = request.GET.get('ask_ai')

    if vehicle:
        logs = logs.filter(vehicle__icontains=vehicle)
    if start_date:
        logs = logs.filter(date__gte=start_date)
    if end_date:
        logs = logs.filter(date__lte=end_date)
    if service_type:
        logs = logs.filter(service__icontains=service_type)

    all_vehicles = MaintenanceLog.objects.values_list('vehicle', flat=True).distinct()
    all_services = MaintenanceLog.objects.values_list('service', flat=True).distinct()

    ai_response = None
    if user_question:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful car maintenance assistant."},
                    {"role": "user", "content": user_question}
                ]
            )
            ai_response = response.choices[0].message.content.strip()
        except Exception as e:
            ai_response = f"Error with AI response: {e}"

    context = {
        'logs': logs,
        'vehicles': all_vehicles,
        'service_types': all_services,
        'chart_services_per_vehicle': get_service_counts_by_vehicle(),
        'chart_service_frequency': get_service_frequency_chart(),
        'chart_cost_by_service': get_cost_by_service_chart(),
        'chart_cost_over_time': get_cost_over_time_chart(),
        'form': form,
        'ai_response': ai_response,
    }

    return render(request, 'maintenance/dashboard.html', context)
