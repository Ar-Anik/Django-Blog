from notification.models import Notification

def user_notification(request):
    context = {}

    if request.user.is_authenticated:
        notification = Notification.objects.filter(
            user = request.user
        ).order_by('-created_date')

        unseen = notification.exclude(is_seen=True)

        context['notifications'] = notification
        context['unseen'] = unseen.count()

    return context
