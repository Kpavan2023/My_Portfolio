# Kollipara Pavan Kumar | Personal Portfolio

A responsive, dark-themed personal portfolio for a Software and AI/ML engineer. It is a single-page site (HTML, CSS and vanilla JavaScript) served by a small Flask app, with a working contact form.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Sections](#sections)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Contact Form Backend](#contact-form-backend)
- [Customization](#customization)
- [Deployment](#deployment)
- [Accessibility and Performance](#accessibility-and-performance)
- [Contact](#contact)
- [License](#license)

## Overview

This portfolio presents my education, skills, projects, IEEE publication and certificates in one scrolling page. It uses no frontend framework: everything lives in one `index.html` file with embedded CSS and JavaScript, so it is easy to read, edit and host anywhere.

## Features

- Dark glassmorphism design with gradient accents and an animated background
- Custom cursor and a subtle particle trail (desktop mouse only)
- Typing animation in the hero section
- Scroll-reveal animations using `IntersectionObserver`
- Sticky navbar that changes style on scroll, with a mobile hamburger menu
- Expandable certificate categories (Hackathons, Programming, Soft Skills)
- Contact form that posts JSON to a `/contact` endpoint, with a loading spinner and toast messages
- Scroll-to-top button
- Fully responsive layout (desktop, tablet, mobile)
- Respects `prefers-reduced-motion`

## Sections

| Section | What it shows |
|---|---|
| Home | Name, role, quote, typing animation, resume link, social links, profile photo |
| About | Introduction, stats (CGPA 8.74, projects, IEEE paper, hackathons), education timeline, core stack, interests |
| Skills | Languages, Web and Backend, AI/ML, Tools and Platforms, Core CS |
| Projects | Intrusion Detection System, Smart Library Manager, SmartQGen, Conversational Meeting Booking Assistant |
| Publications | IEEE ICAAIC 2025 paper with DOI and certificate link |
| Achievements | Hackathon, programming and soft-skills certificates |
| Contact | Email, LinkedIn, GitHub and a message form |

## Tech Stack

**Frontend**
- HTML5, CSS3 (custom properties, grid, flexbox, animations)
- Vanilla JavaScript (no libraries)
- Google Fonts: Syne and DM Sans
- Font Awesome 6.4 (CDN) for icons

**Backend**
- Python with Flask, serving `index.html`, static files and the `/contact` endpoint

## Project Structure

The HTML expects the profile image at `/static/images/Port_pic.jpeg` and a `POST /contact` route. A typical layout:

```
portfolio/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── images/
        └── Port_pic.jpeg
```

Adjust the paths if your repository is organised differently.

## Getting Started

### Prerequisites

- Python 3.9 or newer
- pip

### Run locally

```bash
# 1. Clone the repository
git clone https://github.com/Kpavan2023/<your-repo-name>.git
cd <your-repo-name>

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

### Just want to preview the page?

Open `index.html` directly in a browser. The page will load, but the profile image and the contact form will not work until it is served by Flask, because they rely on the `/static/...` and `/contact` paths.

## Contact Form Backend

The form in the Contact section sends this request:

```
POST /contact
Content-Type: application/json

{ "name": "...", "email": "...", "message": "..." }
```

The page shows a success message when the response status is 2xx and an error message otherwise.

Below is a minimal example `app.py` that serves the page and emails you each message. Treat it as a starting point and adapt it to your setup.

```python
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not (name and email and message):
        return jsonify({"error": "All fields are required"}), 400

    msg = EmailMessage()
    msg["Subject"] = f"Portfolio message from {name}"
    msg["From"] = os.environ["MAIL_USER"]
    msg["To"] = os.environ["MAIL_RECEIVER"]
    msg["Reply-To"] = email
    msg.set_content(f"Name: {name}\nEmail: {email}\n\n{message}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.environ["MAIL_USER"], os.environ["MAIL_APP_PASSWORD"])
            server.send_message(msg)
    except Exception as exc:
        app.logger.error("Mail error: %s", exc)
        return jsonify({"error": "Could not send message"}), 500

    return jsonify({"status": "sent"}), 200


if __name__ == "__main__":
    app.run(debug=True)
```

Example `requirements.txt`:

```
Flask
python-dotenv
gunicorn
```

Example `.env` (never commit this file; it is listed in `.gitignore`):

```
MAIL_USER=your_email@gmail.com
MAIL_APP_PASSWORD=your_gmail_app_password
MAIL_RECEIVER=your_email@gmail.com
```

For Gmail, create an App Password (requires 2-step verification) and use it instead of your normal password.

## Customization

- **Colors and fonts:** edit the CSS variables in the `:root` block at the top of the `<style>` section (`--indigo`, `--purple`, `--sky`, `--font-display`, `--font-body`).
- **Typing phrases:** change the `phrases` array in the JavaScript.
- **Projects:** copy any `.project-card` block inside `.projects-grid` and update the title, bullets, tech badges and GitHub link.
- **Certificates:** edit the `.cert-list` blocks near the bottom of the Achievements section.
- **Resume link:** update the `href` on the "View Resume" button in the hero section.
- **Profile photo:** replace `static/images/Port_pic.jpeg`.

## Deployment

Because the site needs a backend for the contact form, use a host that runs Python, for example Render, Railway or PythonAnywhere.

1. Push the repository to GitHub.
2. Create a new web service from the repository.
3. Set the build command to `pip install -r requirements.txt` and the start command to `gunicorn app:app`.
4. Add the `MAIL_USER`, `MAIL_APP_PASSWORD` and `MAIL_RECEIVER` environment variables in the host's dashboard.

If you only need the static page (no contact form), GitHub Pages or Netlify also work. Change the image path to a relative one (`static/images/Port_pic.jpeg`) and replace the form with a `mailto:` link or a form service.

## Accessibility and Performance

- The custom cursor only appears on devices with a fine pointer (mouse), so touch devices keep the normal cursor.
- Animations are disabled for visitors who enable "reduce motion" in their system settings.
- No JavaScript frameworks or build step, so the page stays lightweight.
- Images, fonts and icons load from a CDN or the static folder; keep the profile photo compressed for fast loading.

## Contact

- Email: pavankumarkollipara2@gmail.com
- LinkedIn: https://www.linkedin.com/in/pavan-kumar-kollipara-443947268/
- GitHub: https://github.com/Kpavan2023

## License

Copyright (c) 2026 Kollipara Pavan Kumar. All rights reserved.