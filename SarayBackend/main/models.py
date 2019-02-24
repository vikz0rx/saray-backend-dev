from django.db import models
from django.utils.translation import ugettext_lazy as _

class News(models.Model):
    title = models.CharField(_('title'), max_length=128)
    text = models.TextField(_('text'), max_length=4096)
    image = models.FileField(_('image'), upload_to='news')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('news')