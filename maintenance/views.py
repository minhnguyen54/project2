from django.shortcuts import render
from .models import MaintenanceLog
from .charts import (
    get_service_counts_by_vehicle,
    get_service_frequency_chart,
    get_cost_by_service_chart,
    get_cost_over_time_chart
)

def dashboard(request):
    logs = MaintenanceLog.objects.all()

    # Filters
    vehicle = request.GET.get('vehicle')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    service_type = request.GET.get('service_type')

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

    context = {
        'logs': logs,
        'vehicles': all_vehicles,
        'service_types': all_services,
        'chart_services_per_vehicle': get_service_counts_by_vehicle(),
        'chart_service_frequency': get_service_frequency_chart(),
        'chart_cost_by_service': get_cost_by_service_chart(),
        'chart_cost_over_time': get_cost_over_time_chart(),
    }

    return render(request, 'maintenance/dashboard.html', context)

