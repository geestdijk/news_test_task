from .models import NavigationLink

def template_renderer(request):
    return {
        'nav_links': NavigationLink.objects.filter(enabled=True).order_by("order"),
    }
