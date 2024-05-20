from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        if "notes" in fields:
            fields = [field for field in fields if field != "notes"] + ["notes"]
        return fields
