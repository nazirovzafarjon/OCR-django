# OCR Django App

A simple web application that extracts text from images using Optical Character Recognition (OCR). Upload an image through the browser and get the recognized text back instantly.

## Features

- **Image-to-text extraction** — upload any image (JPEG, PNG, etc.) and extract the text it contains.
- **REST API endpoint** (`/api/ocr/`) for programmatic OCR requests, built with Django REST Framework.
- **Simple web UI** — a single-page form (`/`) for uploading an image and viewing the extracted text without leaving the page (via `fetch`/AJAX).
- **Automatic cleanup** — uploaded images are stored temporarily and deleted from disk after processing.
- **Styled with Tailwind CSS** for a clean, responsive interface.

## Technologies Used

- **[Django](https://www.djangoproject.com/)** — backend web framework.
- **[Django REST Framework](https://www.django-rest-framework.org/)** — powers the `/api/ocr/` endpoint.
- **[EasyOCR](https://github.com/JaidedAI/EasyOCR)** — deep learning–based OCR engine (built on PyTorch) used to read text from images.
- **[Pillow](https://python-pillow.org/)** — image handling.
- **[django-tailwind](https://django-tailwind.readthedocs.io/)** — Tailwind CSS integration for styling.
- **SQLite** — default database.

## Project Structure

```
ocr_project/      # Django project settings, root URLs
ocr_app/          # Main app: views, OCR logic, API endpoint
  ocr.py          # EasyOCR wrapper that extracts text from an image path
  views.py        # index view + OCRAPIView (DRF APIView) handling uploads
theme/            # Tailwind app (styles)
template/         # HTML templates (index.html with upload form)
```

## How It Works

1. The user selects an image on the homepage (`index.html`) and submits the form.
2. JavaScript sends the image via `fetch` to the `POST /api/ocr/` endpoint as `multipart/form-data`.
3. `OCRAPIView` saves the file temporarily, passes its path to `extract_text_from_image` (in `ocr_app/ocr.py`), which uses EasyOCR's `Reader` to read the text.
4. The extracted text is returned as JSON and displayed on the page.
5. The temporary file is deleted after processing, regardless of success or failure.

## Setup & Installation

1. **Clone the repository** and navigate into the project folder.

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Build Tailwind CSS** (optional, only if you change styles):
   ```bash
   python manage.py tailwind start
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. Open `http://127.0.0.1:8000/` in your browser, upload an image, and view the extracted text.

## API Usage

**Endpoint:** `POST /api/ocr/`

**Request:** `multipart/form-data` with a single field `image` containing the image file.

**Example with `curl`:**
```bash
curl -X POST http://127.0.0.1:8000/api/ocr/ \
  -F "image=@/path/to/your/image.png"
```

**Successful response:**
```json
{ "text": "Extracted text from the image" }
```

**Error response:**
```json
{ "error": "No image provided" }
```

## Notes

- EasyOCR currently loads only the English (`en`) language model. Add more languages by editing the `Reader` initialization in `ocr_app/ocr.py`.
- This project uses `DEBUG = True` and a sample `SECRET_KEY` for local development only — do not use these settings in production.
