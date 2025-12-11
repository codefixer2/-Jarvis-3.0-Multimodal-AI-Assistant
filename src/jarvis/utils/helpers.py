"""Helper utility functions"""
import time
import os


def format_timestamp():
    """Get formatted timestamp string"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_applications():
    """Get dictionary of available applications"""
    return {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "camera": "microsoft.windows.camera:",
        "browser": 'chrome.exe',
        "OpenAI": "C:\\Program Files\\OpenAI\\OpenAI.exe",
        "Brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
        "Discord": "C:\\Program Files\\Discord\\Discord.exe",
        "WhatsApp": "C:\\Program Files\\WhatsApp\\WhatsApp.exe",
        "Telegram": "C:\\Program Files\\Telegram\\Telegram.exe",
        "Skype": "C:\\Program Files\\Skype\\Skype.exe",
        "Zoom": "C:\\Program Files\\Zoom\\Zoom.exe",
        "Microsoft Teams": "C:\\Program Files\\Microsoft Teams\\Teams.exe",
        "Microsoft Edge": "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
        "Microsoft Word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "Microsoft Excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "Microsoft PowerPoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
        "Microsoft OneNote": "C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE",
        "Microsoft Outlook": "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE",
        "whatsapp": "C:\\Program Files\\WhatsApp\\WhatsApp.exe",
        "youtube": "C:\\Program Files\\Youtube\\Youtube.exe",
        "facebook": "C:\\Program Files\\Facebook\\Facebook.exe",
        "Chrome": "C:\\Program Files\\Chrome\\Chrome.exe",
        "twitter": "C:\\Program Files\\Twitter\\Twitter.exe",
        "linkedin": "C:\\Program Files\\LinkedIn\\LinkedIn.exe",
        "github": "C:\\Program Files\\GitHub\\GitHub.exe",
        "gitlab": "C:\\Program Files\\GitLab\\GitLab.exe",
    }


def open_application(app_name):
    """Open an application by name"""
    apps = get_applications()
    app_path = apps.get(app_name.lower())
    if app_path:
        try:
            os.startfile(app_path)
            return True, f"Opened application: {app_name}"
        except Exception as e:
            return False, f"Failed to open application {app_name}: {str(e)}"
    else:
        return False, f"Application not found in database: {app_name}"


