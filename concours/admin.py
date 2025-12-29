from django.contrib import admin
from .models import Concours, Dossier, Serie, Matiere, Note

admin.site.register(Concours)
admin.site.register(Dossier)
admin.site.register(Serie)
admin.site.register(Matiere)
admin.site.register(Note)
