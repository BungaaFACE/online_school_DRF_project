from celery import shared_task
from datetime import datetime, timedelta

from users.models import User

@shared_task
def last_login_blocker():
    one_month_ago = datetime.now() - timedelta(days=30)
    
    for afk_user in User.objects.filter(
        last_login__lte=one_month_ago, is_active=True):
        
        afk_user.is_active = False
        afk_user.save()