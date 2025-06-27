from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse

# Role choices for the SIMS system
USER_ROLES = (
    ('admin', 'Admin'),
    ('supervisor', 'Supervisor'),
    ('pg', 'Postgraduate'),
)

# Medical specialty choices (expand as needed)
SPECIALTY_CHOICES = (
    ('medicine', 'Internal Medicine'),
    ('surgery', 'Surgery'),
    ('pediatrics', 'Pediatrics'),
    ('gynecology', 'Gynecology & Obstetrics'),
    ('orthopedics', 'Orthopedics'),
    ('cardiology', 'Cardiology'),
    ('neurology', 'Neurology'),
    ('psychiatry', 'Psychiatry'),
    ('dermatology', 'Dermatology'),
    ('radiology', 'Radiology'),
    ('anesthesia', 'Anesthesia'),
    ('pathology', 'Pathology'),
    ('microbiology', 'Microbiology'),
    ('pharmacology', 'Pharmacology'),
    ('community_medicine', 'Community Medicine'),
    ('forensic_medicine', 'Forensic Medicine'),
    ('other', 'Other'),
)

# Year choices for PG training
YEAR_CHOICES = (
    ('1', 'Year 1'),
    ('2', 'Year 2'),
    ('3', 'Year 3'),
    ('4', 'Year 4'),  # For some specialties
)

