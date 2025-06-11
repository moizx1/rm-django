from rest_framework import serializers
from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        many = True,
        slug_field = 'name',
        queryset = Role.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'CNIC', 'DOB', 'address', 'roles']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        roles_data = validated_data.pop('roles')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user.roles.set(roles_data)
        return user
