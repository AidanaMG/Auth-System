from .models import AccessRule


def get_user_permission(user, element_name, action):
    
    if user is None or not user.is_authenticated or user.role is None:
        return "none"

    try:
        rule = AccessRule.objects.get(role=user.role, element__name=element_name)
    except AccessRule.DoesNotExist:
        return "none"  

    if action == "read":
        if rule.read_all_permission:
            return "all"
        if rule.read_permission:
            return "own"
        return "none"

    if action == "create":
        return "all" if rule.create_permission else "none"  

    if action == "update":
        if rule.update_all_permission:
            return "all"
        if rule.update_permission:
            return "own"
        return "none"

    if action == "delete":
        if rule.delete_all_permission:
            return "all"
        if rule.delete_permission:
            return "own"
        return "none"

    return "none"


def check_object_access(user, element_name, action, obj=None):
    
    permission = get_user_permission(user, element_name, action)

    if permission == "none":
        return False
    if permission == "all":
        return True
    if permission == "own":
        if obj is None:
            return True  
        return obj.owner_id == user.id

    return False