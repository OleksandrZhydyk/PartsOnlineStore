from django.contrib import admin

from catalogue.models import MachineModel, Part

admin.site.register([Part, MachineModel])
