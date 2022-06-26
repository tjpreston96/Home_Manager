from django.contrib import admin

from .models import Bill, Maintenance, Note, Photo, Plant, Shopping, Task

# Register your models here.
admin.site.register(Bill)
admin.site.register(Maintenance)
admin.site.register(Note)
admin.site.register(Photo)
admin.site.register(Plant)
admin.site.register(Shopping)
admin.site.register(Task)
