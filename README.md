# DermaAI ðŸ©º AI-Powered Dermatological Analysis System

DermaAI is a web application built with **Django** and powered by **Machine Learning / Deep Learning** models to assist in identifying skin conditions through image analysis.

---

## ðŸŒŸ Key Features

- **Skin Condition Detection:** Upload images of skin lesions for automated AI classification.
- **Patient & Doctor Portals:** Clean interfaces for managing analysis reports and records.
- **Report Generation:** View structured diagnosis reports based on AI outputs.
- **Local Cache Management:** Efficient handling of model weights and tokenizers without cluttering project history.

---

## ðŸ› ï¸ Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite3 (Development) / PostgreSQL (Production)
- **AI/ML:** PyTorch / TensorFlow / Hugging Face Transformers
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap

---

## ðŸš€ Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

Ensure you have the following installed:
- [Python 3.9+](https://www.python.org/)
- [Git](https://git-scm.com/)

---

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/gokulblee-code/Derma-Ai.git
   cd Derma-Ai/DermaAI
   ```

2. **Create and Activate Virtual Environment**
   - **Windows:**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## ðŸ“ Project Structure

```text
DermaAI/
â”‚
â”œâ”€â”€ DermaAI/           # Django project configuration
â”œâ”€â”€ DermaAIapp/        # Main application logic (views, models, routes)
â”œâ”€â”€ Dataset/           # Image dataset for model training (Ignored by Git)
â”œâ”€â”€ hf_cache/          # Hugging Face cached weights (Ignored by Git)
â”œâ”€â”€ venv/              # Python virtual environment (Ignored by Git)
â”œâ”€â”€ db.sqlite3         # Local database file
â”œâ”€â”€ manage.py          # Django command-line utility
â”œâ”€â”€ requirements.txt   # Required Python libraries
â””â”€â”€ README.md          # Project documentation
```

---

## ðŸ¤ Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/gokulblee-code/Derma-Ai/issues).

---

## ðŸ“„ License

This project is licensed under the MIT License - see the LICENSE file for details.
