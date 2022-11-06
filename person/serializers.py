from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'image')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists')
        return email

    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError("Password must be more than 6 strings!")
        if len(password) > 14:
            raise serializers.ValidationError("Password must be least than 14 strings!")
        if any([True for x in password if x in '!@#$%^&*()-=+[]{}<>/\|?,_. ']):
            raise serializers.ValidationError('Password must be without "!@#$%^&*()-=+[]{}<>/?, "')
        return password

    def validate(self, validate_data):
        p1 = validate_data['password']
        p2 = validate_data['password_confirm']
        if p1 != p2:
            raise serializers.ValidationError('Password doesn`t match!')
        del validate_data['password_confirm']
        return validate_data

    def create(self, validated_data):
        # print('create user with data: ', validated_data)
        user = User.objects.create_user(**validated_data)
        user.send_activation_code()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)