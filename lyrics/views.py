"""
Views for the lyrics system.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Song, LiveState
import os


def setlist_view(request):
    """
    Home page showing the setlist (list of all songs).
    This is what the QR code should point to.
    """
    # Optimized: Cache image detection to avoid scanning on every request
    import os
    from django.core.cache import cache
    from django.conf import settings
    
    # Cache key for image paths
    cache_key = 'setlist_images'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        # Find available images from the choir (only if not cached)
        static_images_dir = os.path.join(settings.BASE_DIR, 'lyrics', 'static', 'lyrics', 'images')
        
        # Get all image files
        available_images = []
        program_image = None
        
        if os.path.exists(static_images_dir):
            # Priority: look for the specific program image first
            program_keywords = [
                'program origina',  # Specific program image
                'program original',
                'whatsapp image 2026-01-02 at 11.31.38',  # Specific program image
                'program', 'programme', 'poster', 'affiche', 
                'ft', 'gtt', 'gsrz', 'fghft'
            ]
            
            # First pass: look for specific program image or keywords
            for filename in os.listdir(static_images_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    full_path = f'lyrics/images/{filename}'
                    available_images.append(full_path)
                    
                    filename_lower = filename.lower()
                    # Check for specific program image first
                    if 'program origina' in filename_lower or 'program original' in filename_lower:
                        program_image = full_path
                    elif not program_image and 'whatsapp image 2026-01-02 at 11.31.38' in filename_lower:
                        program_image = full_path
                    elif not program_image and any(keyword in filename_lower for keyword in program_keywords[3:]):
                        program_image = full_path
            
            # Second pass: if no program found, use first non-large image or skip size check
            if not program_image and available_images:
                # Skip large images (likely photos) - prefer smaller ones
                # Just use the first image that's not obviously a photo
                for img_path in available_images:
                    filename = os.path.basename(img_path).lower()
                    # Skip obvious photo filenames
                    if not any(photo_indicator in filename for photo_indicator in ['dsc_', 'photo', 'img_']):
                        program_image = img_path
                        break
                # If still no program image, just use the first one
                if not program_image:
                    program_image = available_images[0]
            
            # Cache for 1 hour (3600 seconds)
            cached_data = {
                'available_images': available_images,
                'program_image': program_image
            }
            cache.set(cache_key, cached_data, 3600)
        else:
            cached_data = {'available_images': [], 'program_image': None}
    
    available_images = cached_data['available_images']
    program_image = cached_data['program_image']
    
    # Use a different image as hero background (not the program)
    # Include all images - lazy loading in template will handle large files
    hero_image = None
    for img in available_images:
        if img != program_image:
            hero_image = img
            break
    
    # Gallery: exclude program and hero images
    gallery_images = [img for img in available_images if img != hero_image and img != program_image][:4]
    
    # Slider images: exclude program image (include all others, even large ones)
    # Lazy loading in template will handle the large files efficiently
    slider_images = [img for img in available_images if img != program_image]
    
    # Get the full URL for QR code generation (will be done client-side)
    # QR code should point to the songs list page
    from django.urls import reverse
    request_scheme = request.scheme
    request_host = request.get_host()
    page_url = f"{request_scheme}://{request_host}{reverse('songs_list')}"
    
    # Partners/Sponsors list - names of people and organizations that supported the concert
    # Format: {'name': 'Name', 'role': 'Role/Activity'}
    partners = [
        {
            'name': 'MR ADIMADO KOSSI AIMÉ',
            'role': 'Directeur ECADIF SARL U Spécialisé dans la vente de motos et pièces détachées d\'Evame et Apsonic'
        },
        {
            'name': 'MR MAGLOIRE',
            'role': 'Directeur Evame Togo'
        },
        {
            'name': 'MR AFOUTOU KOMI',
            'role': 'Directeur Commercial ECADIF SARL U'
        },
        {
            'name': 'ADIMADO KODZO JOSUE',
            'role': 'Responsable IT & Gestion des Stocks, ECADIF Sarl U · Fondateur, The Creative Branders Ltd'
        },
        {
            'name': 'ADIMADO MAKAFUI',
            'role': 'Auditeur Interne à ECADIF SARL U'
        },
        {
            'name': 'AFFO CEDRIC',
            'role': 'Auditeur à GCAS'
        },
        {
            'name': 'AFOUTOU AKOUVI',
            'role': 'Couturière'
        },
        {
            'name': 'AHAMA SOKÉ',
            'role': ''
        },
        {
            'name': 'AHAMA LUCRÈCE',
            'role': 'Couturière'
        },
        {
            'name': 'KPETEMEY KOKOUVI PEDRO',
            'role': 'Auditeur Spécialité Fiscalité Comptabilité'
        },
        {
            'name': 'AMEDJODEKA ELOM',
            'role': 'Responsable RH PAM Togo'
        },
        {
            'name': 'ATIVI EMMANUEL',
            'role': 'Responsable Qualité · Directeur du cabinet'
        },
        {
            'name': 'ADAMA OLIVIA',
            'role': ''
        },
        {
            'name': 'AGBENOWOKO KOMI',
            'role': 'Transitaire'
        },
        {
            'name': 'MALONNUI ADJOVI',
            'role': 'Revendeuse de pagnes au grand marché'
        },
        {
            'name': 'MME AMEY BODIVIANE',
            'role': 'Responsable RH'
        },
        {
            'name': 'AFOGNON BONAVENTURE',
            'role': 'Menuisier'
        },
        {
            'name': 'ADOH ÉLODIE',
            'role': ''
        },
        {
            'name': 'MR ADODOKPO DOMINIQUE',
            'role': 'Transitaire à Lomé'
        },
        {
            'name': 'MME ADODOKPO CHRISTIANE',
            'role': 'Grande Commerçante à Lomé'
        },
        {
            'name': 'SR EKOÉ SITSOFE',
            'role': ''
        },
        {
            'name': 'SR EKOÉ ESSI',
            'role': ''
        },
        {
            'name': 'MR EKOÉ AMÉLI',
            'role': ''
        },
        {
            'name': 'MR ADAMA HENOC',
            'role': ''
        },
        {
            'name': 'MR AHLIN MICHEL',
            'role': 'Carreleur à Lomé'
        },
        {
            'name': 'WOTONEGNON VICTOIRE',
            'role': ''
        },
        {
            'name': 'FR FREDDY',
            'role': ''
        },
        {
            'name': 'MME AGBASSAGBÉ DÉDÉ',
            'role': ''
        },
        {
            'name': 'MR AGBASSAGBÉ EMMANUEL',
            'role': ''
        },
        {
            'name': 'MR AKAKPO AMAH',
            'role': ''
        },
        {
            'name': 'FAMILLE LAWSON',
            'role': ''
        },
        {
            'name': 'MR AFOUTOU KOMLAN',
            'role': 'Directeur Logistique & Transport à ECADIF SARL U'
        },
        {
            'name': 'FAMILLE HOUESSOU',
            'role': ''
        },
        {
            'name': 'MANOTTI',
            'role': ''
        },
        {
            'name': 'DAVID FATCHAO',
            'role': 'Commerçant au grand marché de Lomé'
        },
        {
            'name': 'HOUESSOU CHRISTINE',
            'role': ''
        },
    ]
    
    return render(request, 'lyrics/setlist.html', {
        'hero_image': hero_image,
        'program_image': program_image,
        'gallery_images': gallery_images,
        'slider_images': slider_images,
        'page_url': page_url,
        'partners': partners
    })


def songs_list_view(request):
    """
    Page displaying the list of all songs with links to lyrics.
    """
    songs = Song.objects.all()
    return render(request, 'lyrics/songs_list.html', {
        'songs': songs
    })


def song_detail_view(request, slug):
    """
    Full lyrics page for a specific song (mobile-friendly).
    """
    song = get_object_or_404(Song, slug=slug)
    lines = song.lines.all()
    return render(request, 'lyrics/song_detail.html', {
        'song': song,
        'lines': lines
    })


def program_view(request):
    """
    Display the concert program (poster/image).
    """
    import os
    import json
    from django.core.cache import cache
    from django.conf import settings
    from django.http import Http404
    
    # Use cached image data from setlist_view
    cache_key = 'setlist_images'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        program_image = cached_data.get('program_image')
    else:
        # Fallback: quick scan if cache miss
        static_images_dir = os.path.join(settings.BASE_DIR, 'lyrics', 'static', 'lyrics', 'images')
        program_image = None
        
        if os.path.exists(static_images_dir):
            # Quick scan for program image
            for filename in os.listdir(static_images_dir):
                filename_lower = filename.lower()
                if filename_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    if 'program origina' in filename_lower or 'program original' in filename_lower:
                        program_image = f'lyrics/images/{filename}'
                        break
                    elif 'whatsapp image 2026-01-02 at 11.31.38' in filename_lower:
                        program_image = f'lyrics/images/{filename}'
                        break
    
    program_text = None
    
    # Try to load extracted text
    program_text_file = os.path.join(settings.BASE_DIR, 'lyrics', 'static', 'lyrics', 'program_text.json')
    program_text_lines = None
    if os.path.exists(program_text_file):
        try:
            with open(program_text_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                program_text = data.get('text', '')
                # Split text into lines for better formatting
                if program_text:
                    program_text_lines = program_text.split('\n')
        except (json.JSONDecodeError, IOError, Exception) as e:
            # Silently fail if text file can't be read
            program_text = None
            program_text_lines = None
    
    if not program_image:
        raise Http404("Programme non trouvé")
    
    return render(request, 'lyrics/program.html', {
        'program_image': program_image,
        'program_text': program_text,
        'program_text_lines': program_text_lines
    })


def download_program_view(request):
    """
    Download the concert program image.
    """
    from django.conf import settings
    
    static_images_dir = os.path.join(settings.BASE_DIR, 'lyrics', 'static', 'lyrics', 'images')
    program_file = None
    
    if os.path.exists(static_images_dir):
        # Look for the specific program image first
        for filename in os.listdir(static_images_dir):
            filename_lower = filename.lower()
            if filename_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # Check for specific program image - priority to "Program Origina"
                if 'program origina' in filename_lower or 'program original' in filename_lower:
                    program_file = os.path.join(static_images_dir, filename)
                    break
                elif 'whatsapp image 2026-01-02 at 11.31.38' in filename_lower:
                    program_file = os.path.join(static_images_dir, filename)
                    break
        
        # If not found, try other keywords
        if not program_file:
            program_keywords = ['program', 'programme', 'poster', 'affiche', 'ft', 'gtt', 'gsrz', 'fghft']
            for filename in os.listdir(static_images_dir):
                filename_lower = filename.lower()
                if filename_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    if any(keyword in filename_lower for keyword in program_keywords):
                        program_file = os.path.join(static_images_dir, filename)
                        break
        
        # If still not found, use largest file
        if not program_file:
            try:
                image_files = []
                for filename in os.listdir(static_images_dir):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        img_file = os.path.join(static_images_dir, filename)
                        if os.path.exists(img_file):
                            size = os.path.getsize(img_file)
                            image_files.append((size, img_file))
                if image_files:
                    image_files.sort(reverse=True)
                    program_file = image_files[0][1]
            except:
                pass
    
    if not program_file or not os.path.exists(program_file):
        raise Http404("Programme non trouvé")
    
    # Determine content type based on file extension
    filename = os.path.basename(program_file)
    if filename.lower().endswith('.png'):
        content_type = 'image/png'
    elif filename.lower().endswith('.gif'):
        content_type = 'image/gif'
    else:
        content_type = 'image/jpeg'
    
    response = FileResponse(
        open(program_file, 'rb'),
        content_type=content_type
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def screen_view(request):
    """
    Projector screen view - displays current lyrics in large text.
    Auto-refreshes via polling.
    """
    return render(request, 'lyrics/screen.html')


def control_view(request):
    """
    Controller page - allows operator to select songs and advance lyrics.
    """
    songs = Song.objects.all()
    live_state = LiveState.get_current()
    return render(request, 'lyrics/control.html', {
        'songs': songs,
        'live_state': live_state
    })


@require_http_methods(["GET"])
def api_state_view(request):
    """
    API endpoint that returns the current live state as JSON.
    Polled by the projector screen every ~800ms.
    """
    live_state = LiveState.get_current()
    
    if not live_state.active_song:
        return JsonResponse({
            'active': False,
            'song': None,
            'index': 0,
            'start': 0,
            'lines': [],
            'total': 0,
            'updated_at': live_state.updated_at.isoformat()
        })
    
    song = live_state.active_song
    all_lines = list(song.lines.all())
    
    # Split long lines into multiple slides (max ~80 characters per slide)
    MAX_CHARS_PER_SLIDE = 80
    
    def split_long_line(line, max_chars=MAX_CHARS_PER_SLIDE):
        """Split a long line into multiple parts for better display."""
        line = line.strip()
        if not line:
            return [""]
        if len(line) <= max_chars:
            return [line]
        
        # Try to split at natural break points (commas, spaces, etc.)
        parts = []
        current_part = ""
        
        # Split by common separators first
        segments = line.replace(',', ' ,').replace('.', ' .').replace(';', ' ;').split()
        
        for segment in segments:
            if len(current_part) + len(segment) + 1 <= max_chars:
                current_part += (" " if current_part else "") + segment
            else:
                if current_part:
                    parts.append(current_part.strip())
                current_part = segment
        
        if current_part:
            parts.append(current_part.strip())
        
        # If still too long, force split
        if not parts or any(len(p) > max_chars * 1.5 for p in parts):
            parts = []
            for i in range(0, len(line), max_chars):
                parts.append(line[i:i+max_chars].strip())
        
        return parts
    
    # Expand all lines into virtual slides (long lines become multiple slides)
    virtual_slides = []
    line_to_slide_mapping = {}  # Maps virtual slide index to original line index
    
    for line_idx, line_obj in enumerate(all_lines):
        line_text = line_obj.text.strip()
        if not line_text:
            # Empty line becomes one empty slide
            virtual_slides.append("")
            line_to_slide_mapping[len(virtual_slides) - 1] = line_idx
        else:
            # Split long lines into multiple slides
            parts = split_long_line(line_text, MAX_CHARS_PER_SLIDE)
            for part in parts:
                virtual_slides.append(part)
                line_to_slide_mapping[len(virtual_slides) - 1] = line_idx
    
    total_virtual_slides = len(virtual_slides)
    total_original_lines = len(all_lines)
    
    # Use the active_index as the virtual slide index
    current_virtual_index = live_state.active_index
    
    # Ensure index is within bounds
    if current_virtual_index < 0:
        current_virtual_index = 0
    if current_virtual_index >= total_virtual_slides:
        current_virtual_index = max(0, total_virtual_slides - 1)
    
    # Get the current slide
    current_slide = virtual_slides[current_virtual_index] if current_virtual_index < total_virtual_slides else ""
    
    # Get the next slide if available (for preview)
    next_slide = ""
    if current_virtual_index + 1 < total_virtual_slides:
        next_slide = virtual_slides[current_virtual_index + 1]
    
    # Build window lines
    window_lines = []
    if current_slide.strip():
        window_lines.append(current_slide)
    if next_slide.strip():
        window_lines.append(next_slide)
    
    # Find which original line this virtual slide belongs to
    original_line_index = line_to_slide_mapping.get(current_virtual_index, 0)
    
    current_line_index_in_window = 0
    
    return JsonResponse({
        'active': True,
        'song': {
            'title': song.title,
            'slug': song.slug
        },
        'index': current_virtual_index,  # Virtual slide index
        'original_line_index': original_line_index,  # Original line index
        'lines': window_lines,
        'current_line_index': current_line_index_in_window,
        'total': total_virtual_slides,  # Total virtual slides
        'total_original_lines': total_original_lines,  # Total original lines
        'updated_at': live_state.updated_at.isoformat()
    })


@require_http_methods(["POST"])
@csrf_exempt  # For simplicity in MVP - consider adding proper auth later
def control_set_song_view(request, song_id):
    """
    Set the active song and reset index to 0.
    """
    song = get_object_or_404(Song, pk=song_id)
    live_state = LiveState.get_current()
    live_state.active_song = song
    live_state.active_index = 0
    live_state.save()
    
    return JsonResponse({'success': True, 'message': f'Chant "{song.title}" mis en direct'})


@require_http_methods(["POST"])
@csrf_exempt
def control_next_view(request):
    """
    Advance to the next line.
    """
    live_state = LiveState.get_current()
    
    if not live_state.active_song:
        return JsonResponse({'success': False, 'message': 'Aucun chant actif'}, status=400)
    
    # Calculate total virtual slides (with long lines split)
    all_lines = list(live_state.active_song.lines.all())
    MAX_CHARS_PER_SLIDE = 80
    
    def count_slides(line_text):
        """Count how many virtual slides a line will create."""
        line_text = line_text.strip()
        if not line_text:
            return 1
        if len(line_text) <= MAX_CHARS_PER_SLIDE:
            return 1
        # Estimate: divide by max chars
        return max(1, (len(line_text) + MAX_CHARS_PER_SLIDE - 1) // MAX_CHARS_PER_SLIDE)
    
    total_virtual_slides = sum(count_slides(line.text) for line in all_lines)
    
    if live_state.active_index < total_virtual_slides - 1:
        live_state.active_index += 1
        live_state.save()
        return JsonResponse({'success': True, 'index': live_state.active_index})
    
    return JsonResponse({'success': False, 'message': 'Déjà à la dernière ligne'})


@require_http_methods(["GET"])
def api_song_lyrics_view(request, song_id):
    """
    API endpoint that returns all lyrics lines for a song.
    """
    song = get_object_or_404(Song, pk=song_id)
    lines = song.lines.all()
    
    return JsonResponse({
        'song': {
            'id': song.id,
            'title': song.title,
            'slug': song.slug
        },
        'lines': [{'order': line.order, 'text': line.text} for line in lines],
        'total': lines.count()
    })


@require_http_methods(["POST"])
@csrf_exempt
def control_prev_view(request):
    """
    Go back to the previous slide (virtual slide, so long lines are split).
    """
    live_state = LiveState.get_current()
    
    if not live_state.active_song:
        return JsonResponse({'success': False, 'message': 'Aucun chant actif'}, status=400)
    
    if live_state.active_index > 0:
        live_state.active_index -= 1
        live_state.save()
        return JsonResponse({'success': True, 'index': live_state.active_index})
    
    return JsonResponse({'success': False, 'message': 'Déjà à la première ligne'})
