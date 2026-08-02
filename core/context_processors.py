from .models import Announcement

def global_context(request):
    """
    Context processor to provide global site variables across all templates.
    """
    announcements = Announcement.objects.filter(is_active=True)[:3]
    return {
        'site_announcements': announcements,
        'app_name': 'Algebrify'
    }
