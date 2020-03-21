import csv
from io import TextIOWrapper

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import path

from .forms import CustomUserCreationForm, CustomUserChangeForm, BulkImportForm
from .models import CustomUser, Faculty, Student, Department, ResearchScholar


CSV_HEADERS = {
    Student: ('email', 'id_num', 'name'),
    Faculty: ('email', 'name', 'psrn', 'alt_email', 'contact_num', 'dept'),
    ResearchScholar: (
        'email',
        'name',
        'id_num',
        'tenure_type',
        'fellowship',
        'fellowship_details',
        'joining_date',
        'proposal_approval_date',
        'qualifier_passing_date',
        'graduation_date',
        'supervisor',
        'co_supervisor',
        'dept',
    )
}


EXCLUDE_FIELDS = (
    'password',
    'last_login',
    'is_superuser',
    'groups',
    'user_permissions',
    'is_staff',
    'is_active',
    'date_joined'
)


def create_users(user_type, records):
    headers = CSV_HEADERS[user_type]
    if set(records.fieldnames) != set(headers):
        raise Exception(f"Invalid CSV headers/columns. Expected: {headers}")
    for record in records:
        record = {key: (value or None) for key, value in record.items()}
        if 'dept' in records.fieldnames:
            record['dept'] = Department.objects.get(name=record['dept'])
        if 'supervisor' in records.fieldnames:
            supervisor = Faculty.objects.filter(name=record['supervisor'])
            record['supervisor'] = supervisor.first()
        # TODO: Update object if it already exists instead of failing hard
        try:
            user_type.objects.create(**record)
        except Exception as err:
            raise Exception(f'On row number {records.line_num}: {err}')


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
    exclude = EXCLUDE_FIELDS

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            try:
                csv_file = TextIOWrapper(
                    request.FILES['csv_file'].file,
                    encoding=request.encoding
                )
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
                csv_file.seek(0)
                reader = csv.DictReader(csv_file, dialect=dialect)
            except Exception as err:
                messages.error(request, f'Error: {err}')
                return redirect("..")
            try:
                if '/student/' in request.path:
                    user_type = Student
                elif '/faculty/' in request.path:
                    user_type = Faculty
                elif '/researchscholar/' in request.path:
                    user_type = ResearchScholar
                else:
                    raise Http404
                create_users(user_type, reader)
            except Exception as err:
                messages.error(request, f'Error: {err}')
            else:
                messages.success(request, "Your csv file has been imported")
            return redirect("..")
        form = BulkImportForm()
        payload = {"form": form}
        return render(
            request, "admin/bulk_import_form.html", payload
        )


admin.site.site_header = "CSIS Dashboard - BITS Pilani Hyderabad Campus"
admin.site.site_title = 'CSIS Dashboard'
admin.site.index_title = 'CSIS Dashboard'

admin.site.register(Student, BulkImportAdmin)
admin.site.register(Faculty, BulkImportAdmin)
admin.site.register(Department)
admin.site.register(ResearchScholar, BulkImportAdmin)
