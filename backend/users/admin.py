import csv
from io import TextIOWrapper

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, CustomUserChangeForm, BulkImportForm
from .models import CustomUser, Faculty, Student, Department


def create_user(user_type, record):

    arg_keys = {
        Student: ['email', 'id_num', 'name'],
        Faculty: ['email', 'name', 'psrn', 'alt_email', 'contact_num', 'dept']
    }

    arg_values_map = {
        Student: ['email', 'id number', 'name'],
        Faculty: ['email', 'name', 'psrn', 'alternate email', 'contact number', 'department']
    }

    if (user_type == Faculty):
        record['department'] = Department.objects.get(name=record['department'])

    arg_values = [record[x] for x in arg_values_map[user_type]]
    arg_dict = dict(zip(arg_keys[user_type], arg_values))
    user_type.objects.create(**arg_dict)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("name", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("name", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("name", "email")
    ordering = ("name", "email")


class BulkImportAdmin(admin.ModelAdmin):
    change_list_template = "admin/csv_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            try:
                csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding=request.encoding)
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
                csv_file.seek(0)
                reader = csv.DictReader(csv_file, dialect=dialect)
            except Exception as err:
                self.message_user(request, "Error: {}".format(err))
                return redirect("..")
            try:
                if ('/student/' in request.path):
                    for row in reader:
                        create_user(Student, row)
                elif ('/faculty/' in request.path):
                    for row in reader:
                        create_user(Faculty, row)
                messages.success(request, "Your csv file has been imported")
            except Exception as err:
                messages.error(request, 'Error on row number {}: {}'.format(reader.line_num, err))
                return redirect("..")
            return redirect("..")
        form = BulkImportForm()
        payload = {"form": form}
        return render(
            request, "admin/bulk_import_form.html", payload
        )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, BulkImportAdmin)
admin.site.register(Faculty, BulkImportAdmin)
admin.site.register(Department)
