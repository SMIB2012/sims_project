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
from .models import User

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
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    """Enhanced user admin with bulk import/export and role-based management"""
    
    resource_class = UserResource
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = ('username', 'get_full_name', 'email', 'get_role_display', 
                   'specialty', 'year', 'supervisor', 'get_status_display', 'date_joined')
    list_filter = ('role', 'specialty', 'year', 'is_active', 'is_staff', 'date_joined')
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
    
    def add_view(self, request, form_url='', extra_context=None):
        """Override add view to redirect to custom user creation form"""
        # Redirect to our enhanced custom user creation form with admin context
        return HttpResponseRedirect(reverse('users:user_create') + '?next=/admin/users/user/')
    
    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add custom CSS and JS"""
        extra_context = extra_context or {}
        
        # Add custom CSS and JS that will be injected into the template
        extra_context['custom_css'] = """
            <style>
                /* SIMS Admin User List Enhancements */
                .change-list .results {
                    max-height: 70vh !important;
                    overflow-y: auto !important;
                    border-radius: 8px !important;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
                }
                
                .change-list .results thead th {
                    position: sticky !important;
                    top: 0 !important;
                    background: linear-gradient(135deg, #417690 0%, #2c5aa0 100%) !important;
                    color: white !important;
                    padding: 12px 8px !important;
                    font-weight: 600 !important;
                    font-size: 0.85rem !important;
                    text-transform: uppercase !important;
                    z-index: 100 !important;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
                    border: none !important;
                }
                
                .change-list .results thead th a {
                    color: white !important;
                    text-decoration: none !important;
                }
                
                .change-list .results tbody tr:hover {
                    background: rgba(65, 118, 144, 0.05) !important;
                }
                
                #content h1:before {
                    content: "👥 ";
                    color: #417690;
                    font-size: 1.2em;
                }
                
                .field-get_role_display {
                    font-weight: 600 !important;
                }
                
                .field-get_status_display {
                    font-weight: 600 !important;
                }
            </style>
        """
        
        extra_context['custom_js'] = """
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    console.log('SIMS Admin Enhancement Loading...');
                    
                    // Add user statistics
                    setTimeout(function() {
                        const rows = document.querySelectorAll('.change-list .results tbody tr');
                        if (rows.length > 0) {
                            const statsDiv = document.createElement('div');
                            statsDiv.style.cssText = `
                                background: linear-gradient(135deg, #e3f2fd 0%, #f1f8e9 100%);
                                padding: 1rem;
                                margin: 1rem 0;
                                border-radius: 8px;
                                display: flex;
                                gap: 1rem;
                                flex-wrap: wrap;
                                font-weight: 600;
                                border: 1px solid #e9ecef;
                            `;
                            
                            statsDiv.innerHTML = `
                                <span>👥 Total Users: <strong style="background: white; padding: 0.25rem 0.5rem; border-radius: 10px; color: #417690;">${rows.length}</strong></span>
                                <span>� Page Size: <strong style="background: white; padding: 0.25rem 0.5rem; border-radius: 10px; color: #417690;">25</strong></span>
                            `;
                            
                            const changeList = document.querySelector('.change-list');
                            if (changeList) {
                                changeList.insertBefore(statsDiv, changeList.firstChild);
                            }
                        }
                        console.log('SIMS Admin Enhancement Complete!');
                    }, 200);
                });
            </script>
        """
        
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

# Customize admin site headers
admin.site.site_header = "SIMS - Postgraduate Medical Training System"
admin.site.site_title = "SIMS Admin"
admin.site.index_title = "Welcome to SIMS Administration"