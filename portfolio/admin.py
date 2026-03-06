from django.contrib import admin
from django import forms
from .models import (
    Profile, Experience, Education, Project,
    Skill, Certificate, Testimonial, ContactMessage
)


class ExperienceAdminForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ExperienceAdmin(admin.ModelAdmin):
    form = ExperienceAdminForm
    list_display = ("title", "company", "start_date", "end_date", "currently_working")
    list_filter = ("employment_type", "currently_working")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "subject")


admin.site.register(Profile)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Certificate)
admin.site.register(Testimonial)