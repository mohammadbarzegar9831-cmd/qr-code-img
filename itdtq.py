import sys
import os
import pickle
import json
from datetime import datetime
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import segno

# ==============================
# Initial Settings
# ==============================
SCOPES = ['https://www.googleapis.com/auth/drive']
APP_NAME = "Google Drive Manager"
VERSION = "2.3"
CONFIG_FILE = "app_config.json"

# ==============================
# Settings Manager
# ==============================
class ConfigManager:
    @staticmethod
    def load():
        default = {"theme": "dark"}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return default
        return default
    
    @staticmethod
    def save(config):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

# ==============================
# Theme Manager (Modern & Minimal Design)
# ==============================
class ThemeManager:
    DARK = {
        "bg": "#0D1117",
        "surface": "#161B22",
        "card": "#1C2333",
        "hover": "#252D3F",
        "primary": "#6C5CE7",
        "primary_hover": "#7C6CF0",
        "primary_light": "#A29BFE",
        "success": "#2EA043",
        "warning": "#D29922",
        "danger": "#F85149",
        "text": "#E6EDF3",
        "text_secondary": "#8B949E",
        "border": "#30363D",
        "input_bg": "#0D1117",
        "shadow": "rgba(0,0,0,0.4)"
    }
    
    LIGHT = {
        "bg": "#F3F6F9",
        "surface": "#FFFFFF",
        "card": "#FFFFFF",
        "hover": "#F0F2F5",
        "primary": "#6C5CE7",
        "primary_hover": "#5A4BD1",
        "primary_light": "#A29BFE",
        "success": "#00B894",
        "warning": "#FDCB6E",
        "danger": "#E17055",
        "text": "#2D3436",
        "text_secondary": "#636E72",
        "border": "#E2E8F0",
        "input_bg": "#FFFFFF",
        "shadow": "rgba(0,0,0,0.08)"
    }
    
    @staticmethod
    def get_theme(name):
        return ThemeManager.DARK if name == "dark" else ThemeManager.LIGHT
    
    @staticmethod
    def generate_stylesheet(name):
        c = ThemeManager.get_theme(name)
        return f"""
            /* ===== Base ===== */
            QMainWindow, QWidget {{
                background-color: {c["bg"]};
                color: {c["text"]};
                font-family: 'Vazir', 'Segoe UI', 'Microsoft YaHei', sans-serif;
                font-size: 13px;
            }}
            
            /* ===== Tabs (borderless, smooth transition) ===== */
            QTabWidget::pane {{
                border: none;
                background: transparent;
                margin-top: 6px;
            }}
            QTabBar::tab {{
                background: transparent;
                color: {c["text_secondary"]};
                border: none;
                padding: 10px 20px;
                margin: 0 2px;
                font-weight: 500;
                font-size: 14px;
                border-radius: 0;
                border-bottom: 2px solid transparent;
            }}
            QTabBar::tab:selected {{
                color: {c["primary"]};
                border-bottom-color: {c["primary"]};
            }}
            QTabBar::tab:hover:!selected {{
                color: {c["text"]};
                background: {c["hover"]};
                border-radius: 8px 8px 0 0;
            }}
            
            /* ===== Inputs ===== */
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background-color: {c["input_bg"]};
                color: {c["text"]};
                border: 2px solid {c["border"]};
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 14px;
                transition: border-color 0.2s;
            }}
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                border-color: {c["primary"]};
            }}
            QLineEdit::placeholder, QTextEdit::placeholder {{
                color: {c["text_secondary"]};
            }}
            
            /* ===== Buttons ===== */
            QPushButton {{
                background-color: {c["primary"]};
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
                padding: 10px 20px;
                transition: background-color 0.2s, transform 0.1s;
            }}
            QPushButton:hover {{
                background-color: {c["primary_hover"]};
            }}
            QPushButton:pressed {{
                background-color: {c["primary_light"]};
            }}
            QPushButton:disabled {{
                background-color: {c["border"]};
                color: {c["text_secondary"]};
            }}
            
            /* ===== Labels (borderless, transparent) ===== */
            QLabel {{
                color: {c["text"]};
                background: transparent;
                border: none;
            }}
            QLabel[type="title"] {{
                font-size: 22px;
                font-weight: bold;
                color: {c["text"]};
                margin-bottom: 4px;
            }}
            QLabel[type="subtitle"] {{
                font-size: 14px;
                color: {c["text_secondary"]};
                margin-bottom: 16px;
            }}
            QLabel[type="label"] {{
                font-weight: 600;
                font-size: 14px;
                color: {c["text_secondary"]};
                margin-bottom: 4px;
            }}
            
            /* ===== Progress Bar ===== */
            QProgressBar {{
                border: none;
                border-radius: 12px;
                background: {c["border"]};
                height: 24px;
                text-align: center;
                color: {c["text"]};
                font-weight: 600;
                font-size: 13px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {c["primary"]}, stop:1 {c["primary_light"]});
                border-radius: 12px;
            }}
            
            /* ===== Scrollbar ===== */
            QScrollBar:vertical {{
                background: transparent;
                width: 6px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {c["border"]};
                border-radius: 3px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {c["primary"]};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            
            /* ===== Combo Box ===== */
            QComboBox {{
                background-color: {c["input_bg"]};
                color: {c["text"]};
                border: 2px solid {c["border"]};
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 14px;
            }}
            QComboBox:hover {{
                border-color: {c["primary"]};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {c["surface"]};
                color: {c["text"]};
                border: 1px solid {c["border"]};
                border-radius: 10px;
                selection-background-color: {c["primary"]};
                selection-color: white;
            }}
            
            /* ===== Result (TextBox) ===== */
            QTextEdit[type="result"] {{
                background-color: {c["surface"]};
                border: 1px solid {c["border"]};
                border-radius: 12px;
                padding: 14px;
                font-size: 13px;
                min-height: 80px;
            }}
            
            /* ===== Theme Button ===== */
            #themeToggleBtn {{
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 20px;
                color: white;
                font-size: 18px;
                padding: 4px 14px;
            }}
            #themeToggleBtn:hover {{
                background: rgba(255,255,255,0.18);
                border-color: rgba(255,255,255,0.4);
            }}
        """

