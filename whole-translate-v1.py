import os
from openai import OpenAI

client = OpenAI(api_key="")
from tqdm import tqdm


def process_directory(path):
    file_contents = []
    file_names = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_contents.append(content)
                file_names.append(file)

    return file_contents, file_names

def translate_content(content, target_language="English"):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}."},
            {"role": "user", "content": content}
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Çeviri sırasında hata oluştu: {e}")
        return None


main_folder = r"/mnt/c/Users/ozdem/Desktop/MEF"
contents, names = process_directory(main_folder)

print(f"Toplam {len(contents)} dosya işlendi.")

translated_contents = []
for content in tqdm(contents, desc="Dosyalar çevriliyor"):
    translated = translate_content(content)
    translated_contents.append(translated)

output_folder = os.path.join(main_folder, "translated")
os.makedirs(output_folder, exist_ok=True)

for name, translated_content in zip(names, translated_contents):
    if translated_content:
        output_path = os.path.join(output_folder, f"translated_{name}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)

print(f"\nÇevrilmiş dosyalar '{output_folder}' klasörüne kaydedildi.")

index = 0  
if 0 <= index < len(contents):
    print(f"\n{names[index]} dosyasının orijinal içeriği:")
    print(contents[index])
    print(f"\n{names[index]} dosyasının çevrilmiş içeriği:")
    print(translated_contents[index])
else:
    print("Geçersiz indeks!")
