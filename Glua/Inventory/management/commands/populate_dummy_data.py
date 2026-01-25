from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from Inventory.models import (
    Measurement, Drug, Sale, Stocked, LockedProduct, 
    MarketingItem, IssuedItem, PickingList, Cannister, IssuedCannister, Client
)


class Command(BaseCommand):
    help = 'Populate database with dummy data for testing'

    def handle(self, *args, **kwargs):
        # Clear existing data (in correct order due to foreign key constraints)
        self.stdout.write('Clearing existing data...')
        Sale.objects.all().delete()
        LockedProduct.objects.all().delete()
        Stocked.objects.all().delete()
        IssuedCannister.objects.all().delete()
        IssuedItem.objects.all().delete()
        PickingList.objects.all().delete()
        MarketingItem.objects.all().delete()
        Cannister.objects.all().delete()
        Drug.objects.all().delete()
        Measurement.objects.all().delete()
        Client.objects.all().delete()

        # Get or create admin user
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@pharmsaver.com', 'is_staff': True, 'is_superuser': True}
        )

        # Create Measurements
        self.stdout.write('Creating Measurements...')
        measurements_data = ['Tablets', 'Capsules', 'Liquid (ml)', 'Syrup (ml)', 'Injection (ml)']
        measurements = []
        for i, name in enumerate(measurements_data):
            measurement, _ = Measurement.objects.get_or_create(
                name=name,
                defaults={'expiry_date': timezone.now().date() + timedelta(days=365)}
            )
            measurements.append(measurement)

        # Create Clients
        self.stdout.write('Creating Clients...')
        clients_data = [f'Client {i}' for i in range(1, 26)]  # 25 clients
        clients = []
        for name in clients_data:
            client, _ = Client.objects.get_or_create(
                name=name,
                defaults={
                    'email': f'{name.lower().replace(" ", "_")}@example.com',
                    'phone': '+254712345678'
                }
            )
            clients.append(client)

        # Create Drugs - significantly more drugs for ~500 data points
        self.stdout.write('Creating Drugs...')
        drugs_data = [
            {'name': f'Drug {i} - {["Paracetamol", "Amoxicillin", "Aspirin", "Ibuprofen", "Metformin", "Ciprofloxacin", "Atorvastatin", "Lisinopril", "Omeprazole", "Loratadine"][i % 10]}', 
             'batch_no': f'BATCH{i:04d}', 'stock': 100 + (i * 2), 'dose_pack': 250 + (i % 500), 'reorder_level': 50 + (i % 100)}
            for i in range(1, 51)  # 50 different drugs
        ]
        
        drugs = []
        for drug_data in drugs_data:
            drug, _ = Drug.objects.get_or_create(
                name=drug_data['name'],
                batch_no=drug_data['batch_no'],
                defaults={
                    'stock': drug_data['stock'],
                    'dose_pack': drug_data['dose_pack'],
                    'expiry_date': timezone.now().date() + timedelta(days=180 + (hash(drug_data['name']) % 365)),
                    'reorder_level': drug_data['reorder_level'],
                    'measurement_units': measurements[0]
                }
            )
            drugs.append(drug)

        # Create Sales - scale up to ~150 sales
        self.stdout.write('Creating Sales...')
        for i, drug in enumerate(drugs):
            for j in range(3):  # 3 sales per drug = 150 sales
                client = clients[j % len(clients)]
                Sale.objects.get_or_create(
                    seller=admin_user,
                    drug_sold=drug.name,
                    client=client,
                    batch_no=drug.batch_no,
                    quantity=10 + (j * 5),
                    remaining_quantity=5 + (j * 2),
                    defaults={
                        'date_sold': timezone.now() - timedelta(days=j)
                    }
                )

        # Create Stocked Items - scale up to ~150 stocked items
        self.stdout.write('Creating Stocked Items...')
        for i, drug in enumerate(drugs):
            for j in range(3):  # 3 stocked per drug = 150 stocked
                Stocked.objects.get_or_create(
                    drug_name=drug,
                    staff=admin_user,
                    number_added=50 + (j * 10),
                    supplier=f'Supplier {j+1}',
                    defaults={
                        'date_added': timezone.now() - timedelta(days=j),
                        'total': drug.stock
                    }
                )

        # Create Locked Products - scale up to ~100 locked products
        self.stdout.write('Creating Locked Products...')
        for i, drug in enumerate(drugs):
            for j in range(2):  # 2 locked per drug = 100 locked
                if j < 2:
                    client = clients[j % len(clients)]
                    LockedProduct.objects.get_or_create(
                        drug=drug,
                        locked_by=admin_user,
                        quantity=20 + (j * 5),
                        client=client,
                        defaults={
                            'date_locked': timezone.now() - timedelta(days=j)
                        }
                    )

        # Create Marketing Items
        self.stdout.write('Creating Marketing Items...')
        marketing_items_data = [
            {'name': f'Marketing Item {i}', 'stock': 100 + (i * 50)}
            for i in range(1, 11)  # 10 marketing items
        ]
        
        for item_data in marketing_items_data:
            MarketingItem.objects.get_or_create(
                name=item_data['name'],
                defaults={'stock': item_data['stock']}
            )

        # Create Issued Items - scale up to ~30 issued items
        self.stdout.write('Creating Issued Items...')
        for i in range(30):
            IssuedItem.objects.get_or_create(
                item=f'Issued Item {i+1}',
                stock=100 + (i * 20),
                issued_to=f'Department {(i % 5)+1}',
                quantity_issued=25 + (i * 5),
                issued_by=admin_user,
                defaults={
                    'date_issued': timezone.now() - timedelta(days=i % 30)
                }
            )

        # Create Picking Lists - scale up to ~50 picking lists
        self.stdout.write('Creating Picking Lists...')
        for i in range(50):
            client = clients[i % len(clients)]
            PickingList.objects.get_or_create(
                date=timezone.now().date() - timedelta(days=i % 30),
                client=client,
                product=drugs[i % len(drugs)].name,
                batch_no=drugs[i % len(drugs)].batch_no,
                quantity=30 + (i * 10),
            )

        # Create Cannisters
        self.stdout.write('Creating Cannisters...')
        cannisters_data = [
            {'name': f'Liquid {chr(65 + i)}', 'batch_no': f'CAN{i:03d}', 'stock': 50 + (i * 5), 'litres': f'{20 + i}L'}
            for i in range(15)  # 15 different cannisters
        ]
        
        cannisters = []
        for cannister_data in cannisters_data:
            cannister, _ = Cannister.objects.get_or_create(
                name=cannister_data['name'],
                batch_no=cannister_data['batch_no'],
                defaults={
                    'stock': cannister_data['stock'],
                    'litres': cannister_data['litres']
                }
            )
            cannisters.append(cannister)

        # Create Issued Cannisters - scale up to ~75 issued cannisters
        self.stdout.write('Creating Issued Cannisters...')
        for i, cannister in enumerate(cannisters):
            for j in range(5):  # 5 issued per cannister = 75 issued
                client = clients[j % len(clients)]
                IssuedCannister.objects.get_or_create(
                    name=cannister.name,
                    batch_no=cannister.batch_no,
                    staff_on_duty=admin_user,
                    client=client,
                    quantity=20 + (j * 5),
                    balance=10 + (j * 2),
                    action=j % 2 == 0,
                    defaults={
                        'date_issued': timezone.now() - timedelta(days=j),
                        'date_returned': timezone.now() - timedelta(days=j-1) if j > 0 else timezone.now()
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data!'))
