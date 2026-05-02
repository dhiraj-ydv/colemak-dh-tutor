# Colemak-DH Touch Typing Tutor

A full-stack web application designed to help users master the Colemak-DH keyboard layout through progressive lessons and real-time visual guidance.

## Features
- **Progressive Lessons:** From home row basics to full mastery.
- **Custom Practice:** Paste any text or upload `.txt` files to practice.
- **Dynamic Visualizer:** Real-time keyboard and hand visualization with finger highlighting.
- **Progress Tracking:** Saves WPM and accuracy to a local database.
- **Web App UI:** Clean, responsive dark-themed interface with a mobile-style hamburger menu.
- **Ergonomic Mapping:** 100% accurate finger-to-key mapping for Colemak-DH.

## Tech Stack
- **Frontend:** Vue.js 3, TypeScript, Vite, Vanilla CSS.
- **Backend:** Python (Flask), Flask-SQLAlchemy, SQLite.

## Getting Started

### Prerequisites
- Python 3.x
- Node.js & npm

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd "Colemak Touch Typing"
   ```

2. **Setup Backend:**
   ```bash
   cd backend
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Setup Frontend:**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the App

1. **Recommended (Windows):**
   Simply double-click the **`start.bat`** file in the root directory. This will:
   - Launch the backend and frontend in the background.
   - Automatically manage process life-cycles.
   - Support **Stop** and **Restart** commands directly from the web app's menu.

2. **Manual Start:**
   - **Backend:** `python run.py` (from root)
   - **Frontend:** `npm run dev` (from `frontend` folder)

## Usage
- Click the **☰ menu** to select lessons or access Custom Practice.
- Use **TAB** to force focus the typing area.
- Use **ESC** to restart the current lesson.

## License
MIT
