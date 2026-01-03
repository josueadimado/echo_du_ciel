# Louange Echo - Concert Lyrics System

A Django-based web application for displaying concert lyrics on phones (via QR code) and projector screens, with a controller interface for live management.

## Features

- **QR Code Access**: Audience scans QR code to view setlist and full lyrics on their phones
- **Projector Screen**: Large-screen display that auto-updates with current lyrics
- **Live Control**: Operator can select songs and advance lyrics in real-time
- **Simple Polling**: Uses HTTP polling (no WebSockets) for reliability

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Import Lyrics

Import songs from your `lyrics.md` file:

```bash
python manage.py import_lyrics
```

Or to clear existing songs and re-import:

```bash
python manage.py import_lyrics --clear
```

### 4. Run Development Server

```bash
python manage.py runserver
```

## Usage

### For Audience (QR Code)
- Point QR code to: `http://your-domain.com/`
- Users see setlist and can tap songs to view full lyrics
- **Generate QR Code**: Use any QR code generator (e.g., qr-code-generator.com) and point it to your domain root URL

### For Projector Screen
- Open: `http://your-domain.com/screen/`
- Displays current lyrics in large text, auto-updates every 800ms
- Press F11 for full-screen mode

### For Controller/Operator
- Open: `http://your-domain.com/control/`
- Select a song and click "Go Live"
- Use "Next" and "Previous" buttons to advance lyrics

## Deployment to PythonAnywhere

1. **Upload your project** to PythonAnywhere
2. **Create a Web App** in the Web tab
3. **Set up virtual environment** and install dependencies:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
4. **Configure WSGI file** to point to `louange_echo.wsgi.application`
5. **Run migrations**:
   ```bash
   python3.10 manage.py migrate
   ```
6. **Create superuser**:
   ```bash
   python3.10 manage.py createsuperuser
   ```
7. **Import lyrics**:
   ```bash
   python3.10 manage.py import_lyrics
   ```
8. **Reload your web app**

## Project Structure

```
louange_echo/
├── lyrics/              # Main app
│   ├── models.py       # Song, LyricLine, LiveState models
│   ├── views.py        # All views (setlist, screen, control, API)
│   ├── urls.py         # URL routing
│   ├── admin.py        # Django admin configuration
│   └── templates/      # HTML templates
├── louange_echo/       # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── lyrics.md           # Source lyrics file
├── manage.py
└── requirements.txt
```

## API Endpoints

- `GET /api/state/` - Returns current live state as JSON
- `POST /control/set-song/<id>/` - Set active song
- `POST /control/next/` - Advance to next line
- `POST /control/prev/` - Go back to previous line

## Admin Interface

Access at `/admin/` to:
- Add/edit songs and lyrics
- Manage setlist order
- View live state

## Notes

- The system uses simple HTTP polling (800ms interval) for screen updates
- LiveState is a single-row model that stores the current state
- All lyrics are stored in the database for fast access
- Mobile-friendly templates for audience viewing

## License

This project is for internal use.
