"""
Models for the lyrics system.
"""
from django.db import models
from django.utils.text import slugify


class Song(models.Model):
    """
    Represents a song with a title and order in the setlist.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    order = models.IntegerField(default=0, help_text="Order in the setlist")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class LyricLine(models.Model):
    """
    Represents a single line of lyrics for a song.
    """
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='lines')
    order = models.IntegerField(help_text="Line order within the song")
    text = models.TextField()

    class Meta:
        ordering = ['song', 'order']
        unique_together = ['song', 'order']

    def __str__(self):
        return f"{self.song.title} - Line {self.order}"


class LiveState(models.Model):
    """
    Single-row model that stores the current live state.
    This is the "shared truth" that the projector reads and controller modifies.
    """
    active_song = models.ForeignKey(
        Song, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='live_states'
    )
    active_index = models.IntegerField(
        default=0,
        help_text="Current lyric line index (0-based)"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Live State"
        verbose_name_plural = "Live State"

    def __str__(self):
        if self.active_song:
            return f"Live: {self.active_song.title} (line {self.active_index})"
        return "No active song"

    @classmethod
    def get_current(cls):
        """
        Get or create the single LiveState instance.
        There should only ever be one row in this table.
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
