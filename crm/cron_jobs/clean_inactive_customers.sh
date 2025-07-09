#!/bin/bash

# Se placer dans la racine du projet (supposée être 2 niveaux au-dessus du script)
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || { echo "Failed to cd"; exit 1; }

deleted_count=$(python3 manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer, Order

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(id__in=Order.objects.filter(created_at__gte=one_year_ago).values_list('customer_id', flat=True))
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

if [ -n "$deleted_count" ]; then
    echo "$(date): Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
else
    echo "$(date): No customers deleted or error occurred" >> /tmp/customer_cleanup_log.txt
fi
