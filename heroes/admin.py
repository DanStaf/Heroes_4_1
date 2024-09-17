from django.contrib import admin
from heroes.models import Parent, Hero, ParentStatus, HeroStatus, Cell, Training, PaymentType, Payment

# Register your models here.

admin.site.register(Parent)
admin.site.register(Hero)
admin.site.register(ParentStatus)
admin.site.register(HeroStatus)
admin.site.register(Cell)
admin.site.register(Training)
admin.site.register(PaymentType)
admin.site.register(Payment)
