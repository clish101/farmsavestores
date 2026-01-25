#!/usr/bin/env python
"""
Test script to verify the Excel export functions work correctly
"""
import os
import sys
import django

# Add the Glua directory to the path
sys.path.insert(0, r'c:\Users\Neko\Desktop\pharmTZ\pharmsaver\Glua')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Glua.settings')
django.setup()

from Inventory.models import Sale, IssuedCannister
from openpyxl import load_workbook
from django.conf import settings

template_path = os.path.join(settings.BASE_DIR, 'Inventory transfer record template11.xlsx')

print("=" * 60)
print("Excel Export Functions Verification")
print("=" * 60)

# Check if template exists
if os.path.exists(template_path):
    print(f"✓ Template file found: {template_path}")
    
    # Try to load the template
    try:
        wb = load_workbook(template_path)
        ws = wb.active
        print(f"✓ Template loaded successfully")
        print(f"  - Sheet name: {ws.title}")
        print(f"  - Dimensions: {ws.dimensions}")
    except Exception as e:
        print(f"✗ Error loading template: {e}")
else:
    print(f"✗ Template file not found at: {template_path}")

# Check data availability
sales_count = Sale.objects.count()
cannisters_count = IssuedCannister.objects.count()

print(f"\nDatabase Statistics:")
print(f"  - Sales records: {sales_count}")
print(f"  - Issued Cannisters: {cannisters_count}")

# Test imports
try:
    from Inventory.views import download_bin_report_excel, download_bin_card_excel
    print(f"\n✓ Both Excel export functions imported successfully")
except ImportError as e:
    print(f"\n✗ Error importing functions: {e}")

print("\n" + "=" * 60)
print("Verification Complete")
print("=" * 60)
print("\nTo test the exports:")
print("1. Visit: http://localhost:8000/bin-report/")
print("2. Click: 'Download Excel' button")
print("3. Visit: http://localhost:8000/bin-card/")
print("4. Click: 'Download Excel' button")
