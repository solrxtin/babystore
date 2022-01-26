from django.contrib import admin
from .models import Department, Item, Batch, Sale, Cart


# Register your models here.
admin.site.register(Department)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'price', 'quantity')
admin.site.register(Item, ItemAdmin)

class BatchAdmin(admin.ModelAdmin):
    list_display = ('item', 'batch_rank', 'item_purchased', 'batch_date', 'batch_expiry_date')
admin.site.register(Batch, BatchAdmin)


class SaleAdmin(admin.ModelAdmin):
    list_display = ['item', 'price', 'quantity', 'time_sold']
admin.site.register(Sale, SaleAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['item', 'price', 'quantity', 'user', 'time_added']
admin.site.register(Cart, CartAdmin)


