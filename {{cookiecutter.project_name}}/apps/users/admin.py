from django.contrib import admin

from .enums import UserRoleEnum
from .models import User
from django import forms

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'username', 'email','password','role'

    role = forms.ChoiceField(choices=UserRoleEnum.choices())

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
