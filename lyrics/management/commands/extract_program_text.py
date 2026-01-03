"""
Management command to extract text from program image using OCR.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class Command(BaseCommand):
    help = 'Extract text from program image using OCR'

    def handle(self, *args, **options):
        if not OCR_AVAILABLE:
            self.stdout.write(
                self.style.ERROR(
                    'OCR libraries not available. Install with: pip install pytesseract Pillow'
                )
            )
            self.stdout.write(
                'Also install Tesseract OCR: https://github.com/tesseract-ocr/tesseract'
            )
            return

        # Path to program image
        static_images_dir = os.path.join(settings.BASE_DIR, 'lyrics', 'static', 'lyrics', 'images')
        program_image_path = None
        
        # Find program image
        if os.path.exists(static_images_dir):
            for filename in os.listdir(static_images_dir):
                filename_lower = filename.lower()
                if filename_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    if 'program origina' in filename_lower or 'program original' in filename_lower:
                        program_image_path = os.path.join(static_images_dir, filename)
                        break
        
        if not program_image_path or not os.path.exists(program_image_path):
            self.stdout.write(
                self.style.ERROR('Program image not found!')
            )
            return

        self.stdout.write(f'Extracting text from: {program_image_path}')
        
        try:
            # Open and process image
            image = Image.open(program_image_path)
            
            # Extract text using OCR
            self.stdout.write('Processing image with OCR...')
            extracted_text = pytesseract.image_to_string(image, lang='fra+eng')
            
            # Save extracted text to a JSON file
            output_file = os.path.join(settings.BASE_DIR, 'lyrics', 'static', 'lyrics', 'program_text.json')
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            data = {
                'text': extracted_text,
                'image_path': f'lyrics/images/{os.path.basename(program_image_path)}'
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.stdout.write(
                self.style.SUCCESS(f'Text extracted and saved to: {output_file}')
            )
            self.stdout.write(f'\nExtracted text preview:\n{extracted_text[:500]}...')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error extracting text: {str(e)}')
            )
            self.stdout.write(
                'Make sure Tesseract OCR is installed: https://github.com/tesseract-ocr/tesseract'
            )
