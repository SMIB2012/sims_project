from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import User, SupervisorProfile, ResidentProfile

class UserResource(resources.ModelResource):
    """Resource for bulk import/export of users via CSV/Excel"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'role', 'specialty', 'year', 'supervisor__username', 
                 'is_active', 'date_joined')
        export_order = fields
        import_id_fields = ('username',)
        
    def before_import_row(self, row, **kwargs):
        """Custom logic before importing each row"""
        # Convert supervisor username to supervisor object if provided
        supervisor_username = row.get('supervisor__username')
        if supervisor_username:
            try:
                supervisor = User.objects.get(username=supervisor_username, role='supervisor')
                row['supervisor'] = supervisor.id
            except User.DoesNotExist:
                row['supervisor'] = None
        return row

class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form for admin"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 
                 'specialty', 'year', 'supervisor')

class CustomUserChangeForm(UserChangeForm):
    """Custom user change form for admin"""
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced user admin with role-based management and custom UI"""
    
    # Note: ImportExportModelAdmin temporarily removed to showcase UI improvements
    # resource_class = UserResource
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_list_template = 'admin/sims_users/user/change_list.html'
    
    list_display = ('username', 'get_full_name', 'email', 'get_role_display',
                   'specialty', 'year', 'supervisor', 'get_status_display', 'date_joined')
    # list_filter = ('role', 'specialty', 'year', 'is_active', 'is_staff', 'date_joined')  # Removed to eliminate default filters
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    list_per_page = 25
    list_max_show_all = 100
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('SIMS Role & Assignment'), {
            'fields': ('role', 'specialty', 'year', 'supervisor'),
            'description': 'Role-based access control for SIMS system'
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        (_('SIMS Role & Assignment'), {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'role', 'specialty', 'year', 'supervisor'),
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add enhanced context for our custom UI"""
        extra_context = extra_context or {}

        # Add any additional context needed for our custom template
        extra_context['custom_css'] = ""
        extra_context['custom_js'] = ""

        return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        """Filter queryset based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == 'admin':
            return qs
        elif request.user.role == 'supervisor':
            # Supervisors can only view their assigned PGs
            return qs.filter(supervisor=request.user)
        else:
            # PGs can only view their own profile
            return qs.filter(id=request.user.id)
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize form based on user permissions"""
        form = super().get_form(request, obj, **kwargs)
        
        if not request.user.is_superuser:
            # Non-superusers cannot modify superuser status
            if 'is_superuser' in form.base_fields:
                form.base_fields['is_superuser'].disabled = True
            
            # Only admins can assign admin role
            if request.user.role != 'admin' and 'role' in form.base_fields:
                choices = [choice for choice in form.base_fields['role'].choices 
                          if choice[0] != 'admin']
                form.base_fields['role'].choices = choices
        
        return form
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter supervisor choices to only show supervisors"""
        if db_field.name == "supervisor":
            kwargs["queryset"] = User.objects.filter(role='supervisor')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_add_permission(self, request):
        """Control who can add users"""
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_change_permission(self, request, obj=None):
        """Control who can change users"""
        if request.user.is_superuser or request.user.role == 'admin':
            return True
        if request.user.role == 'supervisor' and obj:
            return obj.supervisor == request.user
        if obj:
            return obj == request.user
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Control who can delete users"""
        return request.user.is_superuser or request.user.role == 'admin'
    
    def get_full_name(self, obj):
        """Display full name with fallback"""
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name or obj.username
    get_full_name.short_description = "Full Name"
    get_full_name.admin_order_field = 'first_name'

    def get_role_display(self, obj):
        """Enhanced role display with color coding"""
        if obj.role == 'admin':
            return f"🔴 {obj.get_role_display()}"
        elif obj.role == 'supervisor':
            return f"🟠 {obj.get_role_display()}"
        elif obj.role == 'pg':
            return f"🟢 {obj.get_role_display()}"
        return obj.get_role_display()
    get_role_display.short_description = "Role"
    get_role_display.admin_order_field = 'role'

    def get_status_display(self, obj):
        """Enhanced status display"""
        if obj.is_active:
            return "✅ Active"
        else:
            return "❌ Inactive"
    get_status_display.short_description = "Status"
    get_status_display.admin_order_field = 'is_active'
    get_status_display.boolean = True

    def save_model(self, request, obj, form, change):
        """Custom save logic"""
        if not change:  # New user
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(SupervisorProfile)
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'supervisor_type', 'department', 'cv_verified', 'specialty_certificate_verified', 'updated_at')
    list_filter = ('supervisor_type', 'department', 'cv_verified', 'specialty_certificate_verified')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'department__name')
    readonly_fields = ('user', 'created_at', 'updated_at') # User should not be changed once profile is created
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Details', {'fields': ('supervisor_type', 'department')}),
        ('Documents', {'fields': ('cv_file', 'cv_verified', 'specialty_certificate_file', 'specialty_certificate_verified', 'publications_list_file')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'department')

@admin.register(ResidentProfile)
class ResidentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'training_type', 'program_duration', 'get_supervisor_name', 'department', 'updated_at')
    list_filter = ('training_type', 'program_duration', 'department', 'supervisor__user__last_name')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'department__name', 'supervisor__user__username')
    readonly_fields = ('user', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Training Details', {'fields': ('training_type', 'program_duration', 'supervisor', 'department')}),
        ('Initial Credentials', {
            'classes': ('collapse',),
            'fields': (
                ('mbbs_certificate', 'mbbs_certificate_verified'),
                ('fsc_certificate', 'fsc_certificate_verified'),
                ('matric_certificate', 'matric_certificate_verified'),
                ('pmdc_registration', 'pmdc_registration_verified'),
                ('house_job_certificate', 'house_job_certificate_verified'),
                ('experience_certificate', 'experience_certificate_verified'),
                ('program_letter', 'program_letter_verified'),
            )
        }),
        ('Ongoing Documents', {
            'classes': ('collapse',),
            'fields': (
                ('workshop_details_file', 'workshop_details_verified'),
                ('imm_result_file', 'imm_result_verified'),
                ('final_exam_result_file', 'final_exam_result_verified'),
                ('thesis_file', 'thesis_verified'),
                ('wpba_records_file', 'wpba_records_verified'),
            )
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'supervisor__user', 'department')

    def get_supervisor_name(self, obj):
        if obj.supervisor:
            return obj.supervisor.user.get_full_name()
        return None
    get_supervisor_name.short_description = 'Supervisor'
    get_supervisor_name.admin_order_field = 'supervisor__user__last_name'


# Customize admin site headers
admin.site.site_header = "SIMS - Postgraduate Medical Training System"
admin.site.site_title = "SIMS Admin"
admin.site.index_title = "Welcome to SIMS Administration"