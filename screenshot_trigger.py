import pyautogui
import keyboard
import time
import win32clipboard
from PIL import Image
import io

def copy_image_to_clipboard(image_path):
    image = Image.open(image_path)
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  # Remove header
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def take_screenshot_and_paste():
    print("📸 Capturando screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")

    print("📋 Copiando imagem para a área de transferência...")
    copy_image_to_clipboard("screenshot.png")

    time.sleep(1)  # Espera para garantir que o navegador esteja pronto

    print("⌨️ Simulando Ctrl+V...")
    keyboard.press_and_release('ctrl+v')

    print("✅ Imagem colada! A análise deve iniciar automaticamente na UI.")

print("🚀 Pressione F8 para capturar e colar o print na UI.")
keyboard.add_hotkey('f8', take_screenshot_and_paste)

keyboard.wait()
