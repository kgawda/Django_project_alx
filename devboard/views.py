from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView

from devboard.forms import ProjectForm, TaskForm
from devboard.mixins import OwnerQuerysetMixin
from devboard.models import Project, Task


# def index(request):
#     return HttpResponse("<h1>DevBoard - etap 1: scaffold!</h1>")

# def index(request):
#     return render(request, "index.html")

class ProjectListView(OwnerQuerysetMixin, ListView):
    model = Project
    template_name = "devboard/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return (
            super().get_queryset()
            .annotate(task_count=Count("tasks"))
            .order_by("-created_at")
        )

class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    model = Project
    template_name = "devboard/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tasks"] = (
            self.object.tasks
            .select_related("assignee")
            .order_by("-priority", "due_date")
        )
        return ctx

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "devboard/project_create.html"
    form_class = ProjectForm
    success_url = reverse_lazy("devboard:lista-project")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f"Projekt '{form.instance.name}' został utworzony.")
        return super().form_valid(form)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "devboard/task_create.html"
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("devboard:project-detail", args=[self.object.project.id])

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get("project")
        if project_id:
            initial["project"] = project_id
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["project"].queryset = Project.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, f"Zadanie '{form.instance.title}' zostało dodane.")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "devboard/task_create.html"
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("devboard:project-detail", args=[self.object.project.id])

    # TODO ...


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "devboard/task_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("devboard:project-detail", args=[self.object.project.id])
