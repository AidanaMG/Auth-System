from rest_framework import serializers
from .models import Role, BusinessElement, AccessRule


class AccessRuleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)
    element_name = serializers.CharField(source="element.name", read_only=True)

    class Meta:
        model = AccessRule
        fields = [
            "id", "role", "role_name", "element", "element_name",
            "read_permission", "read_all_permission",
            "create_permission",
            "update_permission", "update_all_permission",
            "delete_permission", "delete_all_permission",
        ]