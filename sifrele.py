import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import numpy as np

alfabe = ['a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h',
          'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö', 'p',
          'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z']

def turkce_kucult(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()

# --- Şifreleme Fonksiyonları ---
def kaydirma_sifrele(metin, anahtar):
    return ''.join(
        alfabe[(alfabe.index(h) + anahtar) % len(alfabe)] if h in alfabe else h for h in metin)

def dogrusal_sifrele(metin, a, b):
    return ''.join(
        alfabe[(a * alfabe.index(h) + b) % len(alfabe)] if h in alfabe else h for h in metin)

def yer_degistirme_sifrele(metin):
    anahtar_alfabe = alfabe.copy()
    random.shuffle(anahtar_alfabe)
    sifreli = ''.join(
        anahtar_alfabe[alfabe.index(h)] if h in alfabe else h for h in metin)
    return sifreli, anahtar_alfabe

def permutasyon_sifrele(metin, anahtar):
    blok_boyutu = len(anahtar)
    eksik = blok_boyutu - len(metin) % blok_boyutu
    metin += 'x' * eksik if eksik != blok_boyutu else ''
    sifreli = ''
    for i in range(0, len(metin), blok_boyutu):
        blok = metin[i:i+blok_boyutu]
        sifreli += ''.join(blok[j-1] for j in anahtar)
    return sifreli

def sayisal_yerdegistirme_sifrele(metin, k):
    satir = math.ceil(len(metin)/k)
    matris = [['x']*k for _ in range(satir)]
    idx = 0
    for i in range(satir):
        for j in range(k):
            if idx < len(metin):
                matris[i][j] = metin[idx]
                idx += 1
    return ''.join(matris[r][c] for c in range(k) for r in range(satir))

def rota_sifrele(metin, k):
    satir = math.ceil(len(metin)/k)
    matris = [['x']*k for _ in range(satir)]
    idx = 0
    for i in range(satir):
        for j in range(k):
            if idx < len(metin):
                matris[i][j] = metin[idx]
                idx += 1
    spiral = []
    top, bottom, left, right = 0, satir-1, 0, k-1
    while top <= bottom and left <= right:
        for i in range(bottom, top-1, -1): spiral.append(matris[i][left])
        left += 1
        for j in range(left, right+1): spiral.append(matris[top][j])
        top += 1
        for i in range(top, bottom+1): spiral.append(matris[i][right])
        right -= 1
        for j in range(right, left-1, -1): spiral.append(matris[bottom][j])
        bottom -= 1
    return ''.join(spiral)

def zigzag_sifrele(metin, s):
    if s == 1 or s >= len(metin):
        return metin
    zigzag = ['' for _ in range(s)]
    row, down = 0, True
    for c in metin:
        zigzag[row] += c
        if row == 0:
            down = True
        elif row == s - 1:
            down = False
        row += 1 if down else -1
    return ''.join(zigzag)

def vigenere_sifrele(metin, anahtar):
    anahtar = turkce_kucult(''.join(h for h in anahtar if h in alfabe))
    return ''.join(alfabe[(alfabe.index(metin[i]) + alfabe.index(anahtar[i % len(anahtar)])) % len(alfabe)] for i in range(len(metin)))

def hill_encrypt(metin, parametre):
    # Matris girişini (örnek: "1,32,10;5,6,4;4,6,9") 3x3 numpy matrisine çevir
    try:
        satirlar = parametre.strip().split(";")
        key_matrix = np.array([list(map(int, satir.split(","))) for satir in satirlar])
        if key_matrix.shape != (3, 3):
            raise ValueError("Anahtar matrisi 3x3 olmalı.")
    except Exception:
        raise ValueError("Parametre 1'e 3x3 matris giriniz. Örn: 1,32,10;5,6,4;4,6,9")

    # Alfabe dizini listesi
    numbers = [alfabe.index(c) for c in metin if c in alfabe]

    # 3'ün katı yap
    if len(numbers) % 3 != 0:
        numbers += [0] * (3 - len(numbers) % 3)

    result = []
    for i in range(0, len(numbers), 3):
        block = np.dot(key_matrix, np.array(numbers[i:i+3]).reshape(3, 1)) % len(alfabe)
        result.extend(block.flatten().astype(int))

    return ''.join(alfabe[n] for n in result)



def four_square_sifrele(metin):
    alfabe = "abcçdefgğhıijklmnoöprsştuüvyzx"  # Türkçe alfabe (x dahil)
    TL = [alfabe[i:i + 6] for i in range(0, 30, 6)]
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

    m = ''.join(h for h in metin if h in alfabe)
    if len(m) % 2 != 0:
        m += 'x'

    result = ''

    def pos(matrix, ch):
        for i, row in enumerate(matrix):
            if ch in row:
                return i, row.index(ch)

    for i in range(0, len(m), 2):
        a, b = m[i], m[i + 1]
        r1, c1 = pos(TL, a)
        r2, c2 = pos(BR, b)
        result += TR[r1][c2] + BL[r2][c1]

    return result


# --- GUI Kodu ---
def sifrele():
    metin_giris = metin_entry.get()
    temiz_metin = turkce_kucult(metin_giris)
    metin = ''.join(h for h in temiz_metin if h in alfabe)
    yontem = secim_box.get()
    try:
        if yontem == "Kaydırma":
            sonuc = kaydirma_sifrele(metin, int(param1.get()))
        elif yontem == "Doğrusal":
            sonuc = dogrusal_sifrele(metin, int(param1.get()), int(param2.get()))
        elif yontem == "Yer Değiştirme":
            sonuc, anahtar = yer_degistirme_sifrele(metin)
            anahtar_var.set(''.join(anahtar))
        elif yontem == "Permütasyon":
            anahtar = list(map(int, param1.get().split()))
            sonuc = permutasyon_sifrele(metin, anahtar)
        elif yontem == "Sayısal Yer Değiştirme":
            sonuc = sayisal_yerdegistirme_sifrele(metin, int(param1.get()))
        elif yontem == "Rota":
            sonuc = rota_sifrele(metin, int(param1.get()))
        elif yontem == "Zigzag":
            sonuc = zigzag_sifrele(metin, int(param1.get()))
        elif yontem == "Vigenère":
            sonuc = vigenere_sifrele(metin, param1.get())
        elif yontem == "Hill":
            sonuc = hill_encrypt(metin, param1.get())

        elif yontem == "Four Square":
            sonuc = four_square_sifrele(metin)
        else:
            sonuc = "Yöntem bulunamadı."
        sonuc_var.set(sonuc)
    except Exception as e:
        messagebox.showerror("Hata", str(e))

def kopyala_anahtar():
    root.clipboard_clear()
    root.clipboard_append(anahtar_var.get())
    root.update()
    messagebox.showinfo("Kopyalandı", "Anahtar panoya kopyalandı.")

root = tk.Tk()
root.title("Şifreleme Uygulaması")
root.geometry("550x500")

ttk.Label(root, text="Metin:").pack()
metin_entry = ttk.Entry(root, width=60)
metin_entry.pack(pady=5)

yontemler = ["Kaydırma", "Doğrusal", "Yer Değiştirme", "Permütasyon", "Sayısal Yer Değiştirme",
             "Rota", "Zigzag", "Vigenère", "Hill", "Four Square"]

ttk.Label(root, text="Şifreleme Yöntemi:").pack()
secim_box = ttk.Combobox(root, values=yontemler, state="readonly")
secim_box.set(yontemler[0])
secim_box.pack(pady=5)

param1 = tk.StringVar()
param2 = tk.StringVar()

ttk.Label(root, text="Parametre 1 (Anahtar / a / Anahtar kelime):").pack()
ttk.Entry(root, textvariable=param1).pack()

ttk.Label(root, text="Parametre 2 (b):").pack()
ttk.Entry(root, textvariable=param2).pack()

ttk.Button(root, text="Şifrele", command=sifrele).pack(pady=10)

sonuc_var = tk.StringVar()
ttk.Label(root, text="Şifrelenmiş Metin:").pack()
ttk.Entry(root, textvariable=sonuc_var, width=60, state="readonly").pack(pady=5)

anahtar_var = tk.StringVar()
ttk.Label(root, text="Anahtar:").pack()
anahtar_entry = ttk.Entry(root, textvariable=anahtar_var, width=60, state="readonly")
anahtar_entry.pack(pady=2)

ttk.Button(root, text="Anahtarı Kopyala", command=kopyala_anahtar).pack(pady=2)

root.mainloop()