from django.db import models


# Create your models here.
class AppUser(models.Model):
    app_openid = models.CharField(primary_key=True, max_length=128)
    user_id = models.PositiveIntegerField(unique=True)
    nickname = models.CharField(max_length=128)
    bind_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'happytea_wxapp_user_list'
