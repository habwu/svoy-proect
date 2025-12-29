from django.contrib import admin

from files.models import AgreementSettings


@admin.register(AgreementSettings)
class AgreementSettingsAdmin(admin.ModelAdmin):
    pass
