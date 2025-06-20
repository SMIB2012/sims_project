# Generated by Django 5.2.1 on 2025-05-30 07:13

import datetime
import django.core.validators
import django.db.models.deletion
import sims.cases.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('logbook', '0001_initial'),
        ('rotations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the case category', max_length=100, unique=True)),
                ('description', models.TextField(blank=True, help_text='Description of the case category')),
                ('color_code', models.CharField(default='#007bff', help_text='Hex color code for visual identification', max_length=7)),
                ('is_active', models.BooleanField(default=True, help_text='Whether this category is currently active')),
                ('sort_order', models.PositiveIntegerField(default=0, help_text='Sort order for display')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Case Category',
                'verbose_name_plural': 'Case Categories',
                'ordering': ['sort_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='CaseStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cases', models.PositiveIntegerField(default=0, help_text='Total number of cases submitted')),
                ('approved_cases', models.PositiveIntegerField(default=0, help_text='Number of approved cases')),
                ('pending_cases', models.PositiveIntegerField(default=0, help_text='Number of cases pending review')),
                ('draft_cases', models.PositiveIntegerField(default=0, help_text='Number of draft cases')),
                ('simple_cases', models.PositiveIntegerField(default=0, help_text='Number of simple complexity cases')),
                ('moderate_cases', models.PositiveIntegerField(default=0, help_text='Number of moderate complexity cases')),
                ('complex_cases', models.PositiveIntegerField(default=0, help_text='Number of complex cases')),
                ('highly_complex_cases', models.PositiveIntegerField(default=0, help_text='Number of highly complex cases')),
                ('average_self_score', models.FloatField(default=0.0, help_text='Average self-assessment score')),
                ('average_supervisor_score', models.FloatField(default=0.0, help_text='Average supervisor assessment score')),
                ('completion_rate', models.FloatField(default=0.0, help_text='Percentage of cases completed vs required')),
                ('average_submission_time', models.FloatField(default=0.0, help_text='Average days from encounter to submission')),
                ('overdue_cases', models.PositiveIntegerField(default=0, help_text='Number of overdue case submissions')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Last time statistics were updated')),
                ('pg', models.OneToOneField(help_text='Postgraduate for these statistics', limit_choices_to={'role': 'pg'}, on_delete=django.db.models.deletion.CASCADE, related_name='case_statistics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Case Statistics',
                'verbose_name_plural': 'Case Statistics',
            },
        ),
        migrations.CreateModel(
            name='ClinicalCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_title', models.CharField(help_text='Descriptive title for the case', max_length=300)),
                ('date_encountered', models.DateField(help_text='Date when the case was encountered')),
                ('patient_age', models.PositiveIntegerField(help_text='Patient age in years', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(150)])),
                ('patient_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('U', 'Unknown/Not Specified')], help_text='Patient gender', max_length=1)),
                ('complexity', models.CharField(choices=[('simple', 'Simple'), ('moderate', 'Moderate'), ('complex', 'Complex'), ('highly_complex', 'Highly Complex')], default='moderate', help_text='Complexity level of the case', max_length=20)),
                ('chief_complaint', models.TextField(help_text="Patient's chief complaint or presenting symptoms")),
                ('history_of_present_illness', models.TextField(help_text='Detailed history of the present illness')),
                ('past_medical_history', models.TextField(blank=True, help_text='Relevant past medical history')),
                ('family_history', models.TextField(blank=True, help_text='Relevant family history')),
                ('social_history', models.TextField(blank=True, help_text='Social history including habits and occupation')),
                ('physical_examination', models.TextField(help_text='Physical examination findings')),
                ('investigations', models.TextField(blank=True, help_text='Investigations ordered and results')),
                ('differential_diagnosis', models.TextField(blank=True, help_text='Differential diagnosis considerations')),
                ('management_plan', models.TextField(help_text='Management and treatment plan')),
                ('learning_objectives', models.TextField(blank=True, help_text='Learning objectives for this case')),
                ('clinical_reasoning', models.TextField(help_text='Clinical reasoning and thought process')),
                ('learning_points', models.TextField(help_text='Key learning points from this case')),
                ('challenges_faced', models.TextField(blank=True, help_text='Challenges encountered and how they were addressed')),
                ('literature_review', models.TextField(blank=True, help_text='Relevant literature review and evidence')),
                ('outcome', models.TextField(blank=True, help_text='Patient outcome and follow-up')),
                ('follow_up_plan', models.TextField(blank=True, help_text='Follow-up plan and actions required')),
                ('supervisor_feedback', models.TextField(blank=True, help_text="Supervisor's feedback on this case")),
                ('self_assessment_score', models.PositiveIntegerField(blank=True, help_text='Self-assessment score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('supervisor_assessment_score', models.PositiveIntegerField(blank=True, help_text="Supervisor's assessment score (1-10)", null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('case_files', models.FileField(blank=True, help_text='Additional case files (reports, documents)', null=True, upload_to=sims.cases.models.case_file_upload_path)),
                ('case_images', models.ImageField(blank=True, help_text='Case images (X-rays, scans, photos)', null=True, upload_to=sims.cases.models.case_image_upload_path)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted for Review'), ('approved', 'Approved'), ('needs_revision', 'Needs Revision'), ('archived', 'Archived')], default='draft', help_text='Current status of the case', max_length=20)),
                ('is_active', models.BooleanField(default=True, help_text='Whether this case is active')),
                ('is_featured', models.BooleanField(default=False, help_text='Mark as featured case for educational purposes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reviewed_at', models.DateTimeField(blank=True, help_text='Date and time when case was reviewed', null=True)),
                ('category', models.ForeignKey(help_text='Category of the clinical case', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases', to='cases.casecategory')),
                ('created_by', models.ForeignKey(blank=True, help_text='User who created this case', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_cases', to=settings.AUTH_USER_MODEL)),
                ('pg', models.ForeignKey(help_text='Postgraduate who created this case', limit_choices_to={'role': 'pg'}, on_delete=django.db.models.deletion.CASCADE, related_name='clinical_cases', to=settings.AUTH_USER_MODEL)),
                ('primary_diagnosis', models.ForeignKey(help_text='Primary diagnosis', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_cases', to='logbook.diagnosis')),
                ('procedures_performed', models.ManyToManyField(blank=True, help_text='Procedures performed during this case', related_name='clinical_cases', to='logbook.procedure')),
                ('reviewed_by', models.ForeignKey(blank=True, help_text='User who reviewed/approved this case', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_cases', to=settings.AUTH_USER_MODEL)),
                ('rotation', models.ForeignKey(blank=True, help_text='Rotation during which this case occurred', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clinical_cases', to='rotations.rotation')),
                ('secondary_diagnoses', models.ManyToManyField(blank=True, help_text='Secondary or differential diagnoses', related_name='secondary_cases', to='logbook.diagnosis')),
                ('supervisor', models.ForeignKey(blank=True, help_text='Supervising consultant', limit_choices_to={'role__in': ['supervisor', 'admin']}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_cases', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Clinical Case',
                'verbose_name_plural': 'Clinical Cases',
                'ordering': ['-date_encountered', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CaseReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('needs_revision', 'Needs Revision'), ('rejected', 'Rejected')], help_text='Review outcome', max_length=20)),
                ('review_date', models.DateField(default=datetime.date.today, help_text='Date when the review was conducted')),
                ('overall_feedback', models.TextField(help_text='Overall feedback on the case presentation')),
                ('clinical_reasoning_feedback', models.TextField(blank=True, help_text='Feedback on clinical reasoning')),
                ('documentation_feedback', models.TextField(blank=True, help_text='Feedback on case documentation')),
                ('learning_points_feedback', models.TextField(blank=True, help_text='Feedback on learning points identified')),
                ('strengths_identified', models.TextField(blank=True, help_text='Strengths demonstrated in this case')),
                ('areas_for_improvement', models.TextField(blank=True, help_text='Areas requiring improvement')),
                ('recommendations', models.TextField(blank=True, help_text='Specific recommendations for future learning')),
                ('follow_up_required', models.BooleanField(default=False, help_text='Whether follow-up discussion is required')),
                ('clinical_knowledge_score', models.PositiveIntegerField(blank=True, help_text='Clinical knowledge score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('clinical_reasoning_score', models.PositiveIntegerField(blank=True, help_text='Clinical reasoning score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('documentation_score', models.PositiveIntegerField(blank=True, help_text='Documentation quality score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('overall_score', models.PositiveIntegerField(blank=True, help_text='Overall performance score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reviewer', models.ForeignKey(help_text='User conducting the review', limit_choices_to={'role__in': ['supervisor', 'admin']}, on_delete=django.db.models.deletion.CASCADE, related_name='case_reviews', to=settings.AUTH_USER_MODEL)),
                ('case', models.ForeignKey(help_text='Case being reviewed', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='cases.clinicalcase')),
            ],
            options={
                'verbose_name': 'Case Review',
                'verbose_name_plural': 'Case Reviews',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='clinicalcase',
            index=models.Index(fields=['pg', 'date_encountered'], name='cases_clini_pg_id_b9dbf6_idx'),
        ),
        migrations.AddIndex(
            model_name='clinicalcase',
            index=models.Index(fields=['status'], name='cases_clini_status_280b37_idx'),
        ),
        migrations.AddIndex(
            model_name='clinicalcase',
            index=models.Index(fields=['category'], name='cases_clini_categor_57184b_idx'),
        ),
        migrations.AddIndex(
            model_name='clinicalcase',
            index=models.Index(fields=['complexity'], name='cases_clini_complex_ddb78d_idx'),
        ),
        migrations.AddIndex(
            model_name='clinicalcase',
            index=models.Index(fields=['is_featured'], name='cases_clini_is_feat_3b0c46_idx'),
        ),
        migrations.AddIndex(
            model_name='clinicalcase',
            index=models.Index(fields=['created_at'], name='cases_clini_created_4d9739_idx'),
        ),
        migrations.AddConstraint(            model_name='clinicalcase',
            constraint=models.CheckConstraint(check=models.Q(('date_encountered__lte', datetime.date(2025, 5, 30))), name='case_date_not_future'),
        ),
        migrations.AddConstraint(
            model_name='clinicalcase',
            constraint=models.CheckConstraint(check=models.Q(('patient_age__gte', 0), ('patient_age__lte', 150)), name='case_valid_age'),
        ),
        migrations.AlterUniqueTogether(
            name='casereview',
            unique_together={('case', 'reviewer', 'review_date')},
        ),
    ]
