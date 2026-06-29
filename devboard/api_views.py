from rest_framework import viewsets, permissions
from devboard.serializers import CommentSerializer
from devboard.models import Comment, Task
from devboard.serializers import TaskSerializer


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).select_related("author","task")


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            project__owner=self.request.user
        ).select_related("project", "assignee")