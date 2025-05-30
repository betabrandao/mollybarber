from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_type')
    list_select_related = ('profile',)

    def get_user_type(self, instance):
        return instance.profile.user_type
    get_user_type.short_description = 'Tipo de Usuário'

# Remove o User original e registra o personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
