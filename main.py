import customtkinter as ctk
import cv2, numpy as np, colorsys
from PIL import Image
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

# Global variables
k1_val, process_btn,upload_btn = 5, None, None
upperFr,arrow,app,gray_img,r_imgFr,l_imgFr,tabs= None,None,None,None,None,None,None
image_size = (339, 190)
hov, nor = '#AF4BD6', '#9130BD'
pro_img = None

def select_image(col=0, row=0, imgfr=None):
    global gray_img, fr1, tabs, l_imgFr, imgref
    if imgfr is None:
        imgfr = l_imgFr
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    colored_img = cv2.imread(file_path)
    
    gray_img = cv2.cvtColor(colored_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.png', gray_img)
    img1 = ctk.CTkImage(Image.open('gray.png'), size=image_size)

    # remove previous image
    for child in imgfr.winfo_children():
        info = child.grid_info()
        if info['row'] == row:
            child.destroy()

    ctk.CTkLabel(imgfr, image=img1, text='').grid(column=col, row=row, padx=10,pady=10)

# ---------------Image Processing functions---------------
def PseudoColor():
    global gray_img, k1_val, pro_img, check_var
    
    new_img = np.zeros((gray_img.shape[0], gray_img.shape[1], 3), dtype=np.uint8)

    colors = []
    for i in range(k1_val):
        weights = np.random.rand(3)

        if check_var.get():
            weights /= weights.sum() # Normalize the weights to get smoothed trasitions in colors

        colors.append(weights)

    for i in range(k1_val):
        for j in range(3):
            weighted_pixels = (gray_img * colors[i][j]).astype('uint8')
            new_img[:, :, j] += weighted_pixels
    
    # cliping values back in range of 0 to 255
    new_img = np.clip(new_img, 0, 255).astype('uint8')


    cv2.imwrite('Colored.png', new_img)

    pro_img = ctk.CTkImage(Image.open('Colored.png'), size=image_size)
    for child in r_imgFr.winfo_children():
        info = child.grid_info()
        if info['row'] == 0:
            child.destroy()
    ctk.CTkLabel(r_imgFr, image=pro_img, text='').grid(column=0, row=0, padx=10,pady=10)


def process_image():
    global tabs, gray_img
    if gray_img is None:
        messagebox.showerror('ERROR', 'Please select an image first!')
        return
    
    PseudoColor()

# ---------------Layout functions---------------
def show_val(value, r, txt):
    global k1_val

    if r == 1:
        k1_val =  int(value)
        txt.configure(text=f'{k1_val}')

    

def populize_tab(tab, title):
    global gray_img, arrow

    if title == 'Pseuco Coloring':
        global check_var
        check_var = ctk.BooleanVar(value=False)
        tab.columnconfigure((0,6), weight=1)

        fr = ctk.CTkFrame(tab)
        fr.grid(column=1, row=1, pady=5, padx=5, sticky='news', columnspan=3)
        fr.columnconfigure((0,7), weight=1)

        txt1= ctk.CTkLabel(fr, text='5')
        txt1.grid(column=3, row=1, pady=10, padx=5)
        ctk.CTkLabel(fr, text='Sensitivity: ').grid(column=1, row=1, pady=10, padx=5, sticky='e')
        k1 = ctk.CTkSlider(fr, width=300, from_=1, to=10, number_of_steps=10, button_color=nor, progress_color=hov, button_hover_color=hov, command=lambda e: show_val(e,1,txt1))
        k1.grid(column=2, row=1, padx=5, pady=10)

        fr2 = ctk.CTkFrame(tab)
        fr2.grid(column=1, row=2, pady=5, padx=5, sticky='news', columnspan=3)
        fr2.columnconfigure((0,7), weight=1)

        
        checkbox = ctk.CTkCheckBox(fr2, text="Normalize", command=None, fg_color=nor, hover_color=hov,
                                variable=check_var, onvalue=True, offvalue=False)
        checkbox.grid(column=1, row=1, padx=5, pady=5)
        


def upper_frame(img=False):
    global app, r_imgFr, l_imgFr, image_size, arrow, upperFr, upload_btn, process_btn

    if app:
        l_imgFr = ctk.CTkFrame(upperFr, corner_radius=20, fg_color="#2B2B2B")
        l_imgFr.grid(row=0, column=1, padx=15, pady=15, sticky='snew')
        
        arrow = ctk.CTkImage(Image.open('../right arrow.png'), size=(60, 60))
        ctk.CTkLabel(upperFr, image = arrow, text='').grid(column=3, row=0, padx=10, pady=10)
        r_imgFr = ctk.CTkFrame(upperFr, corner_radius=20, fg_color="#2B2B2B")
        r_imgFr.grid(row=0, column=5, padx=15, pady=15, sticky='snew')
    
        img1 = ctk.CTkImage(Image.open('../no image.png'), size=image_size)

        if not img:
            ctk.CTkLabel(l_imgFr, image=img1, text='').grid(column=0, row=0, padx=10,pady=10)
        
        if pro_img is not None:
            ctk.CTkLabel(r_imgFr, image=pro_img, text='').grid(column=0, row=0, padx=10,pady=10)
        else:
            ctk.CTkLabel(r_imgFr, image=img1, text='').grid(column=0, row=0, padx=10,pady=10)
            
        upload_btn = ctk.CTkButton(upperFr, text='Upload Image', command=select_image, fg_color=nor, hover_color=hov)
        upload_btn.grid(column=1, row=1, padx=10, pady=10)

        process_btn = ctk.CTkButton(upperFr, text='Process Image', command=process_image, fg_color=nor, hover_color=hov)
        process_btn.grid(column=5, row=1, padx=10, pady=10)

        ctk.CTkLabel(l_imgFr, text='Original (Gray Scale) Image').grid(column=0, row=1, padx=10, pady=(0,10))
        ctk.CTkLabel(r_imgFr, text='Processed Image').grid(column=0, row=1, padx=10, pady=(0,10))

def basicLayout():
    global app, r_imgFr, l_imgFr, image_size, arrow, tabs, upperFr
    if app:
        app.title('Pseudo Coloring')
        width= app.winfo_screenwidth()               
        height= app.winfo_screenheight()
        app.geometry('%dx%d'% (width//1.3, (height//1.3)+40))
        app.columnconfigure(0, weight=1)
        app.rowconfigure(1, weight=1)

        # upper frame for images
        upperFr = ctk.CTkFrame(app, corner_radius=20)
        upperFr.grid(pady=(20, 15), padx=30, row=0, column=0, sticky='new',)
        upperFr.columnconfigure((0,8), weight=1)

        upper_frame()

        # lower frame for controls
        lowerFr = ctk.CTkScrollableFrame(app, corner_radius=20)
        lowerFr.grid(pady=(0, 20), padx=30, row=1, column=0, sticky='snew')
        lowerFr.rowconfigure(0, weight=1)
        lowerFr.columnconfigure(0, weight=1)
        tabs = ctk.CTkTabview(lowerFr, segmented_button_selected_color=nor, segmented_button_unselected_hover_color=hov, segmented_button_selected_hover_color=hov)
        tabs.grid(sticky='news')

        MMSE = tabs.add('Pseuco Coloring')

        # MMSE Filter tab content
        populize_tab(MMSE, 'Pseuco Coloring')


if __name__ == '__main__':
    app = ctk.CTk()
    basicLayout()
    app.mainloop()