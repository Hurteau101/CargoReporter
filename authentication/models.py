from django.db import models


# Which emails are allowed to access the website. Used by the custom adapter.
class AllowedEmail(models.Model):
    email = models.EmailField()

    class Meta:
        db_table = 'allowed_email'
        verbose_name_plural = 'Allowed Emails'

    def __str__(self):
        return self.email