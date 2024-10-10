import random
import json

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_keys():
    p = q = 0
    while not is_prime(p):
        p = random.randint(100, 300)
    while not is_prime(q) or p == q:
        q = random.randint(100, 300)
    
    n = p * q
    phi = (p-1) * (q-1)
    
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt_rsa(plaintext, public_key):
    key, n = public_key
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt_rsa(ciphertext, private_key):
    key, n = private_key
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)

# Anahtar değerlerini bir dosyada sakla
def anahtar_kaydet(public_key, private_key, anahtar_dosya):
    keys = {
        "public_key": public_key,
        "private_key": private_key
    }
    with open(anahtar_dosya, "w") as file:
        json.dump(keys, file)
    print(f"Anahtarlar {anahtar_dosya} dosyasına kaydedildi.")

# Anahtar değerlerini dosyadan yükle
def anahtar_yukle(anahtar_dosya):
    try:
        with open(anahtar_dosya, "r") as file:
            keys = json.load(file)
            return keys["public_key"], keys["private_key"]
    except FileNotFoundError:
        print("Anahtar dosyası bulunamadı.")
        return None, None

# Dosya şifreleme fonksiyonu
def dosya_sifrele(dosya_yolu, sifreli_dosya_uzantisi, anahtar_dosya):
    try:
        # Anahtar üret ve kaydet
        public_key, private_key = generate_keys()
        anahtar_kaydet(public_key, private_key, anahtar_dosya)

        # Dosya ikili modda okunur
        with open(dosya_yolu, "rb") as file:
            content = file.read()

        # Dosya içeriğini string olarak kodla
        content_str = content.decode("latin1")

        # Şifreleme işlemi
        encrypted_msg = encrypt_rsa(content_str, public_key)
        sifreli_dosya_yolu = f"sifreli_dosya.{sifreli_dosya_uzantisi}"
        with open(sifreli_dosya_yolu, "w", encoding="utf-8") as file:
            file.write(' '.join(map(str, encrypted_msg)))
        print(f"Şifreleme tamamlandı! Şifreli dosya: {sifreli_dosya_yolu}")
    
    except FileNotFoundError:
        print("Hata: Dosya bulunamadı.")
    except Exception as e:
        print(f"Hata: {str(e)}")

# Dosya çözme fonksiyonu
def dosya_coz(sifreli_dosya_yolu, cozulmus_dosya_uzantisi, anahtar_dosya):
    try:
        # Anahtarları dosyadan yükle
        public_key, private_key = anahtar_yukle(anahtar_dosya)
        if public_key is None or private_key is None:
            print("Anahtarlar yüklenemedi, şifre çözme işlemi gerçekleştirilemiyor.")
            return

        # Şifre çözme işlemi
        with open(sifreli_dosya_yolu, "r", encoding="utf-8") as file:
            encrypted_data = list(map(int, file.read().split()))
        
        decrypted_msg = decrypt_rsa(encrypted_data, private_key)

        # Çözülen veriyi binary hale getir
        decrypted_bytes = decrypted_msg.encode("latin1")
        
        cozulmus_dosya_yolu = f"cozulmus_dosya.{cozulmus_dosya_uzantisi}"
        with open(cozulmus_dosya_yolu, "wb") as file:
            file.write(decrypted_bytes)
        print(f"Şifre çözme tamamlandı! Çözülen dosya: {cozulmus_dosya_yolu}")
    
    except FileNotFoundError:
        print("Hata: Dosya bulunamadı.")
    except Exception as e:
        print(f"Hata: {str(e)}")