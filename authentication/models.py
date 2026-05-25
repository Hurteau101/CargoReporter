from django.db import models

class AllowedEmail(models.Model):
    email = models.EmailField()

    class Meta:
        db_table = 'allowed_email'
        verbose_name_plural = 'Allowed Emails'

    def __str__(self):
        return self.email