# ==============================
# Drive Manager Class
# ==============================
class DriveManager:
    def __init__(self, credentials_path='credentials.json'):
        self.credentials_path = credentials_path
        self.service = None
        self.authenticate()

    def authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('drive', 'v3', credentials=creds)

    def create_folder(self, folder_name):
        try:
            file_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
            folder = self.service.files().create(body=file_metadata, fields='id').execute()
            return folder.get('id'), None
        except Exception as e:
            return None, str(e)

    def upload_file(self, file_path, file_name, folder_id=None):
        try:
            file_metadata = {'name': file_name}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
            return file.get('id'), None
        except Exception as e:
            return None, str(e)

    def search_file(self, folder_id, file_name):
        try:
            query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get('files', [])
            if files:
                return files[0]['id'], None
            return None, "File not found"
        except Exception as e:
            return None, str(e)

    def make_public(self, file_id):
        try:
            permission = {'type': 'anyone', 'role': 'reader'}
            self.service.permissions().create(fileId=file_id, body=permission).execute()
            return True, None
        except Exception as e:
            return False, str(e)

    def get_public_link(self, file_id):
        return f"https://drive.google.com/file/d/{file_id}/view"

    def generate_qr(self, link, name, scale=30):
        try:
            qr = segno.make(link)
            output_path = os.path.join(os.getcwd(), f"{name}.png")
            qr.save(output_path, scale=scale, border=4)
            return output_path, None
        except Exception as e:
            return None, str(e)

# ==============================
# Worker (QThread)
# ==============================
class Worker(QThread):
    finished = Signal(object, str)
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result, "")
        except Exception as e:
            self.finished.emit(None, str(e))

