# Image Processing Application (COMP 4360 Midterm Project)

<p align="center">
  <a href="#english"><strong>🇬🇧 English Description</strong></a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#turkish"><strong>🇹🇷 Türkçe Açıklama</strong></a>
</p>

<p align="center">
  <img src="screenshot.jpg" alt="Image Processing App Interface" width="100%">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.x-blue" alt="Python">
    <img src="https://img.shields.io/badge/OpenCV-Library-green" alt="OpenCV">
    <img src="https://img.shields.io/badge/GUI-Tkinter-orange" alt="Tkinter">
</p>

An advanced desktop image processing application developed using **Python**, **OpenCV**, and **Tkinter**. This project allows users to perform various image manipulation techniques including affine transformations, intensity adjustments, spatial filtering, and morphological operations with a user-friendly dark-themed interface.

---

<div id="english"></div>

## 🇬🇧 English Description

### 📥 Download Executable
You can download the compiled `.exe` file directly and run it without installing Python:
👉 **[Download Image Processing App (.exe)](https://drive.google.com/file/d/1dzMEdD2K2fpmViyF0wFHKf_cRlUdFwm6/view?usp=sharing)**

### 🚀 Features
The application features a dual-panel display (Original vs. Result) and supports the following operations:

* **Workflow Integration:** "Commit Result" button allows you to set the processed image as the new original for iterative editing.
* **Basic Operations:**
  * Grayscale conversion
  * Flip (Horizontal/Vertical)
  * Rotate 90° CW
* **Affine Transformations:**
  * Rotation (Custom angle)
  * Scaling (X/Y)
  * Translation (dx, dy)
  * Shearing
* **Intensity Transformations:**
  * Negative Image
  * Contrast Stretching ($\alpha$: 0.5-3.0)
  * Gamma Correction ($\gamma$: 0.1-5.0)
* **Spatial Filters:**
  * Mean, Gaussian (adjustable $\sigma$), Median, Laplacian, Sobel (X/Y)
  * Adjustable Kernel Size (3, 5, 7)
* **Histogram & Morphology:**
  * Histogram Visualization & Equalization
  * Global & Otsu Thresholding
  * Erode, Dilate, Open, Close (with iteration control)

### ⚠️ Known Limitations
* **File Names:** Files with Turkish characters (ğ, ü, ş, ı, ö, ç) cannot be opened due to encoding limitations.
* **Display:** Images are resized to 750x750px for display purposes, but saved files preserve original resolution.
* **Formats:** Supports JPG, PNG, BMP, TIF.

---

<div id="turkish"></div>

## 🇹🇷 Türkçe Açıklama

### 📥 Uygulamayı İndir
Derlenmiş `.exe` dosyasını indirerek Python kurulumuna gerek kalmadan çalıştırabilirsiniz:
👉 **[Görüntü İşleme Uygulamasını İndir (.exe)](https://drive.google.com/file/d/1dzMEdD2K2fpmViyF0wFHKf_cRlUdFwm6/view?usp=sharing)**

### 🚀 Özellikler
Uygulama, orijinal ve işlem görmüş görüntüyü yan yana gösteren çift panelli modern bir arayüze sahiptir.

* **İş Akışı (Workflow):** "Commit Result" özelliği ile işlenmiş görüntüyü orijinalin yerine koyarak üst üste işlemler yapabilirsiniz.
* **Temel İşlemler:**
  * Gri tonlama (Grayscale)
  * Çevirme (Yatay/Dikey)
  * 90° Döndürme
* **Afin Dönüşümler:**
  * Döndürme (Özel açı)
  * Ölçekleme (Scale)
  * Öteleme (Translate)
  * Kesme (Shear)
* **Yoğunluk Dönüşümleri:**
  * Negatif görüntü
  * Kontrast Germe ($\alpha$: 0.5-3.0)
  * Gama Düzeltme ($\gamma$: 0.1-5.0)
* **Uzamsal Filtreler:**
  * Ortalama (Mean), Gaussian (ayarlanabilir $\sigma$), Medyan, Laplacian, Sobel (X/Y)
  * Ayarlanabilir Çekirdek (Kernel) Boyutu (3, 5, 7)
* **Histogram ve Morfoloji:**
  * Histogram Görüntüleme ve Eşitleme
  * Global ve Otsu Eşikleme (Threshold)
  * Erode (Aşındırma), Dilate (Yayma), Açma ve Kapama işlemleri

### ⚠️ Bilinen Sınırlamalar
* **Dosya İsimleri:** Kodlama sınırlamaları nedeniyle dosya adında Türkçe karakter (ğ, ü, ş, ı, ö, ç) bulunan görseller açılamamaktadır.
* **Görüntüleme:** Görseller ekrana sığması için 750x750px boyutuna yeniden boyutlandırılır ancak kaydedilen dosyalar orijinal çözünürlüğünü korur.
* **Formatlar:** JPG, PNG, BMP, TIF formatlarını destekler.

---

### 👨‍💻 Author / Yazar
**Emre Efe Yüksel**
GitHub: [@emreefeyuksel](https://github.com/emreefeyuksel)
Date: November 2025
