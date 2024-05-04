import customtkinter as ctk
import cv2, os, threading, numpy as np, time
from PIL import Image
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

# Global variables
k1_val,k2_val,process_btn,upload_btn,winSize,imgref,wtf = 0.5,0.5,None,None,None,None,False
upperFr,mapping,fr1,k,r,arrow,app,gray_img,r_imgFr,l_imgFr,tabs,Min,Max = None,None,None,None,None,None,None,None,None,None,None,None,None
image_size = (339, 190)
hov, nor = '#AF4BD6', '#9130BD'
pro_img = None


def select_image(col=0, row=0, imgfr=None):
    global gray_img, fr1, tabs, l_imgFr, imgref
    if imgfr is None:
        imgfr = l_imgFr
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    colored_img = cv2.imread(file_path)
    if col == 1:
        imgref = cv2.cvtColor(colored_img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('ref.png', imgref)
        img1 = ctk.CTkImage(Image.open('ref.png'), size=image_size)
    
    else:
        gray_img = cv2.cvtColor(colored_img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('gray.png', gray_img)
        img1 = ctk.CTkImage(Image.open('gray.png'), size=image_size)

    # remove previous image
    for child in imgfr.winfo_children():
        info = child.grid_info()
        if info['row'] == row:
            child.destroy()

    ctk.CTkLabel(imgfr, image=img1, text='').grid(column=col, row=row, padx=10,pady=10)

    create_graph(tabs.tab('Pseuco Coloring'), 1, 0, img=gray_img)
    create_graph(tabs.tab('Pseuco Coloring'), 3, 0, txt='Denoised Image Histogram')



# ---------------Image Processing functions---------------
def Denose_filter():
    global gray_img, winSize2, variance, pro_img
    try:
        size = int(winSize2.get())
        noise_variance = float(variance.get())
        if size < 1 or noise_variance < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Invalid Input', 'Please enter valid input')
        return

    # padding the image
    padded_img = np.pad(gray_img, ((size//2, size//2), (size//2, size//2)), mode='edge')

    new_img = np.copy(padded_img)

    h, w = gray_img.shape

    for y in range(size, h - size):
        for x in range(size, w - size):
            window = padded_img[y - size:y + size + 1, x - size:x + size + 1]
            mean = np.mean(window.flatten())
            var = np.var(window.flatten())

            print(noise_variance/var)
            new_img[y, x] = (new_img[y, x] - (noise_variance/var)*(new_img[y, x] - mean)).astype('uint8')

    
    new_img = new_img[size//2:-size//2, size//2:-size//2]
    
    # cliping values back in range of 0 to 255
    new_img = np.clip(new_img, 0, 255).astype('uint8')

    cv2.imwrite('denois.png', new_img)

    pro_img = ctk.CTkImage(Image.open('denois.png'), size=image_size)
    for child in r_imgFr.winfo_children():
        info = child.grid_info()
        if info['row'] == 0:
            child.destroy()
    ctk.CTkLabel(r_imgFr, image=pro_img, text='').grid(column=0, row=0, padx=10,pady=10)
    create_graph(tabs.tab('Pseuco Coloring'), 3, 0, img=new_img, txt='Denoised Image Histogram')



def process_image():
    global tabs, gray_img
    if gray_img is None:
        messagebox.showerror('ERROR', 'Please select an image first!')
        return
    
    Denose_filter()



# ---------------graph functions---------------
def create_graph(root, col, row, img=None, canvas=None, txt='Origional Histogram'):
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])

    fig = Figure(figsize=(5.8, 3.8), dpi=78)
    ax = fig.add_subplot(111)
    ax.plot(hist, color=nor)

    if canvas:
        canvas.get_tk_widget().grid_forget()

    ax.set_xlabel('Pixel Value')
    ax.set_ylabel('Frequency')
    ax.set_title(txt)

    for child in root.winfo_children():
        info = child.grid_info()
        if info['row'] == row and info['column'] == col:
            child.destroy()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(column=col, row=row, pady=15, padx=5)

    return canvas

# ---------------Layout functions---------------
def show_val(value, r, txt):
    global k1_val, k2_val

    if r == 1:
        k1_val =  round(float(value), 2)
        txt.configure(text=f'{k1_val:.2f}')
    else:
        k2_val =  round(float(value), 2)
        txt.configure(text=f'{k2_val:.2f}')

def populize_tab(tab, title):
    global gray_img, arrow

    if title == 'Pseuco Coloring':
        global winSize2, variance

        tab.columnconfigure((0,6), weight=1)

        create_graph(tab, col=1, row=0, img=gray_img)
        ctk.CTkLabel(tab, image=arrow, text='').grid(column=2, row=0, padx=25, pady=10)
        create_graph(tab, col=3, row=0, txt='Denoised Image Histogram')

        fr = ctk.CTkFrame(tab)
        fr.grid(column=1, row=1, pady=5, padx=5, sticky='news', columnspan=3)
        fr.columnconfigure((0,3), weight=1)

        winSize2 = ctk.CTkEntry(fr, width=105, placeholder_text='Window Size')
        winSize2.grid(column=1, row=1, pady=10, padx=5)

        variance = ctk.CTkEntry(fr, width=105, placeholder_text='Noise Variance')
        variance.grid(column=2, row=1, pady=10, padx=5)


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

        MMSE       = tabs.add('Pseuco Coloring')

        # MMSE Filter tab content
        populize_tab(MMSE, 'Pseuco Coloring')


if __name__ == '__main__':
    app = ctk.CTk()
    basicLayout()
    app.mainloop()