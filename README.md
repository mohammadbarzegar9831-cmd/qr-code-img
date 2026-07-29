# 🚀 Google Drive Manager

A modern, feature-rich desktop application for managing Google Drive with an intuitive PySide6 GUI. Upload files, create folders, generate shareable links, and create QR codes—all with a sleek dark/light theme system.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)
![Version](https://img.shields.io/badge/version-2.3-orange.svg)

---

## ✨ Features

- **📤 File Upload** – Upload any file to Google Drive with optional target folder.
- **📁 Folder Creation** – Create new folders in your Drive.
- **🔗 Public Link Generator** – Search for a file and instantly generate a shareable link.
- **📱 QR Code Maker** – Convert any link (including generated Drive links) into a downloadable QR code image.
- **🎨 Modern Theming** – Toggle between elegant **Dark** and **Light** themes with a single click.
- **📋 Activity Log** – Real‑time log of all operations.
- **⚡ Asynchronous Tasks** – Background threading keeps the UI responsive.

---

## 📷 Screenshots

<p align="center">
  <img src="screenshots/dark_upload.png" width="45%" alt="Dark Upload Tab"/>
  <img src="screenshots/light_qr.png" width="45%" alt="Light QR Tab"/>
</p>

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- A Google Cloud project with the **Drive API** enabled
- OAuth 2.0 credentials (`credentials.json`)

### Step 1: Enable Google Drive API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Navigate to **APIs & Services > Library** and enable the **Google Drive API**.
4. Under **Credentials**, create an **OAuth 2.0 Client ID** (Desktop application type).
5. Download the JSON file and rename it to `credentials.json`.
6. Place this file in the same directory as the application.

### Step 2: Install Dependencies

Clone the repository and install the required packages:

```bash
git clone https://github.com/yourusername/google-drive-manager.git
cd google-drive-manager
pip install -r requirements.txt
