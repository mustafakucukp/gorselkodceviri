import cv2
import pytesseract

# Tesseract OCR'yi ayarla
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Gerekli ön işlemleri ekleyin (örneğin, bulanıklık, eşikleme)
    return gray

def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image)
    return text

def check_code_syntax_and_execute(code):
    import io
    import contextlib

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

# Resim yolunu belirtin
image_path = 'RESİMYOLU'
extracted_text = extract_text_from_image(image_path)
is_valid, message, exec_output = check_code_syntax_and_execute(extracted_text)

# Kodun çıktısını en altta yazdırın
output = ""
if is_valid:
    output += f"Extracted Text:\n{extracted_text}\n\n"
    output += f"Code Validity and Execution Result:\n{message}\n\n"
    output += f"Execution Output:\n{exec_output}"
else:
    output += f"Extracted Text:\n{extracted_text}\n\n"
    output += f"Code Validity and Execution Result:\n{message}\n"

print(output)


