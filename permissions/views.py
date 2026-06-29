from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import AccessRule
from .serializers import AccessRuleSerializer
from .checker import get_user_permission


def is_admin(request):
    user = request._request.jwt_user
    if not user:
        return False
    permission = get_user_permission(user, "access_rules", "read")
    return permission == "all"


@method_decorator(csrf_exempt, name="dispatch")
class AccessRuleListView(APIView):
    def get(self, request):
        if not is_admin(request):
            return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)
        rules = AccessRule.objects.select_related("role", "element").all()
        return Response(AccessRuleSerializer(rules, many=True).data)

    def post(self, request):
        if not is_admin(request):
            return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)
        serializer = AccessRuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name="dispatch")
class AccessRuleDetailView(APIView):
    def get_object(self, pk):
        try:
            return AccessRule.objects.get(pk=pk)
        except AccessRule.DoesNotExist:
            return None

    def put(self, request, pk):
        if not is_admin(request):
            return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)
        rule = self.get_object(pk)
        if rule is None:
            return Response({"detail": "Не найдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AccessRuleSerializer(rule, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)