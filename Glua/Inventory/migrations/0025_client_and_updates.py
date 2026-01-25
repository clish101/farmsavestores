# Generated migration for adding Client model and updating foreign keys

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


def create_clients_from_sales(apps, schema_editor):
    """Create Client records from existing Sale data"""
    Sale = apps.get_model('Inventory', 'Sale')
    Client = apps.get_model('Inventory', 'Client')
    
    # Get all unique client names from Sales
    client_names = Sale.objects.filter(client__isnull=False).values_list('client', flat=True).distinct()
    
    # Create Client records for each unique name
    for name in client_names:
        if name:  # Only create if name is not empty
            Client.objects.get_or_create(name=name)
    
    # Get all unique client names from LockedProducts
    LockedProduct = apps.get_model('Inventory', 'LockedProduct')
    client_names_locked = LockedProduct.objects.filter(client__isnull=False).values_list('client', flat=True).distinct()
    
    for name in client_names_locked:
        if name:
            Client.objects.get_or_create(name=name)


def populate_fk_from_text(apps, schema_editor):
    """Update ForeignKey fields by matching text with Client names"""
    Sale = apps.get_model('Inventory', 'Sale')
    Client = apps.get_model('Inventory', 'Client')
    
    for sale in Sale.objects.all():
        if sale.client_id is None and sale.client:  # If client_id is still None (storing the string)
            try:
                client = Client.objects.get(name=str(sale.client))
                sale.client_id = client.id
                sale.save()
            except Client.DoesNotExist:
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0024_remove_pickinglist_in_stock'),
    ]

    operations = [
        # Create the Client model
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['name'],
            },
        ),
        # Step 1: Create clients from existing data
        migrations.RunPython(create_clients_from_sales),
        # Step 2: Remove old client CharField from Sale temporarily
        migrations.RemoveField(
            model_name='sale',
            name='client',
        ),
        # Step 3: Add new client ForeignKey to Sale
        migrations.AddField(
            model_name='sale',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Inventory.Client'),
        ),
        # Step 4: Remove old client CharField from LockedProduct temporarily
        migrations.RemoveField(
            model_name='lockedproduct',
            name='client',
        ),
        # Step 5: Add new client ForeignKey to LockedProduct
        migrations.AddField(
            model_name='lockedproduct',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Inventory.Client'),
        ),
        # Step 6: Remove old client CharField from PickingList temporarily
        migrations.RemoveField(
            model_name='pickinglist',
            name='client',
        ),
        # Step 7: Add new client ForeignKey to PickingList (nullable initially)
        migrations.AddField(
            model_name='pickinglist',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Inventory.Client'),
        ),
        # Step 8: Remove old client CharField from IssuedCannister temporarily
        migrations.RemoveField(
            model_name='issuedcannister',
            name='client',
        ),
        # Step 9: Add new client ForeignKey to IssuedCannister
        migrations.AddField(
            model_name='issuedcannister',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Inventory.Client'),
        ),
    ]

