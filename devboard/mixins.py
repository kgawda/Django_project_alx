from django.contrib.auth.mixins import LoginRequiredMixin

class OwnerQuerysetMixin(LoginRequiredMixin):
    owner_field = "owner"
    def get_queryset(self):
        return super().get_queryset().filter(**{self.owner_field: self.request.user})