class User(AbstractUser):
    """
    Custom User model for SIMS with role-based access control.
    
    Extends Django's AbstractUser to include medical training specific fields:
    - Role-based permissions (Admin/Supervisor/PG)
    - Medical specialty and training year
    - Supervisor-PG relationships
    - Audit trail fields
    
    Created: 2025-05-29 15:57:19 UTC
    Author: SMIB2012
    """
    
    # Core SIMS fields
    role = models.CharField(
        max_length=20, 
        choices=USER_ROLES,
        help_text="User role determines access permissions in SIMS"
    )
    
    specialty = models.CharField(
        max_length=100, 
        choices=SPECIALTY_CHOICES, 
        blank=True, 
        null=True,
        help_text="Medical specialty (required for PGs and Supervisors)"
    )
    
    year = models.CharField(
        max_length=10, 
        choices=YEAR_CHOICES, 
        blank=True, 
        null=True,
        help_text="Training year (required for PGs)"
    )
    
    supervisor = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_pgs',
        limit_choices_to={'role': 'supervisor'},
        help_text="Assigned supervisor (required for PGs)"
    )
    
    # Profile fields
    registration_number = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Medical council registration number"
    )
    
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text="Contact phone number"
    )
    
    # Audit fields
    created_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='users_created',
        help_text="Admin who created this user account"
    )
    
    modified_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='users_modified',
        help_text="Last admin to modify this user account"
    )
    
    last_login_ip = models.GenericIPAddressField(
        null=True, 
        blank=True,
        help_text="IP address of last login"
    )
    
    # Status fields
    is_archived = models.BooleanField(
        default=False,
        help_text="Mark as archived instead of deleting"
    )
    
    archived_date = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Date when user was archived"
    )
    
    class Meta:
        verbose_name = "SIMS User"
        verbose_name_plural = "SIMS Users"
        ordering = ['role', 'last_name', 'first_name']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['specialty']),
            models.Index(fields=['supervisor']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        """String representation showing name and role"""
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({self.get_role_display()})"
        return f"{self.username} ({self.get_role_display()})"
    
    def clean(self):
        """Validate model fields and business rules"""
        super().clean()
        
        # PGs must have specialty, year, and supervisor
        if self.role == 'pg':
            if not self.specialty:
                raise ValidationError({'specialty': 'Specialty is required for PGs'})
            if not self.year:
                raise ValidationError({'year': 'Training year is required for PGs'})
            if not self.supervisor:
                raise ValidationError({'supervisor': 'Supervisor is required for PGs'})
        
        # Supervisors must have specialty
        if self.role == 'supervisor' and not self.specialty:
            raise ValidationError({'specialty': 'Specialty is required for Supervisors'})
        
        # Admins don't need specialty/year/supervisor
        if self.role == 'admin':
            if self.supervisor:
                raise ValidationError({'supervisor': 'Admins cannot have supervisors'})
        
        # Prevent self-supervision
        if self.supervisor == self:
            raise ValidationError({'supervisor': 'Users cannot supervise themselves'})
        
        # Ensure supervisor is actually a supervisor
        if self.supervisor and self.supervisor.role != 'supervisor':
            raise ValidationError({'supervisor': 'Assigned supervisor must have supervisor role'})
    
    def save(self, *args, **kwargs):
        """Override save to handle archiving and validation"""
        # Run validation
        self.full_clean()
        
        # Set archived date if being archived
        if self.is_archived and not self.archived_date:
            self.archived_date = timezone.now()
        
        # Clear archived date if un-archiving
        if not self.is_archived and self.archived_date:
            self.archived_date = None
        
        super().save(*args, **kwargs)
    
    # Role checking methods
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == 'admin'
    
    def is_supervisor(self):
        """Check if user is a supervisor"""
        return self.role == 'supervisor'
    
    def is_pg(self):
        """Check if user is a postgraduate"""
        return self.role == 'pg'
    
    # Relationship methods
    def get_assigned_pgs(self):
        """Get all PGs assigned to this supervisor"""
        if self.is_supervisor():
            return self.assigned_pgs.filter(is_active=True, is_archived=False)
        return User.objects.none()
    
    def get_supervisor_name(self):
        """Get supervisor's full name or username"""
        if self.supervisor:
            return self.supervisor.get_full_name() or self.supervisor.username
        return "No Supervisor Assigned"
    
    # Dashboard URLs
    def get_dashboard_url(self):
        """Get appropriate dashboard URL based on role"""
        if self.is_admin():
            return reverse('admin:index')
        elif self.is_supervisor():
            return reverse('users:supervisor_dashboard')
        elif self.is_pg():
            return reverse('users:pg_dashboard')
        return reverse('users:profile')
    
    def get_absolute_url(self):
        """Get URL for user detail/profile"""
        return reverse('users:profile', kwargs={'pk': self.pk})
    
    # Display methods
    def get_display_name(self):
        """Get display name for UI"""
        full_name = self.get_full_name()
        return full_name if full_name else self.username
    
    def get_role_badge_class(self):
        """Get CSS class for role badge"""
        role_classes = {
            'admin': 'badge-danger',
            'supervisor': 'badge-warning', 
            'pg': 'badge-info'
        }
        return role_classes.get(self.role, 'badge-secondary')
    
    # Statistics methods (for analytics)
    # IMPORTANT: The get_documents_pending_count method will need to be updated
    # after Profile models are fully integrated with other apps (Rotations, Certificates).
    # It currently relies on User.get_assigned_pgs() and assumes related models
    # link directly to User or will be adapted smoothly.
    def get_documents_pending_count(self):
        """Get count of documents pending review (for supervisors)"""
        if not self.is_supervisor():
            return 0
        
        count = 0
        try:
            # Import here to avoid circular imports
            from django.apps import apps

            # Check if apps exist before importing
            if apps.is_installed('sims.certificates'):
                from sims.certificates.models import Certificate
                for pg in self.get_assigned_pgs():
                    count += Certificate.objects.filter(pg=pg, status='pending').count()

            if apps.is_installed('sims.rotations'):
                from sims.rotations.models import Rotation
                for pg in self.get_assigned_pgs():
                    count += Rotation.objects.filter(pg=pg, status='pending').count()

            if apps.is_installed('sims.logbook'):
                from sims.logbook.models import LogbookEntry
                for pg in self.get_assigned_pgs():
                    count += LogbookEntry.objects.filter(pg=pg, status='pending').count()

            if apps.is_installed('sims.cases'):
                from sims.cases.models import ClinicalCase
                for pg in self.get_assigned_pgs():
                    count += ClinicalCase.objects.filter(pg=pg, status='pending').count()

        except ImportError:
            # Handle case where related models don't exist yet
            pass
        
        return count

# Profile Models

# Upload path helper functions (must be top-level for migrations)
def upload_supervisor_cv(instance, filename):
    return f'supervisors/{instance.user.username}/cv/{filename}'

def upload_supervisor_certificate(instance, filename):
    return f'supervisors/{instance.user.username}/certificates/{filename}'

def upload_supervisor_publications(instance, filename):
    return f'supervisors/{instance.user.username}/publications/{filename}'

def upload_resident_initial_credential(instance, filename):
    # Adding field name to path can be tricky if field name changes.
    # For simplicity, keeping a generic 'initial_credentials' folder.
    return f'residents/{instance.user.username}/initial_credentials/{filename}'

def upload_resident_ongoing_document(instance, filename):
    return f'residents/{instance.user.username}/ongoing_documents/{filename}'

# Choices for SupervisorProfile
SUPERVISOR_TYPE_CHOICES = (
    ('fcps', 'FCPS'),
    ('md_ms', 'MD/MS'),
    ('diploma', 'Diploma'),
)

class SupervisorProfile(models.Model):
    """Profile for Supervisors, linked to the User model."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='supervisor_profile',
        limit_choices_to={'role': 'supervisor'}
    )
    supervisor_type = models.CharField(
        max_length=20,
        choices=SUPERVISOR_TYPE_CHOICES,
        help_text="Type of supervisor qualification"
    )
    department = models.ForeignKey(
        'rotations.Department',  # Use string to avoid circular import if Department is in another app
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervisors_in_department',
        help_text="Department affiliation"
    )
    # Document uploads
    cv_file = models.FileField(
        upload_to=upload_supervisor_cv,
        blank=True,
        null=True,
        help_text="Curriculum Vitae document"
    )
    specialty_certificate_file = models.FileField(
        upload_to=upload_supervisor_certificate,
        blank=True,
        null=True,
        help_text="Specialty/qualification certificate"
    )
    publications_list_file = models.FileField(
        upload_to=upload_supervisor_publications,
        blank=True,
        null=True,
        help_text="List of publications or significant achievements"
    )

    # Verification status by Admin (example fields)
    cv_verified = models.BooleanField(default=False, help_text="Admin verified CV")
    specialty_certificate_verified = models.BooleanField(default=False, help_text="Admin verified specialty certificate")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Supervisor Profile: {self.user.get_full_name()}"

    class Meta:
        verbose_name = "Supervisor Profile"
        verbose_name_plural = "Supervisor Profiles"

# Choices for ResidentProfile
TRAINING_TYPE_CHOICES = (
    ('fcps', 'FCPS'),
    ('md_ms', 'MD/MS'),
    ('diploma', 'Diploma'),
    ('other', 'Other'),
)

# Note: resident_document_path_factory removed as it's replaced by specific top-level functions.

class ResidentProfile(models.Model):
    """Profile for Postgraduate Residents, linked to the User model."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='resident_profile',
        limit_choices_to={'role': 'pg'}
    )
    training_type = models.CharField(
        max_length=20,
        choices=TRAINING_TYPE_CHOICES,
        help_text="Type of training program"
    )
    program_duration = models.PositiveIntegerField(
        help_text="Duration of the training program in years"
    )
    supervisor = models.ForeignKey(
        SupervisorProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # A resident might not be assigned a supervisor initially
        related_name='assigned_residents',
        help_text="Assigned supervisor"
    )
    department = models.ForeignKey(
        'rotations.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # May not be in a specific department initially or between rotations
        related_name='residents_in_department',
        help_text="Current primary department (if any)"
    )

    # Initial Credentials
    mbbs_certificate = models.FileField(upload_to=upload_resident_initial_credential, blank=True, null=True)
    mbbs_certificate_verified = models.BooleanField(default=False)
    fsc_certificate = models.FileField(upload_to=upload_resident_initial_credential, blank=True, null=True)
    fsc_certificate_verified = models.BooleanField(default=False)
    matric_certificate = models.FileField(upload_to=upload_resident_initial_credential, blank=True, null=True)
    matric_certificate_verified = models.BooleanField(default=False)
    pmdc_registration = models.FileField(upload_to=upload_resident_initial_credential, blank=True, null=True)
    pmdc_registration_verified = models.BooleanField(default=False)
    house_job_certificate = models.FileField(upload_to=upload_resident_initial_credential, blank=True, null=True)
    house_job_certificate_verified = models.BooleanField(default=False)
    experience_certificate = models.FileField(upload_to=upload_resident_initial_credential, blank=True, null=True)
    experience_certificate_verified = models.BooleanField(default=False)
    program_letter = models.FileField(upload_to=upload_resident_initial_credential, blank=True, null=True)
    program_letter_verified = models.BooleanField(default=False)

    # Ongoing Uploads
    workshop_details_file = models.FileField(upload_to=upload_resident_ongoing_document, blank=True, null=True, help_text="Consolidated workshops details or zip")
    workshop_details_verified = models.BooleanField(default=False)
    imm_result_file = models.FileField(upload_to=upload_resident_ongoing_document, blank=True, null=True)
    imm_result_verified = models.BooleanField(default=False)
    final_exam_result_file = models.FileField(upload_to=upload_resident_ongoing_document, blank=True, null=True)
    final_exam_result_verified = models.BooleanField(default=False)
    thesis_file = models.FileField(upload_to=upload_resident_ongoing_document, blank=True, null=True)
    thesis_verified = models.BooleanField(default=False)
    wpba_records_file = models.FileField(upload_to=upload_resident_ongoing_document, blank=True, null=True, help_text="Workplace Based Assessments records")
    wpba_records_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resident Profile: {self.user.get_full_name()}"

    class Meta:
        verbose_name = "Resident Profile"
        verbose_name_plural = "Resident Profiles"

    def clean(self):
        super().clean()
        # Ensure the linked user is a PG
        if self.user and self.user.role != 'pg':
            raise ValidationError("Resident profile must be linked to a Postgraduate user.")
        # Ensure the assigned supervisor's user is a supervisor
        if self.supervisor and self.supervisor.user.role != 'supervisor':
            raise ValidationError("Assigned supervisor must have a 'supervisor' role.")

    # get_documents_submitted_count was removed from User model.
    # This functionality will be part of ResidentProfile or calculated based on it.