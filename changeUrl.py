import os

# Ana dizin yolu
dir = r"C:\Users\Gedik\Desktop\gray\on"

# Ana dizindeki tüm klasörleri listele
folders = os.listdir(dir)
for folder in folders:
    # Klasördeki tüm dosyaları listele
    img_list = os.listdir(os.path.join(dir, folder))

    for img_name in img_list:
        # '_frame' kelimesine kadar olan kısmı bul
        new_name_prefix = folder  # Yeni isim öneki olarak klasör adını kullan
        suffix = img_name.split("_frame")[1]  # '_frame' sonrasını al

        # Yeni dosya adını oluştur
        new_img_name = f"{new_name_prefix}_frame{suffix}"

        # Dosyayı yeni adıyla yeniden adlandır
        old_path = os.path.join(dir, folder, img_name)
        new_path = os.path.join(dir, folder, new_img_name)
        os.rename(old_path, new_path)
        print(f"Renamed '{img_name}' to '{new_img_name}'")