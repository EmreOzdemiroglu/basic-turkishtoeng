import os
from openai import OpenAI

client = OpenAI(api_key="")


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
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}."},
            {"role": "user", "content": content}
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Çeviri sırasında hata oluştu: {e}")
        return None


main_folder = r"/mnt/c/Users/ozdem/Desktop/MEF"
contents, names = process_directory(main_folder)

print(f"Toplam {len(contents)} dosya bulundu.")

if contents:
    print(names)
    index = int(input("İndex numarası gir"))  
    original_content = contents[index]
    file_name = names[index]

    print(f"\n{file_name} dosyasının orijinal içeriği:")
    print(original_content)

    print("\nÇeviriliyor...")
    translated_content = translate_content(original_content)

    if translated_content:
        print(f"\n{file_name} dosyasının çevrilmiş içeriği:")
        print(translated_content)

        output_folder = os.path.join(main_folder, "translated")
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f"translated_{file_name}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        print(f"\nÇevrilmiş dosya '{output_path}' yoluna kaydedildi.")
    else:
        print("Çeviri başarısız .")
else:
    print("klasörde hiç .txt dosyası bulunamadı.")

if 'translated_content' in locals():
    print("\niçerik örneği:")
    print(translated_content[:100] + "...")  
