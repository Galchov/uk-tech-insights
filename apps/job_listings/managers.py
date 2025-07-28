from django.db import models


class JobPostQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    