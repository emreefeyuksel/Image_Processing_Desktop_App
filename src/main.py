import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkthemes import ThemedTk
TITLE_FONT = ("Helvetica", 12, "bold")
SUBTITLE_FONT = ("Helvetica", 10, "bold")

# Global değişkenler
original_image_bgr = None
current_image_bgr = None
current_image_rgb = None  # Görüntüleme için RGB formatı
display_image_tk = None

# Arayüz Boyutları
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 750
IMAGE_PANEL_SIZE = 750
CONTROL_FRAME_WIDTH = 300


class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Processing App by Emre Efe Yüksel")

        try:
            master.set_theme("equilux")  # Şık bir dark tema
        except Exception:
            pass

        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.exit_fullscreen)
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.gamma_scale = None
        self.gamma_label = None
        self.info_label = None

        master.configure(bg="#333333")

        self.create_widgets()

    def exit_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', False)
        #Normal pencere boyutunu da ayarlayabiliriz (opsiyonel)
        #self.master.geometry("1300x750")

    def create_widgets(self):
        control_frame = ttk.Frame(self.master, padding="10", width=CONTROL_FRAME_WIDTH)
        control_frame.pack(side="left", fill="y", expand=False)  #Kontrol paneli sabit kalır
        ttk.Label(control_frame, text="Image Processing App", font=TITLE_FONT).pack(pady=(0, 0))
        ttk.Label(control_frame, text="by Emre Efe Yüksel", font=("Helvetica", 11, "normal")).pack(pady=(0, 10))
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill="x", pady=1)

        # ----------------------------------------------------------------------------------
        # --- BÖLÜM 1: Status Bar ve Separator ---
        # ----------------------------------------------------------------------------------

        # Kontrol Çerçevesinin En Altına Statü Çerçevesi (side="bottom" ile en alta yapışır)
        status_frame = ttk.LabelFrame(control_frame, text="ℹ️ Info & Status", padding="5")
        status_frame.pack(fill="x", pady=(10, 0), side="bottom")

        # Durum/Log Çubuğu (Uygulama mesajları için)
        self.log_label = ttk.Label(status_frame, text="Status: Ready", foreground="white", anchor="w")
        self.log_label.pack(fill="x", pady=2)

        # Görüntü Bilgi Etiketi
        self.info_label = ttk.Label(status_frame, text="Resolution: N/A\nChannels: N/A", anchor="w")
        self.info_label.pack(fill="x", pady=2)

        # Statü Çerçevesinin hemen üstüne yatay bir ayırıcı ekle (Estetik ve görsel ayrım için)
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill="x", pady=10, side="bottom")

        # ----------------------------------------------------------------------------------
        # --- BÖLÜM 2: Görüntü Panelleri ---
        # ----------------------------------------------------------------------------------

        # Sağ Panel (Görüntüler ve Histogram)
        display_frame = ttk.Frame(self.master, padding="10")
        display_frame.pack(side="right", fill="both", expand=True)  # TÜM KALAN ALANI KAPLA

        # Görüntü Gösterim Alanı (image_frame)
        image_frame = ttk.Frame(display_frame)
        image_frame.pack(side="top", fill="both", expand=True)  # image_frame tüm dikey alanı kaplar

        # --- Orijinal Görüntü ve Başlık (Kapsayıcı) ---
        original_container = ttk.Frame(image_frame)
        original_container.pack(side="left", padx=20, anchor='center', expand=True)  # Ortala ve boşluğu genişlet

        # Başlık (FONT Kullanımı)
        ttk.Label(original_container, text="Original Image", anchor="center", font=TITLE_FONT).pack(side="top",
                                                                                                    pady=(0, 5))

        # Orijinal Görüntü Paneli
        self.original_panel = tk.Label(original_container, width=IMAGE_PANEL_SIZE, height=IMAGE_PANEL_SIZE,
                                       relief="sunken", bg="#555555")
        self.original_panel.pack(side="top")

        # --- Sonuç Görüntü ve Başlık (Kapsayıcı) ---
        result_container = ttk.Frame(image_frame)
        result_container.pack(side="left", padx=20, anchor='center', expand=True)  # Ortala ve boşluğu genişlet

        # Başlık (FONT Kullanımı)
        ttk.Label(result_container, text="Result Image", anchor="center", font=TITLE_FONT).pack(side="top", pady=(0, 5))

        # Sonuç Görüntü Paneli
        self.result_panel = tk.Label(result_container, width=IMAGE_PANEL_SIZE, height=IMAGE_PANEL_SIZE, relief="sunken",
                                     bg="#555555")
        self.result_panel.pack(side="top")

        # ----------------------------------------------------------------------------------
        # --- BÖLÜM 3: Kontrol Menüleri (Kalan Orta Alanı Doldurur) ---
        # ----------------------------------------------------------------------------------

        # Menü ve Kontroller (Sekmeler ve Dosya İşlemleri)
        self.create_file_menu(control_frame)
        self.create_operation_tabs(control_frame)

    # --- Dosya İşlemleri ve Temel Menü ---
    def create_file_menu(self, parent):
        file_frame = ttk.LabelFrame(parent, text="File Operations", padding="5")
        file_frame.pack(fill="x", pady=5)

        ttk.Button(file_frame, text="Open Image", command=self.open_image).pack(fill="x", pady=2)
        ttk.Button(file_frame, text="Save Result", command=self.save_image).pack(fill="x", pady=2)
        ttk.Button(file_frame, text="Reset to Original", command=self.reset_image).pack(fill="x", pady=2)

        # Yeni Commit Butonu (Result'ı Original olarak ayarla)
        ttk.Button(file_frame, text="Commit Result (Set Original)", command=self.set_current_as_original).pack(fill="x",
                                                                                                               pady=5)

    def set_current_as_original(self):
        global original_image_bgr, current_image_bgr
        if current_image_bgr is None:
            tk.messagebox.showwarning("Warning", "No processed image to commit.")
            return

        original_image_bgr = current_image_bgr.copy()

        # Görüntü panellerini orijinal görüntüyü güncelleyerek yeniden çiz
        self.display_images(original_image_bgr, current_image_bgr)
        tk.messagebox.showinfo("Success", "Current result set as new original image.")

    def open_image(self):
        global original_image_bgr, current_image_bgr, current_image_rgb
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tif")]
        )
        if not filepath:
            return

        img = cv2.imread(filepath)
        if img is None:
            # self.log_label.config(text="❌ HATA: Görüntü açılamadı.", foreground="red") # Eğer hata logu kullanılacaksa
            tk.messagebox.showerror("Error", "Could not open image.")
            return

        original_image_bgr = img.copy()
        self.reset_image()

        # BİLGİ ETİKETİNİ GÜNCELLE
        h, w = img.shape[:2]
        channels = img.shape[2] if len(img.shape) == 3 else 1
        self.info_label.config(text=f"Resolution: {w}x{h}\nChannels: {channels}")
        self.log_label.config(text="✅ Image loaded successfully.", foreground="lightgreen")
        self.master.after(2000, lambda: self.log_label.config(text="Status: Ready", foreground="white"))

    def save_image(self):
        global current_image_bgr
        if current_image_bgr is None:
            tk.messagebox.showerror("Error", "No processed image to save.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg"), ("BMP file", "*.bmp")]
        )
        if filepath:
            cv2.imwrite(filepath, current_image_bgr)
            tk.messagebox.showinfo("Success", f"Image saved to {filepath}")

    def reset_image(self):
        global original_image_bgr, current_image_bgr, current_image_rgb
        if original_image_bgr is None:
            return

        current_image_bgr = original_image_bgr.copy()
        self.display_images(original_image_bgr, current_image_bgr)

    # --- Görüntüleme Fonksiyonu ---
    def display_images(self, original_bgr, result_bgr):
        # Orijinal Görüntü Gösterimi
        img_orig_rgb = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB)
        img_orig_pil = Image.fromarray(img_orig_rgb)
        img_orig_pil = img_orig_pil.resize((IMAGE_PANEL_SIZE, IMAGE_PANEL_SIZE))
        img_orig_tk = ImageTk.PhotoImage(image=img_orig_pil)
        self.original_panel.config(image=img_orig_tk)
        self.original_panel.image = img_orig_tk

        # Sonuç Görüntüsü Gösterimi
        if len(result_bgr.shape) == 2 or result_bgr.shape[2] == 1:
            img_result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_GRAY2BGR)
        else:
            img_result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)

        img_result_pil = Image.fromarray(img_result_rgb)
        img_result_pil = img_result_pil.resize((IMAGE_PANEL_SIZE, IMAGE_PANEL_SIZE))
        img_result_tk = ImageTk.PhotoImage(image=img_result_pil)
        self.result_panel.config(image=img_result_tk)
        self.result_panel.image = img_result_tk

        global current_image_bgr
        current_image_bgr = result_bgr

    # --- Operasyon Sekmeleri ---
    def create_operation_tabs(self, parent):
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True, pady=5)

        tab_basic = ttk.Frame(notebook)
        notebook.add(tab_basic, text="Basics / Affine")
        self.create_basic_features(tab_basic)

        tab_intensity = ttk.Frame(notebook)
        notebook.add(tab_intensity, text="Intensity")
        self.create_intensity_features(tab_intensity)

        tab_filters = ttk.Frame(notebook)
        notebook.add(tab_filters, text="Filters")
        self.create_filter_features(tab_filters)

        tab_hist_morph = ttk.Frame(notebook)
        notebook.add(tab_hist_morph, text="Hist / Morph")
        self.create_hist_morph_features(tab_hist_morph)

    # Implementasyon fonksiyonları
    def apply_operation(self, operation_func, *args, **kwargs):
        global current_image_bgr
        if current_image_bgr is None:
            self.log_label.config(text="❌ Warning: Please open an image first.", foreground="yellow")
            return

        try:
            result_bgr = operation_func(current_image_bgr.copy(), *args, **kwargs)
            self.display_images(original_image_bgr, result_bgr)

            # BAŞARI LOGU
            self.log_label.config(text=f"✅ Operation Successful: {operation_func.__name__}", foreground="lightgreen")
            self.master.after(2000, lambda: self.log_label.config(text="Status: Ready", foreground="white"))

        except Exception as e:
            # HATA LOGU
            self.log_label.config(text=f"❌ ERROR: An issue occurred during operation: {e}", foreground="red")
            # tk.messagebox.showerror("Error", f"An error occurred: {e}") # Pop-up'ı kaldırdık

    # --- BÖLÜM A: TEMEL İŞLEMLER ---
    def op_grayscale(self, img):
        if len(img.shape) == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    def op_flip(self, img, flip_code):
        return cv2.flip(img, flip_code)

    def op_rotate_90(self, img, rotate_code):
        return cv2.rotate(img, rotate_code)

    # --- BÖLÜM B: AFFINE DÖNÜŞÜMLER ---
    def op_affine_transform(self, img, M):
        h, w = img.shape[:2]
        return cv2.warpAffine(img, M, (w, h))

    def create_basic_features(self, tab):

        # 1. TEMEL OPERASYONLAR GRUBU (LabelFrame)
        basic_op_frame = ttk.LabelFrame(tab, text="Basics", padding="10")
        basic_op_frame.pack(fill="x", pady=5)

        ttk.Button(basic_op_frame, text="Grayscale", command=lambda: self.apply_operation(self.op_grayscale)).pack(
            fill="x", pady=2)
        ttk.Button(basic_op_frame, text="Flip Horizontal", command=lambda: self.apply_operation(self.op_flip, 1)).pack(
            fill="x", pady=2)
        ttk.Button(basic_op_frame, text="Flip Vertical", command=lambda: self.apply_operation(self.op_flip, 0)).pack(
            fill="x", pady=2)
        ttk.Button(basic_op_frame, text="Rotate 90° CW",
                   command=lambda: self.apply_operation(self.op_rotate_90, cv2.ROTATE_90_CLOCKWISE)).pack(fill="x",
                                                                                                          pady=2)

        #AFFINE DÖNÜŞÜMLER GRUBU (LabelFrame)
        affine_section_frame = ttk.LabelFrame(tab, text="📐 Affine Transformations", padding="10")
        affine_section_frame.pack(fill="x", pady=10)

        affine_frame = ttk.Frame(affine_section_frame, padding="5")
        affine_frame.pack(fill="x", pady=5)

        #1. Rotasyon
        ttk.Label(affine_frame, text="Rotation Angle (°):").grid(row=0, column=0, sticky="w")
        self.rot_angle_entry = ttk.Entry(affine_frame, width=5)
        self.rot_angle_entry.insert(0, "45")
        self.rot_angle_entry.grid(row=0, column=1, padx=(0, 5))
        ttk.Button(affine_frame, text="Rotate", command=self.op_rotation).grid(row=0, column=2, padx=5, sticky="ew")

        #2. Ölçekleme
        ttk.Label(affine_frame, text="Scale X, Y (e.g., 1.5, 0.8):").grid(row=1, column=0, sticky="w")
        self.scale_entry = ttk.Entry(affine_frame, width=10)
        self.scale_entry.insert(0, "1.5, 1.5")
        self.scale_entry.grid(row=1, column=1, padx=(0, 5))
        ttk.Button(affine_frame, text="Scale", command=self.op_scale).grid(row=1, column=2, padx=5, sticky="ew")

        #3. Öteleme (Translate)
        ttk.Label(affine_frame, text="Translate Dx, Dy (px):").grid(row=2, column=0, sticky="w")
        self.translate_entry = ttk.Entry(affine_frame, width=10)
        self.translate_entry.insert(0, "50, 50")
        self.translate_entry.grid(row=2, column=1, padx=(0, 5))
        ttk.Button(affine_frame, text="Translate", command=self.op_translate).grid(row=2, column=2, padx=5, sticky="ew")

        #4. Kaydırma (Shear)
        ttk.Label(affine_frame, text="Shear X, Y (e.g., 0.2, 0):").grid(row=3, column=0, sticky="w")
        self.shear_entry = ttk.Entry(affine_frame, width=10)
        self.shear_entry.insert(0, "0.2, 0.0")
        self.shear_entry.grid(row=3, column=1, padx=(0, 5))
        ttk.Button(affine_frame, text="Shear", command=self.op_shear).grid(row=3, column=2, padx=5, sticky="ew")

    def op_rotation(self):
        try:
            angle = float(self.rot_angle_entry.get())
            h, w = current_image_bgr.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            self.apply_operation(self.op_affine_transform, M)
        except ValueError:
            tk.messagebox.showerror("Error", "Rotation angle must be a number.")

    def op_scale(self):
        try:
            scale_x_str, scale_y_str = [x.strip() for x in self.scale_entry.get().split(',')]
            scale_x = float(scale_x_str)
            scale_y = float(scale_y_str)
            M = np.float32([[scale_x, 0, 0], [0, scale_y, 0]])
            self.apply_operation(self.op_affine_transform, M)
        except ValueError:
            tk.messagebox.showerror("Error", "Scale X, Y must be valid numbers (e.g., 1.5, 0.8).")

    def op_translate(self):
        try:
            dx_str, dy_str = [x.strip() for x in self.translate_entry.get().split(',')]
            dx = int(dx_str)
            dy = int(dy_str)
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            self.apply_operation(self.op_affine_transform, M)
        except ValueError:
            tk.messagebox.showerror("Error", "Translate Dx, Dy must be integers.")

    def op_shear(self):
        try:
            shear_x, shear_y = [float(x.strip()) for x in self.shear_entry.get().split(',')]

            # Kaydırma Matrisi
            M = np.float32([[1, shear_x, 0], [shear_y, 1, 0]])

            self.apply_operation(self.op_affine_transform, M)
        except ValueError:
            tk.messagebox.showerror("Error", "Shear X, Y must be valid numbers (e.g., 0.2, 0.0).")

    # --- BÖLÜM C: YOĞUNLUK DÖNÜŞÜMLERİ ---
    def create_intensity_features(self, tab):

        #Yoğunluk Dönüşümlerini LabelFrame içine al
        intensity_frame = ttk.LabelFrame(tab, text="💡 Intensity Transformations", padding="10")
        intensity_frame.pack(fill="x", pady=5)

        ttk.Button(intensity_frame, text="Negative", command=lambda: self.apply_operation(self.op_negative)).pack(
            fill="x", pady=2)

        # --- KONTRAST SLIDERI BAŞLANGICI ---
        ttk.Label(intensity_frame, text="Contrast Factor (α):").pack(pady=5)
        self.contrast_scale = ttk.Scale(intensity_frame, from_=0.5, to=3.0, orient=tk.HORIZONTAL,
                                        command=self.update_contrast_label)
        self.contrast_scale.set(1.0)  # Varsayılan 1.0
        self.contrast_scale.pack(fill="x", pady=2)
        self.contrast_label = ttk.Label(intensity_frame, text=f"α: 1.00")
        self.contrast_label.pack(pady=2)

        ttk.Button(intensity_frame, text="Apply Contrast", command=self.op_apply_contrast).pack(fill="x", pady=5)
        # --- KONTRAST SLIDERI SONU ---

        # Gamma Düzeltme Kaydırıcısı
        ttk.Label(intensity_frame, text="Gamma Correction (γ):").pack(pady=5)
        self.gamma_scale = ttk.Scale(intensity_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL,
                                     command=self.update_gamma_label)
        self.gamma_scale.set(1.0)
        self.gamma_scale.pack(fill="x", pady=2)
        self.gamma_label = ttk.Label(intensity_frame, text=f"γ: 1.00")
        self.gamma_label.pack(pady=2)

        # İşlemi butona bağla
        ttk.Button(intensity_frame, text="Apply Gamma", command=self.op_apply_gamma).pack(fill="x", pady=5)
    def op_negative(self, img):
        return 255 - img

    def op_contrast_stretching(self, img, alpha):
        # Basit Kontrast Ayarı: g(x) = alpha * f(x)
        # alpha > 1: Kontrast artar, alpha < 1: Kontrast azalır.

        # NumPy kullanarak işlemi float yapıp sonra kısıtlamak performansı artırır.
        img_float = img.astype(np.float32)

        # Alfa ile çarpma (Kontrast)
        stretched = img_float * alpha

        # Pikselleri 0-255 aralığına kısıtla ve uint8'e çevir
        return stretched.clip(0, 255).astype(np.uint8)

    def update_contrast_label(self, val):
        """Sadece kaydırıcı değeri değiştikçe kontrast etiketini günceller."""
        alpha = float(val)
        self.contrast_label.config(text=f"α: {alpha:.2f}")

    def op_apply_contrast(self):
        """'Apply Contrast' butonuna basıldığında kontrast işlemini uygular."""
        global current_image_bgr
        if current_image_bgr is None:
            self.log_label.config(text="⚠️ Warning: Please open an image first.", foreground="yellow")
            return

        alpha = float(self.contrast_scale.get())
        # Dinamik parametreyi op_contrast_stretching metoduna gönder
        self.apply_operation(self.op_contrast_stretching, alpha)

    def op_gamma_correction(self, img, gamma):
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(img, table)

    def update_gamma_label(self, val):
        """Sadece kaydırıcı değeri değiştikçe etiketi günceller (İşlem yapmaz)."""
        gamma = float(val)
        self.gamma_label.config(text=f"γ: {gamma:.2f}")

    def op_apply_gamma(self):
        """'Apply Gamma' butonuna basıldığında görüntü işleme işlemini uygular."""
        global current_image_bgr
        if current_image_bgr is None:
            tk.messagebox.showwarning("Warning", "Please open an image first.")
            return

        gamma = float(self.gamma_scale.get())
        self.apply_operation(self.op_gamma_correction, gamma)

    # --- BÖLÜM D: UZAMSAL FİLTRELER ---
    def create_filter_features(self, tab):

        # Filtreleri LabelFrame içine al
        filter_group_frame = ttk.LabelFrame(tab, text="🌀 Spatial Filters", padding="10")
        filter_group_frame.pack(fill="x", pady=5)

        # Kernel Boyutu Kontrolleri
        kernel_control_frame = ttk.Frame(filter_group_frame, padding="5")
        kernel_control_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(kernel_control_frame, text="Kernel Size (Odd, e.g., 3, 5):").grid(row=0, column=0, sticky="w")
        self.kernel_size_entry = ttk.Entry(kernel_control_frame, width=5)
        self.kernel_size_entry.insert(0, "3")
        self.kernel_size_entry.grid(row=0, column=1)

        # Gaussian Sigma Slider
        ttk.Label(filter_group_frame, text="Gaussian Sigma (σ):").pack(pady=(10, 0))
        self.sigma_scale = ttk.Scale(filter_group_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL,
                                     command=self.update_sigma_label)
        self.sigma_scale.set(1.0)
        self.sigma_scale.pack(fill="x", pady=2)
        self.sigma_label = ttk.Label(filter_group_frame, text=f"σ: 1.00")
        self.sigma_label.pack(pady=2)

        # --- Yumuşatma Filtreleri ---
        ttk.Separator(filter_group_frame, orient=tk.HORIZONTAL).pack(fill="x", pady=8)
        ttk.Label(filter_group_frame, text="Smoothing Filters", font=("Helvetica", 9, "bold")).pack(fill="x",
                                                                                                    pady=(0, 2))

        ttk.Button(filter_group_frame, text="Mean/Box", command=self.op_mean_filter).pack(fill="x", pady=2)
        ttk.Button(filter_group_frame, text="Gaussian Filter", command=self.op_apply_gaussian_filter).pack(fill="x",
                                                                                                           pady=2)
        ttk.Button(filter_group_frame, text="Median", command=self.op_median_filter).pack(fill="x", pady=2)

        # --- Kenar Algılama Filtreleri ---
        ttk.Separator(filter_group_frame, orient=tk.HORIZONTAL).pack(fill="x", pady=8)
        ttk.Label(filter_group_frame, text="Edge Detection Filters", font=("Helvetica", 9, "bold")).pack(fill="x",
                                                                                                         pady=(0, 2))

        # Laplacian
        ttk.Button(filter_group_frame, text="Laplacian (3x3)", command=self.op_laplacian_filter).pack(fill="x", pady=2)

        # Sobel X ve Y (Yan Yana)
        sobel_frame = ttk.Frame(filter_group_frame)
        sobel_frame.pack(fill="x", pady=2)

        ttk.Button(sobel_frame, text="Sobel X", command=lambda: self.op_sobel_filter('x')).pack(side="left",
                                                                                                expand=True, fill="x",
                                                                                                padx=(0, 5))
        ttk.Button(sobel_frame, text="Sobel Y", command=lambda: self.op_sobel_filter('y')).pack(side="left",
                                                                                                expand=True, fill="x",
                                                                                                padx=(5, 0))

    def op_apply_gaussian_filter(self):
        """Gaussian filtresini sigma ve ksize değerleriyle uygular."""
        ksize = self.get_kernel_size()
        sigma = float(self.sigma_scale.get())
        if ksize:
            # cv2.GaussianBlur(src, ksize, sigmaX, sigmaY)
            self.apply_operation(cv2.GaussianBlur, (ksize, ksize), sigma, sigma)

    def update_sigma_label(self, val):
        """Sadece kaydırıcı değeri değiştikçe sigma etiketini günceller."""
        sigma = float(val)
        self.sigma_label.config(text=f"σ: {sigma:.2f}")

    def get_kernel_size(self):
        try:
            ksize = int(self.kernel_size_entry.get())
            if ksize % 2 == 0 or ksize <= 1:
                tk.messagebox.showerror("Error", "Kernel size must be an odd number (e.g., 3, 5, 7).")
                return None
            return ksize
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid kernel size.")
            return None

    def op_mean_filter(self):
        ksize = self.get_kernel_size()
        if ksize:
            self.apply_operation(cv2.blur, (ksize, ksize))

    def op_median_filter(self):
        ksize = self.get_kernel_size()
        if ksize:
            self.apply_operation(cv2.medianBlur, ksize)

    def op_laplacian_filter(self):
        def laplacian_func(img):
            gray = self.op_grayscale(img)
            lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
            return cv2.convertScaleAbs(lap)

        self.apply_operation(laplacian_func)

    def op_sobel_filter(self, orientation):
        def sobel_func(img):
            gray = self.op_grayscale(img)
            ksize = self.get_kernel_size() or 3
            if orientation == 'x':
                sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
            elif orientation == 'y':
                sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
            return cv2.convertScaleAbs(sobel)

        self.apply_operation(sobel_func)

    # --- BÖLÜM E & F: HİSTOGRAM VE MORFOLOJİ ---
    def create_hist_morph_features(self, tab):

        # 1. HISTOGRAM OPERATIONS GRUBU (LabelFrame)
        hist_op_frame = ttk.LabelFrame(tab, text="📊 Histogram Operations", padding="10")
        hist_op_frame.pack(fill="x", pady=5)

        ttk.Button(hist_op_frame, text="Show Histogram", command=self.show_histogram).pack(fill="x", pady=2)
        ttk.Button(hist_op_frame, text="Equalize Histogram",
                   command=lambda: self.apply_operation(self.op_histogram_equalization)).pack(fill="x", pady=2)

        # 2. MORPHOLOGICAL OPERATIONS GRUBU (LabelFrame)
        morph_op_section_frame = ttk.LabelFrame(tab, text="⬜ Morphological Operations", padding="10")
        morph_op_section_frame.pack(fill="x", pady=10)

        morph_frame = ttk.Frame(morph_op_section_frame, padding="5")
        morph_frame.pack(fill="x", pady=5)

        # --- YENİ: ITERATIONS SLIDER ---
        ttk.Label(morph_frame, text="Iterations (Strength):").grid(row=0, column=0, sticky="w", columnspan=2)
        self.iterations_scale = ttk.Scale(morph_frame, from_=1, to=5, orient=tk.HORIZONTAL,
                                          command=self.update_iterations_label)
        self.iterations_scale.set(1)  # Varsayılan 1
        self.iterations_scale.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        self.iterations_label = ttk.Label(morph_frame, text=f"Itr: 1")
        self.iterations_label.grid(row=2, column=0, columnspan=2)
        # --- ITERATIONS SLIDER SONU ---

        ttk.Label(morph_frame, text="Kernel Size (e.g., 3, 5):").grid(row=3, column=0, sticky="w")
        self.morph_ksize_entry = ttk.Entry(morph_frame, width=5)
        self.morph_ksize_entry.insert(0, "3")
        self.morph_ksize_entry.grid(row=3, column=1)

        ttk.Button(morph_frame, text="Global Threshold", command=lambda: self.op_threshold(cv2.THRESH_BINARY)).grid(
            row=4, column=0, pady=2, sticky="ew")
        ttk.Button(morph_frame, text="Otsu Threshold",
                   command=lambda: self.op_threshold(cv2.THRESH_BINARY + cv2.THRESH_OTSU)).grid(row=4, column=1, pady=2,
                                                                                                sticky="ew")

        # Morfolojik Operatörler, artık op_morphology metodu Iterations değerini kullanacak.
        ttk.Button(morph_frame, text="Erode", command=lambda: self.op_morphology(cv2.MORPH_ERODE)).grid(row=5, column=0,
                                                                                                        pady=2,
                                                                                                        sticky="ew")
        ttk.Button(morph_frame, text="Dilate", command=lambda: self.op_morphology(cv2.MORPH_DILATE)).grid(row=5,
                                                                                                          column=1,
                                                                                                          pady=2,
                                                                                                          sticky="ew")

        ttk.Button(morph_frame, text="Open", command=lambda: self.op_morphology(cv2.MORPH_OPEN)).grid(row=6, column=0,
                                                                                                      pady=2,
                                                                                                      sticky="ew")
        ttk.Button(morph_frame, text="Close", command=lambda: self.op_morphology(cv2.MORPH_CLOSE)).grid(row=6, column=1,
                                                                                                        pady=2,
                                                                                                        sticky="ew")

    def update_iterations_label(self, val):
        """Sadece kaydırıcı değeri değiştikçe Iterations etiketini günceller (Tam sayıya yuvarlar)."""
        iterations = int(float(val))
        self.iterations_label.config(text=f"Itr: {iterations}")

    def op_histogram_equalization(self, img):
        if len(img.shape) == 3:
            img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        else:
            return cv2.equalizeHist(img)

    def show_histogram(self):
        global current_image_bgr
        if current_image_bgr is None:
            tk.messagebox.showwarning("Warning", "Please open an image first.")
            return

        img_to_hist = current_image_bgr
        if len(img_to_hist.shape) == 3:
            img_to_hist = cv2.cvtColor(img_to_hist, cv2.COLOR_BGR2GRAY)

        hist = cv2.calcHist([img_to_hist], [0], None, [256], [0, 256])

        # Matplotlib figure'ü Dark tema ile uyumlu hale getir
        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        ax.plot(hist, color='cyan')
        ax.set_title("Histogram of Current Image", color='white')
        ax.set_xlabel("Pixel Value", color='white')
        ax.set_ylabel("Frequency", color='white')
        fig.patch.set_facecolor('#333333')  # Figür arka plan
        ax.set_facecolor('#333333')  # Axes arka plan

        hist_window = tk.Toplevel(self.master)
        hist_window.title("Histogram")

        canvas = FigureCanvasTkAgg(fig, master=hist_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        ttk.Button(hist_window, text="Close", command=hist_window.destroy).pack(pady=5)

    def op_threshold(self, threshold_type):
        def thresh_func(img):
            gray = self.op_grayscale(img)
            thresh_val, dst = cv2.threshold(gray, 127, 255, threshold_type)
            return dst

        self.apply_operation(thresh_func)

    def op_morphology(self, morph_op):
        def morph_func(img):
            try:
                ksize = int(self.morph_ksize_entry.get())
                iterations = int(float(self.iterations_scale.get()))  # Iterations değerini al
            except ValueError:
                self.log_label.config(text="❌ ERROR: Kernel/Iteration must be integers.", foreground="red")
                return img

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))

            if len(img.shape) == 3:
                # Morfolojik işlemlerden önce griye/binary'ye çevir
                _, img = cv2.threshold(self.op_grayscale(img), 127, 255, cv2.THRESH_BINARY)

            # Erode ve Dilate için Iterations kullan
            if morph_op == cv2.MORPH_ERODE:
                return cv2.erode(img, kernel, iterations=iterations)
            elif morph_op == cv2.MORPH_DILATE:
                return cv2.dilate(img, kernel, iterations=iterations)

            # Open ve Close için iterations parametresi yoktur, sadece bir kez uygulanır (iterations=1 varsayılır)
            elif morph_op == cv2.MORPH_OPEN:
                return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
            elif morph_op == cv2.MORPH_CLOSE:
                return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
            return img

        self.apply_operation(morph_func)

if __name__ == "__main__":
    root = ThemedTk()
    app = ImageProcessorApp(root)

    root.mainloop()
