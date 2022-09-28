from django.contrib import admin

from catalogue.models import Part, MachineModel

admin.site.register([Part, MachineModel])
