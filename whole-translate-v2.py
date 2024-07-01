import os
import openai
from tqdm import tqdm

# OpenAI API anahtarınızı buraya girin
openai.api_key = "YOUR_API_KEY_HERE"

def process_directory(path):
    file_info = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_info.append((file_path, file, content))
    return file_info

def translate_content(content, target_language="Turkish"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}."},
                {"role": "user", "content": content}
            ],
            max_tokens=13000,  # 16k model için güvenli bir sınır
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Çeviri sırasında hata oluştu: {e}")
        return None

def chunk_content(content, chunk_size=4000):
    return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

# Ana klasör yolu
main_folder = r"C:\path\to\your\main\folder"

# İşlemi çalıştır
file_info = process_directory(main_folder)

print(f"Toplam {len(file_info)} dosya bulundu.")

# Tüm dosyaları çevirme
for file_path, file_name, content in tqdm(file_info, desc="Dosyalar çevriliyor"):
    print(f"\nÇevriliyor: {file_name}")
    
    chunks = chunk_content(content)
    translated_chunks = []
    
    for chunk in tqdm(chunks, desc="Parçalar çevriliyor", leave=False):
        translated_chunk = translate_content(chunk)
        if translated_chunk:
            translated_chunks.append(translated_chunk)
        else:
            print(f"'{file_name}' dosyasının bir parçası çevrilemedi.")
    
    if translated_chunks:
        translated_content = " ".join(translated_chunks)
        
        # Çevrilmiş içeriği kaydetme
        original_dir = os.path.dirname(file_path)
        output_folder = os.path.join(original_dir, "translated")
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f"translated_{file_name}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        print(f"Çevrilmiş dosya '{output_path}' yoluna kaydedildi.")
    else:
        print(f"'{file_name}' dosyası çevrilemedi.")

print("\nTüm çeviriler tamamlandı.")
