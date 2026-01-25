from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now


class Client(models.Model):
    """Model definition for Client."""
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Client."""
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['name']

    def __str__(self):
        """Unicode representation of Client."""
        return self.name



# class Batch(models.Model):
#     """Model definition for Batch."""
#     name = models.CharField(max_length=200)
#     expiry_date = models.DateField(blank=False)

#     class Meta:
#         """Meta definition for Batch."""
#         verbose_name = 'Batch Number'
#         verbose_name_plural = 'Batch Numbers'

#     def __str__(self):
#         """Unicode representation of Batch."""
#         return f"{self.name} (Expires: {self.expiry_date})"


class Measurement(models.Model):
    """Model definition for Measurement."""
    name = models.CharField(max_length=200)
    expiry_date = models.DateField(blank = False)

    class Meta:
        """Meta definition for Measurement."""
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements'

    def __str__(self):
        """Unicode representation of Measurement."""
        return self.name

# class Vaccine_name(models.Model):
#     name = models.CharField(max_length=200)


class Drug(models.Model):
    """Model definition for Drug."""
    # name = models.ForeignKey(Vaccine_name, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=200)
    batch_no = models.CharField(max_length=200)
    # buying_price = models.FloatField()
    # minimum_price = models.FloatField(null=True, blank=True)
    # ref_code = models.CharField(unique=True, max_length=200, null=True, blank=True)
    # selling_price = models.FloatField(null=True)
    # maximum_price = models.FloatField()
    stock = models.IntegerField()
    dose_pack = models.FloatField(null=False)
    expiry_date = models.DateField(blank=True, null=True)
    reorder_level = models.FloatField(null=False)
    measurement_units = models.ForeignKey(
        Measurement, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        """Meta definition for Drug."""
        verbose_name = 'Drug'
        verbose_name_plural = 'Drugs'

    def __str__(self):
        """Unicode representation of Drug."""
        return self.name

    # def save(self, *args, bypass_lock_check=False, **kwargs):
    #     # Ensure that the drug name is capitalized
    #     for field_name in ['name']:
    #         val = getattr(self, field_name, False)
    #         if val:
    #             setattr(self, field_name, val.capitalize())


    #     # Call the parent save method
    #     super(Drug, self).save(*args, **kwargs)


class Sale(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    drug_sold = models.CharField(max_length=200)
    date_sold = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)
    batch_no = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    remaining_quantity = models.FloatField(null=True, blank=True)
    # buying_price = models.FloatField(null=True, blank=True)

    # def total(self):
    #     """Calculate total sale amount."""
    #     return self.quantity * self.sale_price

    # def profit(self):
    #     """Calculate profit from the sale."""
    #     buying = self.quantity * self.drug_sold.buying_price
    #     selling = self.quantity * self.sale_price
    #     return selling - buying

    class Meta:
        """Meta definition for Sale."""
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self):
        return f'{self.drug_sold} sold on {self.date_sold}'


class Stocked(models.Model):
    """Model definition for Stock."""
    drug_name = models.ForeignKey(Drug, on_delete=models.PROTECT)
    date_added = models.DateTimeField(auto_now_add=True)
    supplier = models.CharField(max_length=200, null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.PROTECT)
    number_added = models.IntegerField()
    total = models.IntegerField(null=True)

    class Meta:
        """Meta definition for Stock."""
        verbose_name = 'Stock Addition'
        verbose_name_plural = 'Stock Additions'

    def __str__(self):
        """Unicode representation of Stock."""
        return f'{self.number_added} {self.drug_name} added to stock '

    def save(self, *args, **kwargs):
        for field_name in ['supplier']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Stocked, self).save(*args, **kwargs)

class LockedProduct(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT)
    locked_by = models.ForeignKey(User, on_delete=models.PROTECT)
    date_locked = models.DateTimeField(auto_now_add=True)
    quantity = models.FloatField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)

@receiver(pre_save, sender=LockedProduct)
def prevent_locked_drug_update(sender, instance, **kwargs):
    if instance.pk:  # if it's an update (not a new record)
        original = LockedProduct.objects.get(pk=instance.pk)
        if original.date_locked and instance.drug != original.drug:
            raise PermissionDenied("Cannot update locked drugs.")

class MarketingItem(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class IssuedItem(models.Model):
    item = models.CharField(max_length=255, verbose_name="Item")
    stock = models.PositiveIntegerField(verbose_name="Stock/Quantity")
    issued_to = models.CharField(max_length=255, verbose_name="Issued To")
    quantity_issued = models.PositiveIntegerField(verbose_name="Quantity Issued")
    date_issued = models.DateTimeField(default=now, verbose_name="Date Issued")
    issued_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Issued By",
        related_name="issued_items", null=True, blank=True
    )

    def __str__(self):
        return f"{self.item} - Issued to {self.issued_to} by {self.issued_by}"

    class Meta:
        verbose_name = "Issued Item"
        verbose_name_plural = "Issued Items"
        ordering = ['-date_issued']  # Order by latest issued items first

class PickingList(models.Model):
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)
    product = models.CharField(max_length=255)
    batch_no = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    # in_stock = models.ForeignKey(
    #     Drug, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.client} - {self.product}"
    
class Cannister(models.Model):
    name = models.CharField(max_length=255)
    batch_no = models.CharField(max_length=100, unique=True)
    stock = models.PositiveIntegerField()
    litres = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.batch_no}"
    
class IssuedCannister(models.Model):
    date_issued = models.DateTimeField(default=now)
    date_returned = models.DateTimeField(default=now)
    name = models.CharField(max_length=255)
    batch_no = models.CharField(max_length=100)
    staff_on_duty = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issued_by")
    returned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="returned_by", null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    balance = models.PositiveIntegerField(null=True, blank=True)
    action = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.batch_no} issued to {self.client}, returned {self.action}"
