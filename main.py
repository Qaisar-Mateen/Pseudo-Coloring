import customtkinter as ctk
import cv2, os, numpy as np
from PIL import Image
from tkinter import filedialog, messagebox

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

# Global variables
process_btn,upload_btn,imgref = None,None,None
upperFr,fr1,arrow,app,gray_img,r_imgFr,l_imgFr,tabs = None,None,None,None,None,None,None,None
image_size = (339, 190)
hov, nor = '#AF4BD6', '#9130BD'
pro_img = None


def select_image(col=0, row=0, imgfr=None, colored=False):
    global gray_img, fr1, tabs, l_imgFr, imgref
    if imgfr is None:
        imgfr = l_imgFr
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    colored_img = cv2.imread(file_path)
    if col == 1:
        imgref = colored_img
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

    if tabs.get() == 'Pseudo Coloring':
        for frm in tabs.tab('Pseudo Coloring').winfo_children():
            if frm.grid_info()['row'] == 1:
                fr = frm
        # if col==0:
        #     create_graph(fr, 1, 0, img=gray_img, txt='Target Image Histogram')
        # elif col==1:
        #     create_graph(fr, 3, 0, img=imgref, txt='Reference Image Histogram')  

def pseudo_color():
    pass

def process_image():
    global tabs, gray_img
    if gray_img is None:
        messagebox.showerror('ERROR', 'Please select an image first!')
        return
     
    pseudo_color()



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


def populize_tab(tab, title):
    global gray_img, arrow

    if 1 == 1:
        tab.columnconfigure((0,6), weight=1)

        plus = ctk.CTkImage(Image.open('../plus.png'), size=(70, 60))
        noImg = ctk.CTkImage(Image.open('../no image.png'), size=image_size)

        f = ctk.CTkFrame(tab)
        f.grid(column=1, row=0, pady=5, padx=5, sticky='news', columnspan=5)
        f.columnconfigure((0,6), weight=1)
        imgFr1 = ctk.CTkFrame(f, corner_radius=20, fg_color="#2B2B2B")
        imgFr1.grid(row=0, column=1, padx=15, pady=15, sticky='snew')
        ctk.CTkLabel(imgFr1, image=noImg, text='').grid(column=0, row=0, padx=10, pady=10)
        ctk.CTkLabel(imgFr1, text='Target Image').grid(column=0, row=1, padx=10, pady=(0,10))

        img1_btn = ctk.CTkButton(f, text='Upload Target Image', command=lambda: select_image(0, 0, imgFr1), fg_color=nor, hover_color=hov)
        img1_btn.grid(column=1, row=2, padx=10, pady=10)

        ctk.CTkLabel(f, image=plus, text='').grid(column=2, row=0, padx=10, pady=10)

        imgFr2 = ctk.CTkFrame(f, corner_radius=20, fg_color="#2B2B2B")
        imgFr2.grid(row=0, column=3, padx=15, pady=15, sticky='snew')
        ctk.CTkLabel(imgFr2, image=noImg, text='').grid(column=1, row=0, padx=10, pady=10)
        ctk.CTkLabel(imgFr2, text='Reference Image').grid(column=1, row=1, padx=10, pady=(0,10))

        img2_btn = ctk.CTkButton(f, text='Upload Reference Image', command=lambda: select_image(1, 0, imgFr2), fg_color=nor, hover_color=hov)
        img2_btn.grid(column=3, row=2, padx=10, pady=10)

        # fr = ctk.CTkFrame(tab)
        # fr.grid(column=1, row=1, pady=5, padx=5, sticky='news', columnspan=5)
        # fr.columnconfigure((0,6), weight=1)
        # create_graph(fr, 1, 0, txt='Target Image Histogram')
        # ctk.CTkLabel(fr, image=plus, text='').grid(column=2, row=0, padx=20, pady=10)
        # create_graph(fr, 3, 0, txt='Reference Image Histogram')
        # ctk.CTkLabel(fr, image=arrow, text='').grid(column=4, row=0, pady=25, padx=10)
        # create_graph(fr, 5, 0, txt='Processed Histogram')


def upper_frame(img=False):
    global app, r_imgFr, l_imgFr, image_size, arrow, upperFr, upload_btn, process_btn

    if app:
        r_imgFr = ctk.CTkFrame(upperFr, corner_radius=20, fg_color="#2B2B2B")
        r_imgFr.grid(row=0, column=5, padx=15, pady=15, sticky='snew')
    
        img1 = ctk.CTkImage(Image.open('../no image.png'), size=image_size)

        if pro_img is not None:
            ctk.CTkLabel(r_imgFr, image=pro_img, text='').grid(column=0, row=0, padx=10,pady=10)
        else:
            ctk.CTkLabel(r_imgFr, image=img1, text='').grid(column=0, row=0, padx=10,pady=10)
            
        process_btn = ctk.CTkButton(upperFr, text='Process Image', command=process_image, fg_color=nor, hover_color=hov)
        process_btn.grid(column=5, row=1, padx=10, pady=10)

        ctk.CTkLabel(r_imgFr, text='Colored Image').grid(column=0, row=1, padx=10, pady=(0,10))

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

        equalize   = tabs.add('Pseudo Coloring')
     
        # specified Histogram equalization tab content
        populize_tab(equalize, 'Pseudo Coloring')

if __name__ == '__main__':
    app = ctk.CTk()
    basicLayout()
    app.mainloop()
    app = None

    if os.path.exists('gray.png'):
        os.remove('gray.png')

    if os.path.exists('ref.png'):
        os.remove('ref.png')

    if os.path.exists('equalized.png'):
        if os.path.exists('specified.png'):
            os.remove('specified.png')
        os.rename('equalized.png','specified.png')
