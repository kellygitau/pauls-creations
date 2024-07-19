from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Product)
admin.site.register(Ordering)
admin.site.register(Payment)
admin.site.register(PaperSize)
admin.site.register(MaterialSize)
