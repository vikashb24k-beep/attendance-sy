---
title: Facevplus Backend
emoji: 👁️
colorFrom: indigo
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
---

# FaceVPlus — Face & Voice Recognition Attendance System (v2.0)

FaceVPlus is a multi-modal attendance management system engineered for modern classrooms. It provides automated student attendance tracking using face recognition (Dlib 128D descriptors) and voice recognition (Resemblyzer acoustic embeddings), backed by a hosted Supabase PostgreSQL database.

---

## Quick Start Guide (Step-by-Step)

### Prerequisites

Make sure you have installed on your computer:
- **Python**: Version 3.10, 3.11, or 3.12 (Python 3.11 recommended)
- **Node.js**: Version 18.0 or higher (v20+ recommended)
- **Git**: Installed on your system
- **Supabase Account**: An active Supabase project with database credentials
- **Webcam & Microphone**: For live biometric capture

---

### Phase 1: Clone the Repository

Open your terminal or command prompt:

```bash
git clone https://github.com/RamanKumar-Dev/Face-recognition-based-attendance-system.git
cd Face-recognition-based-attendance-system
```

---

### Phase 2: Backend Setup (FastAPI & Python)

> **Important**: The backend package is structured as `backend.app`. Run commands from the **root directory** of the repository so Python resolves module paths correctly.

#### Step 1: Create a Virtual Environment

```bash
# Windows
python -m venv venv

# Linux / macOS
python3 -m venv venv
```

#### Step 2: Activate the Virtual Environment

```bash
# Windows (PowerShell)
# If script execution is disabled, allow it for the current session first:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.\venv\Scripts\activate.bat

# Linux / macOS
source venv/bin/activate
```

#### Step 3: Install Backend Dependencies

Make sure to install using `backend/requirements.txt`, which includes all biometric, audio, and token packages:

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

> **Note for Windows users**: `backend/requirements.txt` includes `dlib-bin`, which avoids needing C++ build tools or CMake on Windows.

#### Step 4: Configure Backend Environment Variables

Create a `.env` file inside the `backend/` folder by copying the example template:

```bash
# Windows (PowerShell)
Copy-Item backend/.env.example backend/.env

# Linux / macOS
cp backend/.env.example backend/.env
```

Open `backend/.env` in any text editor and fill in your values:

```ini
# --- Supabase Database ---
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-service-role-or-anon-key

# --- Security & JWT ---
# Use a strong random string (at least 32 characters)
JWT_SECRET=your-random-32-character-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# --- Institutional Access (Google Sign-In) ---
# Web application client ID from Google Cloud Console
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
ALLOWED_EMAIL_DOMAIN=iiitdwd.ac.in

# --- Admin Account ---
# Credentials used to sign in at /admin/login to approve teachers
ADMIN_EMAIL=admin@iiitdwd.ac.in
ADMIN_PASSWORD=choose-a-strong-admin-password

# --- App Settings & CORS ---
APP_NAME=FaceVPlus API
APP_ENV=development
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000
```

#### Step 5: Start the Backend Server

From the **project root folder**, run:

```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

> **Success Check**:
> - Open `http://127.0.0.1:8000/api/health` in your browser. You should receive `{"status": "healthy", ...}`.
> - Open `http://127.0.0.1:8000/docs` to test endpoints in the interactive Swagger UI.

---

### Phase 3: Frontend Setup (React & Vite)

Open a **new terminal window** (keep the backend server running in the first terminal).

#### Step 1: Navigate to the Frontend Directory

```bash
cd frontend
```

#### Step 2: Install Node Dependencies

```bash
npm install
```

#### Step 3: Configure Frontend Environment Variables

Create a `.env` file inside the `frontend/` folder by copying the example template:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

Open `frontend/.env` and configure:

```ini
# In development, Vite automatically proxies /api to http://127.0.0.1:8000
VITE_API_URL=/api
VITE_APP_URL=http://localhost:5173

# Must match GOOGLE_CLIENT_ID in backend/.env
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

#### Step 4: Start the Frontend Development Server

```bash
npm run dev
```

> **Success Check**: Open `http://localhost:5173` in your browser to access the FaceVPlus application.

---

### Phase 4: Database Setup (Supabase PostgreSQL)

