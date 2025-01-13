import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Text, Scrollbar
import os
import numpy as np
import contextlib
import io

# Tesseract OCR'yi ayarla
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    with open(image_path, "rb") as f:
        data = np.frombuffer(f.read(), dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Görüntü dosyası okunamadı. Lütfen geçerli bir görüntü dosyası seçin.")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image)
    return text

def check_code_syntax_and_execute(code):
    try:
        compiled_code = compile(code, '<string>', 'exec')
        with contextlib.redirect_stdout(io.StringIO()) as f:
            exec(compiled_code, globals())
            exec_output = f.getvalue()
        return True, "Kod doğru ve çalıştırıldı.", exec_output
    except SyntaxError as e:
        return False, f"Syntax Hatası: {e}", ""
    except Exception as e:
        return False, f"Çalıştırma Hatası: {e}", ""

def show_results(title, content):
    result_window = Toplevel()
    result_window.title(title)
    result_window.geometry("600x400")  # Pencere boyutu

    text_widget = Text(result_window, wrap="word", font=("Arial", 12))
    text_widget.insert("1.0", content)
    text_widget.config(state="disabled")  # Kullanıcının metni değiştirmesini engelle

    scrollbar = Scrollbar(result_window, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)

    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            file_path = os.path.normpath(file_path)
            print(f"Seçilen dosya yolu: {file_path}")

            extracted_text = extract_text_from_image(file_path)

            is_valid, message, exec_output = check_code_syntax_and_execute(extracted_text)
            output = f"Extracted Text:\n{extracted_text}\n\n"
            output += f"Code Validity and Execution Result:\n{message}\n\n"

            if is_valid:
                output += f"Execution Output:\n{exec_output}"
            else:
                output += "Kod çalıştırılamadı."

            # Sonuçları özelleştirilmiş bir pencerede göster
            show_results("OCR ve Kod Çıktısı", output)
        except ValueError as ve:
            messagebox.showerror("Hata", str(ve))
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

root = tk.Tk()
root.title("OCR ve Kod Çalıştırma")

frame = tk.Frame(root)
frame.pack(pady=20)

# Daha büyük buton
select_button = tk.Button(
    frame,
    text="Dosya Seç",
    command=select_file,
    width=20,  # Butonun genişliği
    height=2,  # Butonun yüksekliği
    font=("Arial", 14)  # Yazı tipi ve boyutu
)
select_button.pack()

root.mainloop()
