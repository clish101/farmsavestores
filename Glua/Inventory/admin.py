from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .models import Drug, Sale, Stocked, Measurement, LockedProduct, MarketingItem, IssuedItem, PickingList, Cannister, IssuedCannister, Client


class LockedProductAdmin(admin.ModelAdmin):
    # Optionally, add fields to the admin panel
    list_display = ('drug', 'locked_by', 'date_locked', 'quantity', 'client')

    def save_model(self, request, obj, form, change):
        # Check if the object is being updated (change == True)
        if change:
            original = LockedProduct.objects.get(pk=obj.pk)
            # If the product is locked, prevent any changes to it
            if original.date_locked and obj.drug != original.drug:
                raise PermissionDenied("Cannot update locked drugs.")

        # Call the parent method to save the object
        super().save_model(request, obj, form, change)


admin.site.register(Drug)  # If you want to use the default admin for Drug
admin.site.register(Sale)  # If you want to use the default admin for Sale
admin.site.register(Client)  # Register Client model
admin.site.register(MarketingItem)  # If you want to use the default admin for marketItem
admin.site.register(IssuedItem)  # If you want to use the default admin for IssuedItem
admin.site.register(LockedProduct, LockedProductAdmin)
admin.site.register(PickingList)
admin.site.register(Cannister)
admin.site.register(IssuedCannister)