1. Sign in to your [Supabase Dashboard](https://supabase.com).
2. Open the **SQL Editor** in your Supabase project.
3. If setting up or updating verification and college domain columns, copy and execute the script in [`backend/migrations/001_verification.sql`](backend/migrations/001_verification.sql).
4. Verify the following core tables are present:
   - **`teachers`**: `teacher_id`, `username`, `password`, `name`, `email`, `status` (`pending` / `approved` / `rejected`).
   - **`students`**: `student_id`, `name`, `email`, `roll_no`, `status` (`pending` / `approved` / `rejected`), `face_embedding` (128D array), `voice_embedding` (256D array).
   - **`subjects`**: `subject_id`, `subject_code`, `name`, `section`, `teacher_id`.
   - **`subject_students`**: `subject_id`, `student_id`, `status` (`pending` / `approved` / `rejected`), `requested_at`.
   - **`attendance_logs`**: `id`, `timestamp`, `subject_id`, `student_id`, `is_present`.

---

### Phase 5: Google OAuth Setup

To enable college-only sign-in:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Create or select a project, then configure the OAuth consent screen.
3. Create Credentials $\to$ **OAuth client ID** $\to$ Application type: **Web application**.
4. Under **Authorized JavaScript origins**, add:
   - `http://localhost:5173`
   - `http://127.0.0.1:5173`
   *(Plus your production URL if deploying)*
5. Copy the generated Client ID:
   - Paste into `backend/.env` as `GOOGLE_CLIENT_ID`
   - Paste into `frontend/.env` as `VITE_GOOGLE_CLIENT_ID`

---

## Features & Verification Workflow

```text
[Institutional Google OAuth (@iiitdwd.ac.in)]
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
[Teacher Registration]  [Student Registration]
   (Status: Pending)       (Status: Pending + Face Photo)
        │                   │
   [Admin Approval]         │ (Teacher shares subject invite / QR)
        │                   ▼
   [Teacher Active] ──> [Teacher Approves Subject Join Request]
                            │
                       [Student Verified & Enrolled]
```

### 1. Admin Portal (`/admin/login`)
- Log in with `ADMIN_EMAIL` and `ADMIN_PASSWORD` from `backend/.env`.
- Review pending teacher sign-ups, approve legitimate faculty, or reject unauthorized accounts.

### 2. Teacher Portal (`/teacher/login`)
- Register with institutional `@iiitdwd.ac.in` Google account.
- Once approved by Admin, create subjects and generate dynamic join codes or QR codes.
- Review and approve pending student join requests.
- **Biometric Attendance**:
  - **Face Recognition**: Upload single/batch classroom photos. Dlib detects faces and matches 128D descriptors against enrolled students.
  - **Voice Attendance**: Record classroom audio utterances to identify students using 256D Resemblyzer embeddings.
  - Review, manually adjust, and finalize attendance records.

### 3. Student Portal (`/student/login`)
- Register with institutional `@iiitdwd.ac.in` Google account and capture a reference face photo.
- Enroll in courses by entering subject code or scanning teacher-provided QR code.
- Authenticate via webcam facial recognition for instant login.
- View real-time subject-wise attendance percentages.

---

## System Architecture

```text
┌────────────────────────────────────────────────────────┐
│                   React 18 + Vite                      │
│   Tailwind CSS • Lucide React • React Router • Axios   │
└───────────────────────────┬────────────────────────────┘
                            │ REST API (JSON / FormData)
                            │ (Vite proxy: /api -> :8000)
┌───────────────────────────▼────────────────────────────┐
│                  FastAPI Backend                       │
│    Uvicorn • Pydantic v2 • PyJWT • Bcrypt Security     │
├───────────────────────────┬────────────────────────────┤
│     Biometric Pipelines   │     Data Access Layer      │
│  • Dlib 128D Face Embed   │  • Supabase Python Client  │
│  • Resemblyzer 256D Voice │  • PostgreSQL Relational   │
└───────────────────────────┴────────────────────────────┘
```

---

## Folder Structure

```text
Face-attendance-system/
├── backend/                  # FastAPI Backend
│   ├── app/
│   │   ├── main.py           # Entrypoint, CORS, route registration
│   │   ├── core/             # Config, security, Google auth
│   │   ├── api/              # Routes (auth, subjects, attendance, admin)
│   │   ├── schemas/          # Pydantic data schemas
│   │   └── services/         # Face & voice processing, Supabase repos
│   ├── requirements.txt      # Complete backend dependencies
│   ├── .env.example          # Backend environment template
│   └── .env                  # Local secret configuration
├── frontend/                 # React Frontend
│   ├── src/
│   │   ├── App.jsx           # App layout & routing
│   │   ├── context/          # React AuthContext
│   │   ├── pages/            # Admin, Teacher, and Student views
│   │   └── components/       # Common UI elements, modals, dialogs
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite config with /api proxy
│   └── .env.example          # Frontend environment template
├── tests/                    # Automated backend tests
├── requirements.txt          # Root package reference
└── README.md
```

---

## Running Backend Tests

Run automated tests to verify authentication tokens, route handlers, and QR code generation:

```bash
# Make sure your virtual environment is active at repository root
pytest backend/tests -v
```

---

## Troubleshooting & FAQ

### `ModuleNotFoundError: No module named 'backend'`
- **Fix**: Run `uvicorn` from the repository root folder, **not** from inside `backend/`:
  ```bash
  uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
  ```

### PowerShell: `running scripts is disabled on this system`
- **Fix**: Run this in PowerShell before activating `venv`:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\venv\Scripts\Activate.ps1
  ```

### Camera or Microphone Access Denied
- Browsers require secure origins (`localhost` or `https://`) for media device permissions. Access the web interface via `http://localhost:5173`.

### Google Sign-in Error: `redirect_uri_mismatch` or Origin Error
- Ensure `http://localhost:5173` is listed under **Authorized JavaScript origins** in Google Cloud Console OAuth credentials.

### `pkg_resources` Deprecation Warning
- This is an upstream warning from `face_recognition_models` and `webrtcvad`. It does not affect functionality and can be safely ignored.

---

## Contributors

Contributions, issues, and feature requests are welcome!

* **Vikash Kumar** — https://github.com/vikashb24k-beep
* **Raman Kumar** — https://github.com/RamanKumar-Dev
* **Nikhil Kumar Sinha** — https://github.com/Nikhil-sinhaa
* **R D** — https://github.com/rd6260
* **Saksham Kushwah** — https://github.com/shhadowpdf

## License

All rights reserved © 2026 FaceVPlus.
