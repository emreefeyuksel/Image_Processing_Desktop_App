# Image Processing Application (COMP 4360 Midterm Project)

![Python](https://img.shields.io/badge/Python-3.x-blue) ![OpenCV](https://img.shields.io/badge/OpenCV-Library-green) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)

An advanced desktop image processing application developed using **Python**, **OpenCV**, and **Tkinter**. [cite_start]This project allows users to perform various image manipulation techniques including affine transformations, intensity adjustments, spatial filtering, and morphological operations with a user-friendly dark-themed interface[cite: 1, 4].

---

## 🇬🇧 English Description

### 📥 Download Executable
You can download the compiled `.exe` file directly and run it without installing Python:
👉 **[Download Image Processing App (.exe)](https://drive.google.com/file/d/1dzMEdD2K2fpmViyF0wFHKf_cRlUdFwm6/view?usp=sharing)**

### 🚀 Features
[cite_start]The application features a dual-panel display (Original vs. Result) and supports the following operations[cite: 3, 38]:

* [cite_start]**workflow Integration:** "Commit Result" button allows you to set the processed image as the new original for iterative editing[cite: 11, 21].
* [cite_start]**Basic Operations:** Grayscale conversion, Flip (Horizontal/Vertical), Rotate 90° CW[cite: 45, 46].
* [cite_start]**Affine Transformations:** * Rotation (Custom angle), Scaling (X/Y), Translation (dx, dy), Shearing[cite: 48].
* [cite_start]**Intensity Transformations:** * Negative Image, Contrast Stretching ($\alpha$: 0.5-3.0), Gamma Correction ($\gamma$: 0.1-5.0)[cite: 49].
* **Spatial Filters:** * Mean, Gaussian (adjustable $\sigma$), Median, Laplacian, Sobel (X/Y). 
    * [cite_start]Adjustable Kernel Size (3, 5, 7)[cite: 50, 56].
* **Histogram & Morphology:** * Histogram Visualization & Equalization.
    * Global & Otsu Thresholding.
    * [cite_start]Erode, Dilate, Open, Close (with iteration control)[cite: 52, 54].

### ⚠️ Known Limitations
* [cite_start]**File Names:** Files with Turkish characters (ğ, ü, ş, ı, ö, ç) cannot be opened due to encoding limitations[cite: 60].
* [cite_start]**Display:** Images are resized to 750x750px for display purposes, but saved files preserve original resolution[cite: 58].
* [cite_start]**Formats:** Supports JPG, PNG, BMP, TIF[cite: 59].

---

## 🇹🇷 Türkçe Açıklama

### 📥 Uygulamayı İndir
Derlenmiş `.exe` dosyasını indirerek Python kurulumuna gerek kalmadan çalıştırabilirsiniz:
👉 **[Görüntü İşleme Uygulamasını İndir (.exe)](https://drive.google.com/file/d/1dzMEdD2K2fpmViyF0wFHKf_cRlUdFwm6/view?usp=sharing)**

### 🚀 Özellikler
[cite_start]Uygulama, orijinal ve işlem görmüş görüntüyü yan yana gösteren çift panelli modern bir arayüze sahiptir[cite: 4].

* [cite_start]**İş Akışı (Workflow):** "Commit Result" özelliği ile işlenmiş görüntüyü orijinalin yerine koyarak üst üste işlemler yapabilirsiniz[cite: 21].
* [cite_start]**Temel İşlemler:** Gri tonlama (Grayscale), Çevirme (Yatay/Dikey), 90° Döndürme[cite: 46].
* [cite_start]**Afin Dönüşümler:** * Döndürme (Özel açı), Ölçekleme (Scale), Öteleme (Translate), Kesme (Shear)[cite: 48].
* [cite_start]**Yoğunluk Dönüşümleri:** * Negatif görüntü, Kontrast Germe ($\alpha$: 0.5-3.0), Gama Düzeltme ($\gamma$: 0.1-5.0)[cite: 49].
* **Uzamsal Filtreler:** * Ortalama (Mean), Gaussian (ayarlanabilir $\sigma$), Medyan, Laplacian, Sobel (X/Y).
    * [cite_start]Ayarlanabilir Çekirdek (Kernel) Boyutu (3, 5, 7)[cite: 50, 56].
* **Histogram ve Morfoloji:** * Histogram Görüntüleme ve Eşitleme.
    * Global ve Otsu Eşikleme (Threshold).
    * [cite_start]Erode (Aşındırma), Dilate (Yayma), Açma ve Kapama işlemleri[cite: 52, 54].

### ⚠️ Bilinen Sınırlamalar
* [cite_start]**Dosya İsimleri:** Kodlama sınırlamaları nedeniyle dosya adında Türkçe karakter (ğ, ü, ş, ı, ö, ç) bulunan görseller açılamamaktadır[cite: 60].
* [cite_start]**Görüntüleme:** Görseller ekrana sığması için 750x750px boyutuna yeniden boyutlandırılır ancak kaydedilen dosyalar orijinal çözünürlüğünü korur[cite: 58].
* [cite_start]**Formatlar:** JPG, PNG, BMP, TIF formatlarını destekler[cite: 59].

---

### 👨‍💻 Author / Yazar
**Emre Efe Yüksel** GitHub: [@emreefeyuksel](https://github.com/emreefeyuksel)
[cite_start]Date: November 2025 [cite: 2]
