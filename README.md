# DermaAI - AI-Powered Dermatological Analysis System

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![ML](https://img.shields.io/badge/AI-Machine%20Learning-FF6F00?logo=pytorch&logoColor=white)](https://huggingface.co/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**DermaAI** is a full-featured web platform built with **Django** that combines **AI-powered skin disease detection** with a complete healthcare management ecosystem. Patients can upload photos of skin conditions for instant AI classification, while doctors, hospitals, and ambulance services manage appointments, prescriptions, payments, and emergency response through dedicated portals.

> Disclaimer: DermaAI provides AI-assisted analysis for educational and decision-support purposes only. It is not a medical device and does not replace professional medical advice, diagnosis, or treatment.

---

## Table of Contents

- [Key Features](#key-features)
- [AI Skin Disease Detection](#ai-skin-disease-detection)
- [Role-Based Modules](#role-based-modules)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [Key Endpoints](#key-endpoints)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Key Features

- **AI Skin Disease Detection:** Upload a skin lesion image and get an instant classification across 31 skin conditions using a fine-tuned vision transformer.
- **Confidence Thresholding:** Predictions below a confidence threshold are rejected instead of giving false reassurance.
- **High-Severity Alerts:** High-risk conditions (e.g. melanoma, squamous & basal cell carcinoma) trigger an urgent consult warning.
- **Home Remedies & Medicine Search:** For non-severe conditions, curated home remedy and medicine info is fetched via the SerpAPI Google Search integration.
- **Product Recommendations:** Personalized and recommended skincare products based on the detected condition.
- **Patient Portal:** Profile management, appointment booking, viewing prescriptions, tests, reports, feedback, and complaints.
- **Doctor Portal:** Manage appointments, write prescriptions, record tests, publish availability, view patient history, and chat with patients.
- **Hospital Portal:** Hospital registration with admin approval, ambulance management, patient transfer, emergency mapping, and inter-hospital chat.
- **Ambulance Services:** Registration, approval workflow, patient assignment, and live confirmation tracking.
- **Appointments & Payments:** Book, reschedule, and cancel appointments; track consultation fee payments.
- **Video Conferencing:** Schedule and join video consultations.
- **Real-Time Chat:** Messaging between patients, doctors, hospitals, and ambulance units.
- **Emergency Map:** Hospitals broadcast emergencies with GPS coordinates rendered on a map view.

---

## AI Skin Disease Detection

The AI pipeline is the core of DermaAI:

1. The user uploads an image of a skin condition.
2. The image is preprocessed and passed through the fine-tuned vision transformer model.
3. A softmax probability is computed; the top class is reported with its confidence score.
4. If confidence falls below the threshold, the request is rejected with a clear message.
5. If the detected class is flagged as high severity, an urgent-care alert is returned.
6. Otherwise, home remedy and medicine information is fetched and returned alongside the prediction.

| Component | Detail |
| --- | --- |
| Base model | DINOv2 (fine-tuned for skin disease classification) |
| Model source | `Jayanth2002/dinov2-base-finetuned-SkinDisease` (Hugging Face) |
| Classes | 31 skin conditions (melanoma, psoriasis, eczema, leprosy variants, tinea, etc.) |
| Confidence threshold | `0.60` |
| High-severity classes | Melanoma, Squamous Cell Carcinoma, Basal Cell Carcinoma |
| Inference | PyTorch, `AutoModelForImageClassification` |

On first run the model weights and tokenizer are downloaded automatically into `hf_cache_v2/` (git-ignored), so the repository stays lightweight.

---

## Role-Based Modules

```
                        DermaAI Platform
        ┌──────────┬──────────┬───────────┬──────────┐
        │  Admin   │ Patient  │  Doctor   │ Hospital │
        └──────────┴──────────┴───────────┴──────────┘
```

- **Admin:** Approve/reject doctor, hospital, and ambulance registrations; manage users, complaints, and hospitals; oversee the platform.
- **Patient:** Register, book appointments, upload skin images for AI analysis, view prescriptions/tests/reports, chat, send feedback and complaints.
- **Doctor:** Accept appointments, write/edit/delete prescriptions, run and view tests, manage availability, review patient history, video consult, chat.
- **Hospital / Ambulance:** Register and get approved, manage ambulances, assign/transfer patients, broadcast emergencies with map location, communicate across units.

---

## Tech Stack

- **Backend:** Python 3.9+, Django 5.0, Django REST Framework
- **Database:** SQLite3 (development) / PostgreSQL (production)
- **AI/ML:** PyTorch, Hugging Face Transformers, Keras/TensorFlow
- **Async Tasks:** Celery + Celery Beat
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap, Django templates
- **Integrations:** SerpAPI (Google Search for remedies/medicines/products), OpenCV, Geopy

---

## Getting Started

### Prerequisites

- [Python 3.9+](https://www.python.org/)
- [Git](https://git-scm.com/)
- [SerpAPI key](https://serpapi.com/) (optional, required for remedy/medicine/product search)

### Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/gokulblee-code/Derma-Ai.git
   cd Derma-Ai
   ```

2. **Create and activate a virtual environment**

   Windows:

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

   macOS / Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

> The first AI prediction will download the model weights (~model size) into `hf_cache_v2/`. A stable internet connection is required on first use.

---

## Project Structure

```text
Derma-Ai/
├── DermaAI/                 # Django project configuration
│   ├── settings.py          # Settings, database, static files, keys
│   ├── urls.py              # Root URL routing
│   ├── wsgi.py / asgi.py    # Deployment entry points
│   └── __init__.py
├── DermaAIapp/              # Core application
│   ├── models.py            # Login, User, Doctor, Appointment, Payment, ...
│   ├── views.py             # Views, AI inference, SerpAPI integrations
│   ├── forms.py             # ModelForm definitions
│   ├── urls.py              # App URL routes
│   ├── admin.py             # Django admin registration
│   ├── middlewares.py       # Custom middleware
│   ├── migrations/          # Database migrations
│   ├── static/              # Static assets
│   └── templates/           # HTML templates (Bootstrap)
├── hf_cache_v2/             # Model cache (git-ignored, created at runtime)
├── manage.py                # Django command-line utility
├── requirements.txt         # Python dependencies
└── .gitignore
```

---

## Usage Guide

1. **Register** as a patient, doctor, or hospital from the landing page. Doctor/hospital/ambulance registrations require admin approval.
2. **Patients** can upload a skin image under the analysis feature to get an AI prediction, confidence score, severity alert, and recommended remedies.
3. **Book appointments** with approved doctors, complete the consultation payment, and track prescriptions and test reports.
4. **Doctors** can manage their availability, accept appointments, write digital prescriptions, and chat or video-consult with patients.
5. **Hospitals & ambulance units** coordinate patient transfers, assignments, and emergency broadcasts shown on the map.

---

## Key Endpoints

| Method | Route | Description |
| --- | --- | --- |
| POST | `/predict_skin_disease/` | Upload a skin image and receive an AI classification |
| GET | `/recommended-products/` | Skincare product recommendations |
| GET | `/personalized_products/` | Personalized product suggestions |
| POST | `/save_disease/<appointment_id>/` | Attach a detected disease to an appointment |
| GET | `/hospital/emergencies/api/` | Hospital emergency feed (JSON) |
| GET | `/hospital/emergency/map/` | Emergency map view |

All other views are served through Django's standard view routing (see `DermaAIapp/urls.py`).

---

## Configuration

Environment-sensitive values can be overridden in `DermaAI/settings.py` or via environment variables:

| Setting | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key (replace in production) |
| `DEBUG` | Set to `False` in production |
| `DATABASES` | SQLite3 by default; swap `ENGINE`/`NAME` for PostgreSQL |
| `SERPAPI_KEY` | API key for home remedy / medicine / product search |

> Security note: never commit real `SECRET_KEY` or `SERPAPI_KEY` values. Use environment variables in production.

---

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an [issue](https://github.com/gokulblee-code/Derma-Ai/issues) or submit a pull request. For substantial changes, please open an issue first to discuss what you would like to change.

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
