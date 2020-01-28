# Generated by Django 3.0.2 on 2020-02-03 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200114_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchScholar',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='scholars', to=settings.AUTH_USER_MODEL)),
                ('id_num', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='ID Number')),
                ('tenure_type', models.CharField(choices=[('FT', 'Full Time'), ('PT', 'Part Time'), ('AS', 'Aspirant')], max_length=2)),
                ('fellowship', models.CharField(choices=[('NONE', 'No Fellowship'), ('INST', 'Institute Fellowship'), ('INDS', 'Industry Funded'), ('PROJ', 'Project Funded')], max_length=4)),
                ('fellowship_details', models.TextField(blank=True, null=True)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('proposal_approval_date', models.DateField(blank=True, null=True)),
                ('qualifier_passing_date', models.DateField(blank=True, null=True)),
                ('graduation_date', models.DateField(blank=True, null=True)),
                ('co_supervisor', models.TextField(blank=True, null=True)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scholars', to='users.Department')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scholars', to='users.Faculty')),
            ],
            options={
                'verbose_name': 'research scholar',
                'default_related_name': 'scholars',
            },
            bases=('users.customuser',),
        ),
    ]
