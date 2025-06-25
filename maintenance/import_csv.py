import csv
import os
from datetime import datetime
from django.conf import settings
from .models import MaintenanceLog

def run_import():
    csv_path = os.path.join(settings.BASE_DIR, 'data', 'maintenance_log.csv')

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = {k.strip().lower(): v for k, v in row.items()}

            MaintenanceLog.objects.create(
                date=datetime.strptime(row['date'], "%Y-%m-%d").date(),
                vehicle=row['vehicle'],
                service=row['service'],
                cost=row['cost'],
                mileage=row['mileage']
            )
    print("CSV data imported successfully.")
