from django.urls import path
from .views import AccessRuleListView, AccessRuleDetailView

urlpatterns = [
    path("access-rules/", AccessRuleListView.as_view()),
    path("access-rules/<int:pk>/", AccessRuleDetailView.as_view()),
]