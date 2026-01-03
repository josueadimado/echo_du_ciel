"""
Management command to import songs and lyrics from lyrics.md file.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from lyrics.models import Song, LyricLine
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Import songs and lyrics from lyrics.md file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='lyrics.md',
            help='Path to the lyrics markdown file (default: lyrics.md)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing songs before importing'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        # Get the base directory (project root)
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        lyrics_file = base_dir / file_path
        
        if not lyrics_file.exists():
            self.stdout.write(
                self.style.ERROR(f'File not found: {lyrics_file}')
            )
            return
        
        # Clear existing songs if requested
        if options['clear']:
            self.stdout.write('Clearing existing songs...')
            Song.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all songs'))
        
        # Read and parse the file
        self.stdout.write(f'Reading lyrics from {lyrics_file}...')
        
        with open(lyrics_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse songs
        songs_data = self.parse_lyrics_file(content)
        
        self.stdout.write(f'Found {len(songs_data)} songs')
        
        # Import songs
        imported_count = 0
        updated_count = 0
        
        for order, song_data in enumerate(songs_data, start=1):
            title = song_data['title']
            lines = song_data['lines']
            
            # Get or create song
            song, created = Song.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    'title': title,
                    'order': order
                }
            )
            
            if not created:
                # Update order if song already exists
                song.order = order
                song.save()
                updated_count += 1
            else:
                imported_count += 1
            
            # Clear existing lines and add new ones
            song.lines.all().delete()
            
            # Add lyric lines
            for line_order, line_text in enumerate(lines, start=0):
                if line_text.strip():  # Skip empty lines
                    LyricLine.objects.create(
                        song=song,
                        order=line_order,
                        text=line_text.strip()
                    )
            
            self.stdout.write(
                f'  {"Updated" if not created else "Imported"}: {title} ({len(lines)} lines)'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully imported {imported_count} new songs, '
                f'updated {updated_count} existing songs'
            )
        )

    def parse_lyrics_file(self, content):
        """
        Parse the lyrics.md file format.
        Songs are separated by multiple blank lines, with titles in all caps.
        """
        songs = []
        lines = content.split('\n')
        
        current_song = None
        current_lines = []
        blank_line_count = 0
        
        for line in lines:
            original_line = line
            line = line.rstrip()
            
            # Track consecutive blank lines
            if not line:
                blank_line_count += 1
                continue
            else:
                # If we had 2+ blank lines, we might be starting a new song
                if blank_line_count >= 2 and current_song:
                    # Save previous song
                    songs.append({
                        'title': current_song,
                        'lines': current_lines
                    })
                    current_song = None
                    current_lines = []
                blank_line_count = 0
            
            # Check if this line is a song title
            # Titles are: all uppercase, reasonable length, no leading spaces
            is_title = (
                line and
                line.isupper() and
                len(line.split()) <= 15 and  # Reasonable title length
                not line.startswith(' ') and
                not line.startswith('(') and  # Not a parenthetical note
                current_song is None  # We're not already in a song
            )
            
            if is_title:
                # Start new song
                current_song = line
                current_lines = []
            elif current_song:
                # Add line to current song (even if it's empty, we'll filter later)
                current_lines.append(original_line)
        
        # Don't forget the last song
        if current_song:
            songs.append({
                'title': current_song,
                'lines': current_lines
            })
        
        return songs
