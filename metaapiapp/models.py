from django.db import models

# Create your models here.


class pagePost(models.Model):
    page_post_id = models.CharField(max_length=100,null=True,blank=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    class meta:
        db_table = 'page_post'