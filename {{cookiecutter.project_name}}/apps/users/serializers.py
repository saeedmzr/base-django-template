from django.core.validators import MinLengthValidator
from rest_framework import serializers

from .validators import number_validator, letter_validator, special_char_validator
from ..base.serializers import BaseModelSerializer
from .models import User


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'is_active', 'created_at', 'updated_at',
            'password', 'confirm_password'
        )

    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        validators=[number_validator, letter_validator, special_char_validator, MinLengthValidator(8)],
        write_only=True,
        required=False  # allow updates without password
    )
    confirm_password = serializers.CharField(
        max_length=255,
        write_only=True,
        required=False  # only needed when setting/changing password
    )

    def validate_username(self, username):
        # If instance exists and username unchanged, allow it.
        qs = User.objects.filter(username=username)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('username already taken')
        return username

    def validate_email(self, email):
        qs = User.objects.filter(email=email)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('email already taken')
        return email

    def _validate_password_pair(self, attrs):
        pwd = attrs.get('password')
        cpwd = attrs.get('confirm_password')
        # Require both when password is being set/changed
        if pwd is None and cpwd is None:
            return
        if not pwd or not cpwd:
            # Map to specific fields for better UX
            raise serializers.ValidationError({
                'password': 'Please fill password and confirm password',
                'confirm_password': 'Please fill password and confirm password',
            })
        if pwd != cpwd:
            raise serializers.ValidationError({
                'confirm_password': 'confirm password is not equal to password'
            })

    def create(self, validated_data):
        # Enforce password/confirm_password on create
        self._validate_password_pair(validated_data)
        validated_data.pop('confirm_password', None)

        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Only enforce pair if password is present in the update payload
        if 'password' in validated_data or 'confirm_password' in validated_data:
            self._validate_password_pair(validated_data)

        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
