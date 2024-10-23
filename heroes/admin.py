from django.contrib import admin
from heroes.models import Parent, Hero, ParentStatus, HeroStatus, Branch, Team, Training, PaymentType, Payment

# Register your models here.

admin.site.register(Parent)
admin.site.register(Hero)
admin.site.register(ParentStatus)
admin.site.register(HeroStatus)
admin.site.register(Branch)
admin.site.register(Team)
admin.site.register(Training)
admin.site.register(PaymentType)
admin.site.register(Payment)
