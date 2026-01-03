"""
Django admin configuration for lyrics app.
"""
from django.contrib import admin
from .models import Song, LyricLine, LiveState


class LyricLineInline(admin.TabularInline):
    """Inline editor for lyric lines within the Song admin."""
    model = LyricLine
    extra = 1
    ordering = ['order']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """Admin interface for songs."""
    list_display = ['title', 'order', 'slug', 'created_at']
    list_editable = ['order']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LyricLineInline]


@admin.register(LyricLine)
class LyricLineAdmin(admin.ModelAdmin):
    """Admin interface for lyric lines."""
    list_display = ['song', 'order', 'text_preview']
    list_filter = ['song']
    ordering = ['song', 'order']
    search_fields = ['text', 'song__title']

    def text_preview(self, obj):
        """Show a preview of the line text."""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'


@admin.register(LiveState)
class LiveStateAdmin(admin.ModelAdmin):
    """Admin interface for live state."""
    list_display = ['active_song', 'active_index', 'updated_at']
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        """Only allow one LiveState instance."""
        return not LiveState.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of LiveState."""
        return False
