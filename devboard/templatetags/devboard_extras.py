from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def status_badge(task):
    color_types = {
        "TODO": "dark",
        "IN_PROGRESS": "info",
        "DONE": "success",
    }
    icons = {
        "TODO": "circle",
        "IN_PROGRESS": "hourglass-split",
        "DONE": "check-circle",
    }
    return format_html(
        """
        <span class="badge bg-{}">
            <i class="bi bi-{}"></i> {}
        </span>
        """.format(
            color_types[task.status],
            icons[task.status],
            task.get_status_display(),
        )
    )