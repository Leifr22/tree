from django.db import models
from django.urls import reverse, NoReverseMatch

class MenuItem(models.Model):
    menu = models.CharField(
        max_length=100,
        help_text="Group name for this menu (e.g. 'main_menu')."
    )
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    url = models.CharField(
        max_length=200,
        blank=True,
        help_text="Absolute URL, e.g. '/about/'"
    )
    named_url = models.CharField(
        max_length=200,
        blank=True,
        help_text="Django named URL, e.g. 'app:detail'"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Position among siblings"
    )

    class Meta:
        ordering = ['order']
        unique_together = [('menu', 'parent', 'order')]

    def __str__(self):
        return f"[{self.menu}] {self.title}"

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return self.url or '#'