# ==============================
# Main Window (Modern UI)
# ==============================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = ConfigManager.load()
        self.current_theme = self.config.get("theme", "dark")
        self.drive = DriveManager()
        
        self.setWindowTitle(f"{APP_NAME} v{VERSION}")
        self.setGeometry(100, 100, 1100, 780)
        self.setMinimumSize(950, 700)
        
        # ===== Header =====
        header = QWidget()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6C5CE7, stop:1 #9B59B6);
                border-bottom: none;
            }
        """)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(30, 0, 30, 0)
        
        title = QLabel("🚀 " + APP_NAME)
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        h_layout.addWidget(title)
        h_layout.addStretch()
        
        status = QLabel("✅ Connected")
        status.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 13px;")
        h_layout.addWidget(status)
        h_layout.addSpacing(16)
        
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setObjectName("themeToggleBtn")
        self.theme_btn.setFixedSize(48, 34)
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        h_layout.addWidget(self.theme_btn)
        
        # ===== Central area =====
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabWidget::pane { background: transparent; }")
        main_layout.addWidget(self.tabs)
        
        self.tab_upload = QWidget()
        self.tab_folder = QWidget()
        self.tab_link = QWidget()
        self.tab_qr = QWidget()
        self.tab_logs = QWidget()
        
        self.tabs.addTab(self.tab_upload, "📤 Upload")
        self.tabs.addTab(self.tab_folder, "📁 Folder")
        self.tabs.addTab(self.tab_link, "🔗 Public Link")
        self.tabs.addTab(self.tab_qr, "📱 QR Code")
        self.tabs.addTab(self.tab_logs, "📋 Log")
        
        # Apply theme
        self.apply_theme(self.current_theme)
        
        # Setup tab contents
        self.setup_upload_tab()
        self.setup_folder_tab()
        self.setup_link_tab()
        self.setup_qr_tab()
        self.setup_logs_tab()
        
        self.add_log("✅ Application started")
        self.add_log(f"🎨 Theme: {'Dark' if self.current_theme == 'dark' else 'Light'}")
    
    # ==============================
    # Theme management
    # ==============================
    def apply_theme(self, name):
        self.current_theme = name
        self.setStyleSheet(ThemeManager.generate_stylesheet(name))
        if hasattr(self, 'theme_btn'):
            self.theme_btn.setText("☀️" if name == "dark" else "🌙")
            self.theme_btn.setToolTip("Switch to Light Theme" if name == "dark" else "Switch to Dark Theme")
        self.config["theme"] = name
        ConfigManager.save(self.config)
    
    def toggle_theme(self):
        new = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new)
        self.add_log(f"🎨 Theme changed to: {'Light' if new == 'light' else 'Dark'}")
    
    # ==============================
    # Upload Tab
    # ==============================
    def setup_upload_tab(self):
        layout = QVBoxLayout(self.tab_upload)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        
        title = QLabel("📤 File Upload")
        title.setProperty("type", "title")
        layout.addWidget(title)
        
        sub = QLabel("Select your file and upload it to the desired folder.")
        sub.setProperty("type", "subtitle")
        layout.addWidget(sub)
        
        lbl = QLabel("File Path:")
        lbl.setProperty("type", "label")
        layout.addWidget(lbl)
        
        file_row = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Select file path...")
        file_row.addWidget(self.file_path_edit)
        
        browse_btn = QPushButton("📂 Browse")
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.browse_file)
        file_row.addWidget(browse_btn)
        layout.addLayout(file_row)
        
        lbl2 = QLabel("Folder ID or Link (optional):")
        lbl2.setProperty("type", "label")
        layout.addWidget(lbl2)
        self.folder_id_edit = QLineEdit()
        self.folder_id_edit.setPlaceholderText("Folder link or ID (leave empty for root)")
        layout.addWidget(self.folder_id_edit)
        
        lbl3 = QLabel("File Name on Drive:")
        lbl3.setProperty("type", "label")
        layout.addWidget(lbl3)
        self.file_name_edit = QLineEdit()
        self.file_name_edit.setPlaceholderText("Custom name (default: original name)")
        layout.addWidget(self.file_name_edit)
        
        self.upload_btn = QPushButton("🚀 Upload File")
        self.upload_btn.setFixedHeight(48)
        self.upload_btn.clicked.connect(self.start_upload)
        layout.addWidget(self.upload_btn)
        
        self.upload_progress = QProgressBar()
        self.upload_progress.setValue(0)
        self.upload_progress.setVisible(False)
        layout.addWidget(self.upload_progress)
        
        self.upload_result = QTextEdit()
        self.upload_result.setProperty("type", "result")
        self.upload_result.setReadOnly(True)
        self.upload_result.setMinimumHeight(90)
        layout.addWidget(self.upload_result)
        
        layout.addStretch()
    
    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.file_path_edit.setText(path)
            if not self.file_name_edit.text():
                self.file_name_edit.setText(os.path.basename(path))
    
    def start_upload(self):
        path = self.file_path_edit.text().strip()
        if not path or not os.path.exists(path):
            self.upload_result.setHtml("<span style='color:#F85149;'>❌ Please select a valid file.</span>")
            return
        
        folder_input = self.folder_id_edit.text().strip()
        folder_id = self.clean_folder_id(folder_input) if folder_input else None
        fname = self.file_name_edit.text().strip()
        if not fname:
            fname = os.path.basename(path)
        
        self.upload_btn.setEnabled(False)
        self.upload_progress.setVisible(True)
        self.upload_progress.setValue(10)
        self.upload_result.setHtml("<span style='color:#D29922;'>⏳ Uploading...</span>")
        
        def task():
            return self.drive.upload_file(path, fname, folder_id)
        self.run_worker(task, self.on_upload_finished)
    
    def on_upload_finished(self, result, error):
        self.upload_btn.setEnabled(True)
        self.upload_progress.setValue(100)
        if error:
            self.upload_result.setHtml(f"<span style='color:#F85149;'>❌ Error: {error}</span>")
            return
        file_id = result[0] if isinstance(result, tuple) else result
        if not file_id:
            self.upload_result.setHtml("<span style='color:#F85149;'>❌ File ID not received.</span>")
            return
        link = self.drive.get_public_link(file_id)
        self.upload_result.setHtml(
            f"<span style='color:#2EA043;'>✅ File uploaded successfully!</span><br>"
            f"🆔 ID: {file_id}<br>"
            f"🔗 Link: <a href='{link}' style='color:#58A6FF;'>{link}</a>"
        )
        self.add_log(f"File uploaded: {file_id}")
    
    # ==============================
    # Folder Tab
    # ==============================
    def setup_folder_tab(self):
        layout = QVBoxLayout(self.tab_folder)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(18)
        
        title = QLabel("📁 Create New Folder")
        title.setProperty("type", "title")
        layout.addWidget(title)
        
        sub = QLabel("Create a new folder in your Google Drive.")
        sub.setProperty("type", "subtitle")
        layout.addWidget(sub)
        
        lbl = QLabel("Folder Name:")
        lbl.setProperty("type", "label")
        layout.addWidget(lbl)
        self.folder_name_edit = QLineEdit()
        self.folder_name_edit.setPlaceholderText("Enter folder name...")
        layout.addWidget(self.folder_name_edit)
        
        self.folder_btn = QPushButton("➕ Create Folder")
        self.folder_btn.setFixedHeight(48)
        self.folder_btn.clicked.connect(self.start_create_folder)
        layout.addWidget(self.folder_btn)
        
        self.folder_result = QTextEdit()
        self.folder_result.setProperty("type", "result")
        self.folder_result.setReadOnly(True)
        self.folder_result.setMinimumHeight(90)
        layout.addWidget(self.folder_result)
        layout.addStretch()
    
    def start_create_folder(self):
        name = self.folder_name_edit.text().strip()
        if not name:
            self.folder_result.setHtml("<span style='color:#F85149;'>❌ Please enter a folder name.</span>")
            return
        self.folder_btn.setEnabled(False)
        self.folder_result.setHtml("<span style='color:#D29922;'>⏳ Creating...</span>")
        def task():
            return self.drive.create_folder(name)
        self.run_worker(task, self.on_folder_created)
    
    def on_folder_created(self, result, error):
        self.folder_btn.setEnabled(True)
        if error:
            self.folder_result.setHtml(f"<span style='color:#F85149;'>❌ Error: {error}</span>")
            return
        folder_id = result[0] if isinstance(result, tuple) else result
        if not folder_id:
            self.folder_result.setHtml("<span style='color:#F85149;'>❌ Folder ID not received.</span>")
            return
        link = f"https://drive.google.com/drive/folders/{folder_id}"
        self.folder_result.setHtml(
            f"<span style='color:#2EA043;'>✅ Folder created!</span><br>"
            f"🆔 ID: {folder_id}<br>"
            f"🔗 Link: <a href='{link}' style='color:#58A6FF;'>{link}</a>"
        )
        self.add_log(f"Folder created: {folder_id}")
    
    # ==============================
    # Public Link Tab
    # ==============================
    def setup_link_tab(self):
        layout = QVBoxLayout(self.tab_link)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(18)
        
        title = QLabel("🔗 Get Public Link")
        title.setProperty("type", "title")
        layout.addWidget(title)
        sub = QLabel("Get a shareable link for any file in your Drive.")
        sub.setProperty("type", "subtitle")
        layout.addWidget(sub)
        
        lbl1 = QLabel("Folder ID or Link:")
        lbl1.setProperty("type", "label")
        layout.addWidget(lbl1)
        self.link_folder_edit = QLineEdit()
        self.link_folder_edit.setPlaceholderText("Enter folder link or ID...")
        layout.addWidget(self.link_folder_edit)
        
        lbl2 = QLabel("Exact File Name:")
        lbl2.setProperty("type", "label")
        layout.addWidget(lbl2)
        self.link_file_edit = QLineEdit()
        self.link_file_edit.setPlaceholderText("Enter file name exactly...")
        layout.addWidget(self.link_file_edit)
        
        self.link_btn = QPushButton("🔗 Get Public Link")
        self.link_btn.setFixedHeight(48)
        self.link_btn.clicked.connect(self.start_get_link)
        layout.addWidget(self.link_btn)
        
        self.link_result = QTextEdit()
        self.link_result.setProperty("type", "result")
        self.link_result.setReadOnly(True)
        self.link_result.setMinimumHeight(90)
        layout.addWidget(self.link_result)
        layout.addStretch()
    
    def start_get_link(self):
        folder_input = self.link_folder_edit.text().strip()
        fname = self.link_file_edit.text().strip()
        if not folder_input or not fname:
            self.link_result.setHtml("<span style='color:#F85149;'>❌ Please fill in all fields.</span>")
            return
        folder_id = self.clean_folder_id(folder_input)
        if not folder_id:
            self.link_result.setHtml("<span style='color:#F85149;'>❌ Invalid folder ID.</span>")
            return
        self.link_btn.setEnabled(False)
        self.link_result.setHtml("<span style='color:#D29922;'>⏳ Searching...</span>")
        def task1():
            return self.drive.search_file(folder_id, fname)
        self.run_worker(task1, self.on_file_found)
    
    def on_file_found(self, result, error):
        if error or not result:
            self.link_btn.setEnabled(True)
            self.link_result.setHtml(f"<span style='color:#F85149;'>❌ File not found: {error}</span>")
            return
        file_id = result[0] if isinstance(result, tuple) else result
        if not file_id:
            self.link_btn.setEnabled(True)
            self.link_result.setHtml("<span style='color:#F85149;'>❌ Invalid file ID.</span>")
            return
        def task2():
            success, err = self.drive.make_public(file_id)
            if success:
                return self.drive.get_public_link(file_id), None
            return None, err
        self.run_worker(task2, self.on_link_ready)
    
    def on_link_ready(self, result, error):
        self.link_btn.setEnabled(True)
        if error:
            self.link_result.setHtml(f"<span style='color:#F85149;'>❌ Error: {error}</span>")
            return
        link = result[0] if isinstance(result, tuple) else result
        if not link:
            self.link_result.setHtml("<span style='color:#F85149;'>❌ Link not received.</span>")
            return
        self.link_result.setHtml(f"<span style='color:#2EA043;'>✅ Public link:</span><br>🔗 <a href='{link}' style='color:#58A6FF;'>{link}</a>")
        self.add_log(f"Public link: {link}")
    
    # ==============================
    # QR Code Tab
    # ==============================
    def setup_qr_tab(self):
        layout = QVBoxLayout(self.tab_qr)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(18)
        
        title = QLabel("📱 Generate QR Code")
        title.setProperty("type", "title")
        layout.addWidget(title)
        sub = QLabel("Convert any link into a high-quality printable QR Code.")
        sub.setProperty("type", "subtitle")
        layout.addWidget(sub)
        
        lbl1 = QLabel("Link:")
        lbl1.setProperty("type", "label")
        layout.addWidget(lbl1)
        self.qr_link_edit = QLineEdit()
        self.qr_link_edit.setPlaceholderText("Enter link...")
        layout.addWidget(self.qr_link_edit)
        
        lbl2 = QLabel("Output File Name:")
        lbl2.setProperty("type", "label")
        layout.addWidget(lbl2)
        self.qr_name_edit = QLineEdit()
        self.qr_name_edit.setPlaceholderText("Custom name (without extension)")
        layout.addWidget(self.qr_name_edit)
        
        lbl3 = QLabel("Quality (scale) - suggested 30:")
        lbl3.setProperty("type", "label")
        layout.addWidget(lbl3)
        self.qr_scale_edit = QLineEdit()
        self.qr_scale_edit.setPlaceholderText("Number 10 to 50")
        self.qr_scale_edit.setText("30")
        layout.addWidget(self.qr_scale_edit)
        
        self.qr_btn = QPushButton("📱 Generate QR Code")
        self.qr_btn.setFixedHeight(48)
        self.qr_btn.clicked.connect(self.start_generate_qr)
        layout.addWidget(self.qr_btn)
        
        self.qr_result = QTextEdit()
        self.qr_result.setProperty("type", "result")
        self.qr_result.setReadOnly(True)
        self.qr_result.setMinimumHeight(90)
        layout.addWidget(self.qr_result)
        layout.addStretch()
    
    def start_generate_qr(self):
        link = self.qr_link_edit.text().strip()
        name = self.qr_name_edit.text().strip()
        scale_text = self.qr_scale_edit.text().strip()
        if not link:
            self.qr_result.setHtml("<span style='color:#F85149;'>❌ Please enter a link.</span>")
            return
        if not name:
            name = f"qrcode_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            scale = int(scale_text) if scale_text else 30
        except:
            scale = 30
        self.qr_btn.setEnabled(False)
        self.qr_result.setHtml("<span style='color:#D29922;'>⏳ Generating...</span>")
        def task():
            return self.drive.generate_qr(link, name, scale)
        self.run_worker(task, self.on_qr_generated)
    
    def on_qr_generated(self, result, error):
        self.qr_btn.setEnabled(True)
        if error:
            self.qr_result.setHtml(f"<span style='color:#F85149;'>❌ Error: {error}</span>")
            return
        path = result[0] if isinstance(result, tuple) else result
        if not path:
            self.qr_result.setHtml("<span style='color:#F85149;'>❌ File path not received.</span>")
            return
        self.qr_result.setHtml(f"<span style='color:#2EA043;'>✅ QR Code generated!</span><br>📁 Path: {path}")
        self.add_log(f"QR generated: {path}")
    
    # ==============================
    # Log Tab
    # ==============================
    def setup_logs_tab(self):
        layout = QVBoxLayout(self.tab_logs)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(18)
        
        title = QLabel("📋 Operation Logs")
        title.setProperty("type", "title")
        layout.addWidget(title)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 11))
        layout.addWidget(self.log_text)
        
        clear_btn = QPushButton("🗑️ Clear Logs")
        clear_btn.setFixedHeight(40)
        clear_btn.clicked.connect(self.clear_logs)
        layout.addWidget(clear_btn)
    
    def clear_logs(self):
        self.log_text.clear()
        self.add_log("🗑️ Logs cleared")
    
    def add_log(self, msg):
        self.log_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    
    # ==============================
    # Helpers
    # ==============================
    def clean_folder_id(self, text):
        if not text:
            return None
        text = text.strip()
        if 'folders/' in text:
            parts = text.split('folders/')
            if len(parts) > 1:
                return parts[1].split('?')[0].strip()
        return text
    
    def run_worker(self, func, callback):
        self.worker = Worker(func)
        self.worker.finished.connect(callback)
        self.worker.start()

# ==============================
# Run
# ==============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
