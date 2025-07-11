# Generated by Django 5.2.1 on 2025-05-30 07:12

import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rotations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the procedure', max_length=200, unique=True)),
                ('category', models.CharField(choices=[('basic', 'Basic Procedures'), ('intermediate', 'Intermediate Procedures'), ('advanced', 'Advanced Procedures'), ('diagnostic', 'Diagnostic Procedures'), ('therapeutic', 'Therapeutic Procedures'), ('surgical', 'Surgical Procedures'), ('emergency', 'Emergency Procedures')], default='basic', help_text='Category of the procedure', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the procedure')),
                ('difficulty_level', models.PositiveIntegerField(default=1, help_text='Difficulty level from 1 (basic) to 5 (expert)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('duration_minutes', models.PositiveIntegerField(blank=True, help_text='Typical duration in minutes', null=True)),
                ('cme_points', models.PositiveIntegerField(default=0, help_text='CME points typically awarded for this procedure')),
                ('learning_objectives', models.TextField(blank=True, help_text='Learning objectives for this procedure')),
                ('prerequisites', models.TextField(blank=True, help_text='Prerequisites or requirements before performing')),
                ('assessment_criteria', models.TextField(blank=True, help_text='Criteria for assessing competency in this procedure')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this procedure is currently active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Procedure',
                'verbose_name_plural': 'Procedures',
                'ordering': ['category', 'difficulty_level', 'name'],
            },
        ),
        migrations.CreateModel(
            name='LogbookStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_entries', models.PositiveIntegerField(default=0)),
                ('draft_entries', models.PositiveIntegerField(default=0)),
                ('submitted_entries', models.PositiveIntegerField(default=0)),
                ('approved_entries', models.PositiveIntegerField(default=0)),
                ('revision_entries', models.PositiveIntegerField(default=0)),
                ('total_procedures', models.PositiveIntegerField(default=0)),
                ('unique_procedures', models.PositiveIntegerField(default=0)),
                ('total_skills', models.PositiveIntegerField(default=0)),
                ('unique_skills', models.PositiveIntegerField(default=0)),
                ('average_self_score', models.FloatField(blank=True, null=True)),
                ('average_supervisor_score', models.FloatField(blank=True, null=True)),
                ('average_review_score', models.FloatField(blank=True, null=True)),
                ('total_cme_points', models.PositiveIntegerField(default=0)),
                ('completion_rate', models.FloatField(default=0.0)),
                ('average_review_time', models.FloatField(blank=True, null=True)),
                ('last_entry_date', models.DateField(blank=True, null=True)),
                ('most_active_month', models.CharField(blank=True, max_length=7)),
                ('entries_needing_revision_rate', models.FloatField(default=0.0)),
                ('on_time_submission_rate', models.FloatField(default=0.0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pg', models.OneToOneField(help_text='Postgraduate these statistics belong to', limit_choices_to={'role': 'pg'}, on_delete=django.db.models.deletion.CASCADE, related_name='logbook_stats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Logbook Statistics',
                'verbose_name_plural': 'Logbook Statistics',
            },
        ),
        migrations.CreateModel(
            name='LogbookTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the template', max_length=200, unique=True)),
                ('template_type', models.CharField(choices=[('medical', 'Medical Case'), ('surgical', 'Surgical Case'), ('emergency', 'Emergency Case'), ('outpatient', 'Outpatient Case'), ('procedure', 'Procedure Focused'), ('research', 'Research Activity'), ('teaching', 'Teaching Activity'), ('quality', 'Quality Improvement')], default='medical', help_text='Type of logbook entry this template is for', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Description of when to use this template')),
                ('template_structure', models.JSONField(default=dict, help_text='JSON structure defining the template layout')),
                ('required_fields', models.JSONField(default=list, help_text='List of required fields for this template')),
                ('completion_guidelines', models.TextField(blank=True, help_text='Guidelines for completing entries using this template')),
                ('example_entries', models.TextField(blank=True, help_text='Example entries using this template')),
                ('is_default', models.BooleanField(default=False, help_text='Whether this is a default template')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this template is currently active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, help_text='User who created this template', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_templates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Logbook Template',
                'verbose_name_plural': 'Logbook Templates',
                'ordering': ['template_type', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the diagnosis', max_length=200)),
                ('category', models.CharField(choices=[('cardiovascular', 'Cardiovascular'), ('respiratory', 'Respiratory'), ('gastrointestinal', 'Gastrointestinal'), ('neurological', 'Neurological'), ('endocrine', 'Endocrine'), ('infectious', 'Infectious Disease'), ('hematology', 'Hematology'), ('oncology', 'Oncology'), ('psychiatry', 'Psychiatry'), ('dermatology', 'Dermatology'), ('musculoskeletal', 'Musculoskeletal'), ('genitourinary', 'Genitourinary'), ('other', 'Other')], default='other', help_text='Medical category of the diagnosis', max_length=20)),
                ('icd_code', models.CharField(blank=True, help_text='ICD-10 or ICD-11 code', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the diagnosis')),
                ('typical_presentation', models.TextField(blank=True, help_text='Typical clinical presentation')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this diagnosis is currently active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('common_procedures', models.ManyToManyField(blank=True, help_text='Procedures commonly associated with this diagnosis', related_name='common_diagnoses', to='logbook.procedure')),
            ],
            options={
                'verbose_name': 'Diagnosis',
                'verbose_name_plural': 'Diagnoses',
                'ordering': ['category', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the skill', max_length=200)),
                ('category', models.CharField(choices=[('clinical', 'Clinical Skills'), ('technical', 'Technical Skills'), ('communication', 'Communication Skills'), ('professional', 'Professional Skills'), ('academic', 'Academic Skills'), ('leadership', 'Leadership Skills'), ('research', 'Research Skills')], default='clinical', help_text='Category of the skill', max_length=20)),
                ('level', models.CharField(choices=[('basic', 'Basic Level'), ('intermediate', 'Intermediate Level'), ('advanced', 'Advanced Level'), ('expert', 'Expert Level')], default='basic', help_text='Expected competency level', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the skill')),
                ('competency_requirements', models.TextField(blank=True, help_text='Requirements to demonstrate competency')),
                ('assessment_methods', models.TextField(blank=True, help_text='Methods for assessing this skill')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this skill is currently active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
                'ordering': ['category', 'level', 'name'],
                'indexes': [models.Index(fields=['category'], name='logbook_ski_categor_6c0464_idx'), models.Index(fields=['level'], name='logbook_ski_level_24d5c0_idx'), models.Index(fields=['is_active'], name='logbook_ski_is_acti_b9cb8b_idx')],
                'constraints': [models.UniqueConstraint(fields=('name', 'category'), name='unique_skill_per_category')],
            },
        ),
        migrations.AddField(
            model_name='procedure',
            name='required_skills',
            field=models.ManyToManyField(blank=True, help_text='Skills required to perform this procedure', related_name='required_for_procedures', to='logbook.skill'),
        ),
        migrations.CreateModel(
            name='LogbookEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Date of the clinical encounter')),
                ('case_title', models.CharField(blank=True, help_text='Brief title or summary of the case', max_length=300)),
                ('patient_age', models.PositiveIntegerField(help_text='Patient age in years', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(150)])),
                ('patient_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('U', 'Unknown/Not Specified')], help_text='Patient gender', max_length=1)),
                ('patient_chief_complaint', models.TextField(help_text="Patient's chief complaint or presenting symptoms")),
                ('patient_history_summary', models.TextField(blank=True, help_text='Brief summary of relevant patient history')),
                ('investigations_ordered', models.TextField(blank=True, help_text='Investigations ordered and results')),
                ('clinical_reasoning', models.TextField(help_text='Clinical reasoning and thought process')),
                ('learning_points', models.TextField(help_text='Key learning points from this case')),
                ('challenges_faced', models.TextField(blank=True, help_text='Challenges encountered and how they were addressed')),
                ('follow_up_required', models.TextField(blank=True, help_text='Follow-up actions or learning required')),
                ('supervisor_feedback', models.TextField(blank=True, help_text="Supervisor's feedback on this case")),
                ('self_assessment_score', models.PositiveIntegerField(blank=True, help_text='Self-assessment score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('supervisor_assessment_score', models.PositiveIntegerField(blank=True, help_text="Supervisor's assessment score (1-10)", null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted for Review'), ('approved', 'Approved'), ('needs_revision', 'Needs Revision'), ('archived', 'Archived')], default='draft', help_text='Current status of the entry', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('verified_at', models.DateTimeField(blank=True, help_text='Date and time when entry was verified', null=True)),
                ('created_by', models.ForeignKey(blank=True, help_text='User who created this entry', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_entries', to=settings.AUTH_USER_MODEL)),
                ('pg', models.ForeignKey(help_text='Postgraduate who created this entry', limit_choices_to={'role': 'pg'}, on_delete=django.db.models.deletion.CASCADE, related_name='logbook_entries', to=settings.AUTH_USER_MODEL)),
                ('primary_diagnosis', models.ForeignKey(help_text='Primary diagnosis', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_entries', to='logbook.diagnosis')),
                ('rotation', models.ForeignKey(blank=True, help_text='Rotation during which this case occurred', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logbook_entries', to='rotations.rotation')),
                ('secondary_diagnoses', models.ManyToManyField(blank=True, help_text='Secondary or differential diagnoses', related_name='secondary_entries', to='logbook.diagnosis')),
                ('supervisor', models.ForeignKey(blank=True, help_text='Supervising consultant', limit_choices_to={'role__in': ['supervisor', 'admin']}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_entries', to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(blank=True, help_text='User who verified/approved this entry', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verified_entries', to=settings.AUTH_USER_MODEL)),
                ('template', models.ForeignKey(blank=True, help_text='Template used for this entry', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logbook_entries', to='logbook.logbooktemplate')),
                ('procedures', models.ManyToManyField(blank=True, help_text='Procedures performed or observed', related_name='logbook_entries', to='logbook.procedure')),
                ('skills', models.ManyToManyField(blank=True, help_text='Skills demonstrated during this case', related_name='logbook_entries', to='logbook.skill')),
            ],
            options={
                'verbose_name': 'Logbook Entry',
                'verbose_name_plural': 'Logbook Entries',
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='LogbookReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending Review'), ('approved', 'Approved'), ('needs_revision', 'Needs Revision'), ('rejected', 'Rejected')], default='pending', help_text='Review status', max_length=20)),
                ('review_date', models.DateField(default=django.utils.timezone.now, help_text='Date when the review was conducted')),
                ('feedback', models.TextField(help_text='Overall feedback on the entry')),
                ('strengths_identified', models.TextField(blank=True, help_text='Strengths demonstrated in this case')),
                ('areas_for_improvement', models.TextField(blank=True, help_text='Areas requiring improvement')),
                ('recommendations', models.TextField(blank=True, help_text='Specific recommendations for future learning')),
                ('follow_up_required', models.BooleanField(default=False, help_text='Whether follow-up discussion is required')),
                ('clinical_knowledge_score', models.PositiveIntegerField(blank=True, help_text='Clinical knowledge score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('clinical_skills_score', models.PositiveIntegerField(blank=True, help_text='Clinical skills score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('professionalism_score', models.PositiveIntegerField(blank=True, help_text='Professionalism score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('overall_score', models.PositiveIntegerField(blank=True, help_text='Overall performance score (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('logbook_entry', models.ForeignKey(help_text='Logbook entry being reviewed', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='logbook.logbookentry')),
                ('reviewer', models.ForeignKey(help_text='Person conducting the review', limit_choices_to={'role__in': ['supervisor', 'admin']}, on_delete=django.db.models.deletion.CASCADE, related_name='logbook_reviews_given', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Logbook Review',
                'verbose_name_plural': 'Logbook Reviews',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['logbook_entry', 'status'], name='logbook_log_logbook_09a6b6_idx'), models.Index(fields=['reviewer'], name='logbook_log_reviewe_516cc6_idx'), models.Index(fields=['review_date'], name='logbook_log_review__3d60f8_idx'), models.Index(fields=['status'], name='logbook_log_status_cf1b86_idx')],
                'constraints': [models.UniqueConstraint(fields=('logbook_entry', 'reviewer'), name='unique_review_per_reviewer_entry')],
            },
        ),
        migrations.AddIndex(
            model_name='logbooktemplate',
            index=models.Index(fields=['template_type'], name='logbook_log_templat_69f4ca_idx'),
        ),
        migrations.AddIndex(
            model_name='logbooktemplate',
            index=models.Index(fields=['is_default'], name='logbook_log_is_defa_0eaaff_idx'),
        ),
        migrations.AddIndex(
            model_name='logbooktemplate',
            index=models.Index(fields=['is_active'], name='logbook_log_is_acti_b2f794_idx'),
        ),
        migrations.AddIndex(
            model_name='diagnosis',
            index=models.Index(fields=['category'], name='logbook_dia_categor_4172fe_idx'),
        ),
        migrations.AddIndex(
            model_name='diagnosis',
            index=models.Index(fields=['icd_code'], name='logbook_dia_icd_cod_5ed9be_idx'),
        ),
        migrations.AddIndex(
            model_name='diagnosis',
            index=models.Index(fields=['is_active'], name='logbook_dia_is_acti_441d42_idx'),
        ),
        migrations.AddConstraint(
            model_name='diagnosis',
            constraint=models.UniqueConstraint(fields=('name', 'category'), name='unique_diagnosis_per_category'),
        ),
        migrations.AddIndex(
            model_name='procedure',
            index=models.Index(fields=['category'], name='logbook_pro_categor_791b2c_idx'),
        ),
        migrations.AddIndex(
            model_name='procedure',
            index=models.Index(fields=['difficulty_level'], name='logbook_pro_difficu_83f5f2_idx'),
        ),
        migrations.AddIndex(
            model_name='procedure',
            index=models.Index(fields=['is_active'], name='logbook_pro_is_acti_b761e8_idx'),
        ),
        migrations.AddIndex(
            model_name='logbookentry',
            index=models.Index(fields=['pg', 'date'], name='logbook_log_pg_id_92f47b_idx'),
        ),
        migrations.AddIndex(
            model_name='logbookentry',
            index=models.Index(fields=['status'], name='logbook_log_status_3fb333_idx'),
        ),
        migrations.AddIndex(
            model_name='logbookentry',
            index=models.Index(fields=['date'], name='logbook_log_date_2af6e4_idx'),
        ),
        migrations.AddIndex(
            model_name='logbookentry',
            index=models.Index(fields=['rotation'], name='logbook_log_rotatio_2736f5_idx'),
        ),
        migrations.AddIndex(
            model_name='logbookentry',
            index=models.Index(fields=['supervisor'], name='logbook_log_supervi_0874c8_idx'),
        ),
        migrations.AddIndex(
            model_name='logbookentry',
            index=models.Index(fields=['primary_diagnosis'], name='logbook_log_primary_5774a8_idx'),
        ),
        migrations.AddIndex(
            model_name='logbookentry',
            index=models.Index(fields=['created_at'], name='logbook_log_created_2b3be3_idx'),
        ),
        migrations.AddConstraint(            model_name='logbookentry',
            constraint=models.CheckConstraint(check=models.Q(('date__lte', datetime.date(2025, 5, 30))), name='logbook_entry_date_not_future'),
        ),
        migrations.AddConstraint(
            model_name='logbookentry',
            constraint=models.CheckConstraint(check=models.Q(('patient_age__gte', 0), ('patient_age__lte', 150)), name='logbook_entry_valid_age'),
        ),
    ]
