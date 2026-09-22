import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np

alfabe = ['a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h',
          'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö', 'p',
          'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z']
inverse_alphabet = {i: harf for i, harf in enumerate(alfabe)}



# --- Yardımcı Fonksiyonlar (Hill için) ---
def text_to_numbers(text):
    numbers = []
    for char in text.lower():
        if char in alfabe:
            numbers.append(alfabe.index(char))
    return numbers

def numbers_to_text(numbers):
    text = ''.join(inverse_alphabet[num] for num in numbers)
    return text

def mod_inv(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

# --- Şifre Çözme Fonksiyonları ---
def kaydirma_coz(metin, anahtar):
    return ''.join(
        alfabe[(alfabe.index(h.lower()) - anahtar) % len(alfabe)].upper() if h.isupper()
        else alfabe[(alfabe.index(h.lower()) - anahtar) % len(alfabe)]
        if h.lower() in alfabe else h for h in metin)

def dogrusal_coz(metin, a, b):
    mod_inv_a = pow(a, -1, len(alfabe))
    return ''.join(
        alfabe[(mod_inv_a * (alfabe.index(h.lower()) - b)) % len(alfabe)].upper() if h.isupper()
        else alfabe[(mod_inv_a * (alfabe.index(h.lower()) - b)) % len(alfabe)]
        if h.lower() in alfabe else h for h in metin)

def yer_degistirme_coz(metin, anahtar_alfabe):
    return ''.join(
        alfabe[anahtar_alfabe.index(h.lower())].upper() if h.isupper()
        else alfabe[anahtar_alfabe.index(h.lower())]
        if h.lower() in anahtar_alfabe else h for h in metin)

def permutasyon_sifre_coz(sifreli_metin, anahtar):
    blok_boyutu = len(anahtar)
    metin = ""
    for i in range(0, len(sifreli_metin), blok_boyutu):
        blok = sifreli_metin[i:i + blok_boyutu]
        orijinal_blok = [''] * blok_boyutu
        for j, pozisyon in enumerate(anahtar):
            orijinal_blok[pozisyon - 1] = blok[j]
        metin += ''.join(orijinal_blok)
    return metin

def sayisal_yerdegistirme_coz(metin, k):
    satir = math.ceil(len(metin)/k)
    matris = [['x']*k for _ in range(satir)]
    idx = 0
    for j in range(k):
        for i in range(satir):
            if idx < len(metin):
                matris[i][j] = metin[idx]
                idx += 1
    return ''.join(''.join(r) for r in matris).rstrip('x')

def vigenere_coz(metin, anahtar):
    metin = ''.join(h.lower() for h in metin if h.lower() in alfabe)
    anahtar = ''.join(h.lower() for h in anahtar if h.lower() in alfabe)
    return ''.join(alfabe[(alfabe.index(metin[i]) - alfabe.index(anahtar[i % len(anahtar)])) % len(alfabe)]
                   for i in range(len(metin)))

def hill_decrypt(encrypted_text,anahtar):
    key_matrix = np.array([[int(num) for num in row.split(',')] for row in anahtar.split(';')])
    n = len(alfabe)
    try:
        det = int(round(np.linalg.det(key_matrix)))
        mod_det = det % n
        mod_inv_det = mod_inv(mod_det, n)
        if mod_inv_det is None:
            raise ValueError("Anahtar matrisinin modüler tersi bulunamadı.")
        adj_matrix = np.round(np.linalg.inv(key_matrix) * det).astype(int)
        inv_key_matrix = (adj_matrix * mod_inv_det) % n

        encrypted_numbers = text_to_numbers(encrypted_text)
        if len(encrypted_numbers) % 3 != 0:
            encrypted_numbers += [0] * (3 - len(encrypted_numbers) % 3)

        decrypted_numbers = []
        for i in range(0, len(encrypted_numbers), 3):
            block = np.array(encrypted_numbers[i:i + 3]).reshape(3, 1)
            decrypted_block = np.dot(inv_key_matrix, block) % n
            decrypted_numbers.extend(decrypted_block.flatten().astype(int))

        return numbers_to_text(decrypted_numbers)
    except np.linalg.LinAlgError:
        raise ValueError("Anahtar matrisi tekil (singular). Tersi alınamaz.")
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise Exception("Hill şifre çözmede bir hata oluştu: " + str(e))


def four_square_coz(metin):
    alfabea = ['a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h',
              'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö', 'p',
              'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z', 'x']

    TL = [alfabea[i:i + 6] for i in range(0, 30, 6)]
    TR = [['ğ', 'f', 't', 'j', 'p', 'm'],
          ['r', 'a', 'ü', 'ş', 'ö', 'ı'],
          ['o', 'l', 'i', 'v', 'z', 'c'],
          ['d', 'n', 'g', 'b', 'h', 'y'],
          ['u', 'ç', 's', 'k', 'x', 'e']]
    BL = [['c', 'ö', 'h', 't', 'k', 'g'],
          ['ü', 'm', 'j', 'f', 'v', 'ş'],
          ['e', 'i', 'b', 'y', 'd', 'o'],
          ['r', 'x', 'ğ', 'z', 's', 'ç'],
          ['l', 'a', 'u', 'p', 'ı', 'n']]
    BR = TL

    m = ''.join(h.casefold() for h in metin if h.casefold() in alfabea)

    result = ''

    def pos(matrix, ch):
        for i, row in enumerate(matrix):
            if ch in row:
                return i, row.index(ch)

    for i in range(0, len(m), 2):
        a, b = m[i], m[i + 1]
        r1, c2 = pos(TR, a)
        r2, c1 = pos(BL, b)
        result += TL[r1][c1] + BR[r2][c2]

    return result




def rota_coz(sifreli_metin, k):
    L = len(sifreli_metin)
    satir = math.ceil(L / k)
    matris = [['' for _ in range(k)] for _ in range(satir)]
    index = 0
    top, bottom = 0, satir - 1
    left, right = 0, k - 1

    while top <= bottom and left <= right:
        for i in range(bottom, top - 1, -1):
            if index < L:
                matris[i][left] = sifreli_metin[index]
                index += 1
        left += 1
        for j in range(left, right + 1):
            if index < L:
                matris[top][j] = sifreli_metin[index]
                index += 1
        top += 1
        for i in range(top, bottom + 1):
            if index < L:
                matris[i][right] = sifreli_metin[index]
                index += 1
        right -= 1
        for j in range(right, left - 1, -1):
            if index < L:
                matris[bottom][j] = sifreli_metin[index]
                index += 1
        bottom -= 1

    return ''.join(matris[i][j] for i in range(satir) for j in range(k) if matris[i][j] != '')

def zigzag_coz(metin, satir_sayisi):
    if satir_sayisi == 1 or satir_sayisi >= len(metin):
        return metin
    sutun_sayisi = len(metin)
    zigzag = [['' for _ in range(sutun_sayisi)] for _ in range(satir_sayisi)]

    satir = 0
    yukari_asagi = False
    for col in range(sutun_sayisi):
        zigzag[satir][col] = '*'
        if satir == 0 or satir == satir_sayisi - 1:
            yukari_asagi = not yukari_asagi
        satir += 1 if yukari_asagi else -1

    index = 0
    for i in range(satir_sayisi):
        for j in range(sutun_sayisi):
            if zigzag[i][j] == '*' and index < len(metin):
                zigzag[i][j] = metin[index]
                index += 1

    cozulmus = []
    satir = 0
    yukari_asagi = False
    for col in range(sutun_sayisi):
        cozulmus.append(zigzag[satir][col])
        if satir == 0 or satir == satir_sayisi - 1:
            yukari_asagi = not yukari_asagi
        satir += 1 if yukari_asagi else -1

    return ''.join(cozulmus)

# --- GUI ---
def coz():
    metin = metin_entry.get()
    yontem = secim_box.get()
    try:
        if yontem == "Kaydırma":
            sonuc = kaydirma_coz(metin, int(param1.get()))
        elif yontem == "Doğrusal":
            sonuc = dogrusal_coz(metin, int(param1.get()), int(param2.get()))
        elif yontem == "Yer Değiştirme":
            anahtar = list(param1.get().strip().lower())
            sonuc = yer_degistirme_coz(metin, anahtar)
        elif yontem == "Permütasyon":
            anahtar = list(map(int, param1.get().split()))
            if sorted(anahtar) != list(range(1, len(anahtar) + 1)):
                sonuc = "Hatalı anahtar: Permütasyon 1'den n'e kadar benzersiz sayılar içermelidir."
            else:
                sonuc = permutasyon_sifre_coz(metin, anahtar)
        elif yontem == "Sayısal Yer Değiştirme":
            sonuc = sayisal_yerdegistirme_coz(metin, int(param1.get()))
        elif yontem == "Vigenère":
            sonuc = vigenere_coz(metin, param1.get())
        elif yontem == "Hill":
            sonuc = hill_decrypt(metin, param1.get())
        elif yontem == "Four Square":
            sonuc = four_square_coz(metin)
        elif yontem == "Rota":
            sonuc = rota_coz(metin, int(param1.get()))
        elif yontem == "Zigzag":
            sonuc = zigzag_coz(metin, int(param1.get()))
        else:
            sonuc = "Yöntem desteklenmiyor."
        sonuc_var.set(sonuc)
    except ValueError as ve:
        messagebox.showerror("Hata", str(ve))
    except Exception as e:
        messagebox.showerror("Hata", str(e))

root = tk.Tk()
root.title("Çözme Uygulaması")
root.geometry("500x500")

ttk.Label(root, text="Şifreli Metin:").pack()
metin_entry = ttk.Entry(root, width=60)
metin_entry.pack(pady=5)

yontemler = ["Kaydırma", "Doğrusal", "Yer Değiştirme", "Permütasyon",
             "Sayısal Yer Değiştirme", "Vigenère", "Hill", "Four Square", "Rota", "Zigzag"]

ttk.Label(root, text="Çözme Yöntemi:").pack()
secim_box = ttk.Combobox(root, values=yontemler, state="readonly")
secim_box.set(yontemler[0])
secim_box.pack(pady=5)

param1 = tk.StringVar()
param2 = tk.StringVar()

ttk.Label(root, text="Parametre 1 (Anahtar / a / kelime / satır sayısı):").pack()
ttk.Entry(root, textvariable=param1).pack()

ttk.Label(root, text="Parametre 2 (b):").pack()
ttk.Entry(root, textvariable=param2).pack()

ttk.Button(root, text="Çöz", command=coz).pack(pady=10)

sonuc_var = tk.StringVar()
ttk.Label(root, text="Çözülmüş Metin:").pack()
ttk.Entry(root, textvariable=sonuc_var, width=60, state="readonly").pack(pady=5)

root.mainloop()