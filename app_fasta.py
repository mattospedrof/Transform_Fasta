import customtkinter as ctk
import os
import re
import tkinter as tk
import webbrowser
from openpyxl import Workbook
from PIL import Image
from tkinter import messagebox


class File():
    def __init__(self):
        self.selected_file = None
    
    
    def select_file(self):
        try:
            file = ctk.filedialog.askopenfilename(
                title="FASTA Files",
                filetypes=[("Text files", "*.txt;*.FASTA")],
                initialdir="C:\\",
                )
            if file:
                self.selected_file = file
                return os.path.basename(file)
            else:
                messagebox.showwarning("No files were selected", "Select a file")
                return os.path.basename(file)
        except Exception as e:
            messagebox.showerror("Error", f"Open file error '{file}': {e}")
            
        return self.selected_file


    def transform_file(self):
        if not self.selected_file:
            messagebox.showwarning("No files were selected", "Select a file")
            return None
        
        try:
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(['Name', 'Sequence', 'Length'])

            with open(self.selected_file, 'r') as archive:
                sequences = archive.read()

            pattern_completed = r'>([^\n]+)\n([A-Z]+)'
            results_completed = re.findall(pattern_completed, sequences)

            for result in results_completed:
                name = result[0]
                sequence = result[1]
                length = len(sequence)
                
                sheet.append([name, sequence, length])

            file_excel = os.path.splitext(self.selected_file)[0] + '_table.xlsx'
            workbook.save(file_excel)
            
            if os.path.exists(file_excel): 
                messagebox.showinfo("Success", f"{file_excel} was created succesfully")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error converting the file {self.selected_file}: {e}")


class APPView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller
        self.conf_main()
        self.create_widgets()
        
        
    def conf_main(self):
        window_ico = "media/teste.ico"
        
        if hasattr(self, 'set_appearance_mode'):
            self.set_appearance_mode("dark")
        
        if hasattr(self, 'set_default_color_theme'):
            self.set_default_color_theme("dark-blue")

        self.geometry("400x400")
        self.title("Solutions in Bioinformatics")
        self.iconbitmap(default=window_ico)
        self.resizable(width=False, height=False)

    
    def create_widgets(self):
        self.create_image_frame()
        self.create_controls_frame()
        self.update_file_name("No file selected")
        self.remove_file_name()
        
        
    def create_image_frame(self):
        image = Image.open("media/lateral_image.png")
        image_ctk = ctk.CTkImage(light_image=image, dark_image=image, size=(100,400))

        self.frame_image = ctk.CTkFrame(master=self, width=100, height=self.winfo_height())
        self.frame_image.grid(row=0, column=0, sticky="nsw")

        self.label_imagem = ctk.CTkLabel(master=self.frame_image, image=image_ctk, text="")
        self.label_imagem.pack()
        
        
    def create_controls_frame(self):
        self.frame_controls = ctk.CTkFrame(
            master=self, fg_color="black", width=300, height=400,
            corner_radius=0,
        )
        self.frame_controls.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.frame_controls.grid_propagate(False)
        
        
        self.font_title = ctk.CTkFont(family="Georgia", size=20, weight="bold")
        self.font_btn = ctk.CTkFont(family="Georgia", size=14, weight="bold")
        self.font_file_selected = ctk.CTkFont(family="Georgia", size=12, weight="bold")
        self.font_faq = ctk.CTkFont(family="times", size=12, weight="bold", underline=True)
        
        
        self.title_text = ctk.CTkLabel(
            master=self.frame_controls, width=180, height=20,
            text_color="white", font=self.font_title, fg_color="transparent",
            anchor="center",
            text="Converting Fasta to Table",
        )
        self.title_text.grid(row=1, column=1, padx=(20, 10), pady=(20, 0))
        
        
        self.btn_select_file = ctk.CTkButton(
            master=self.frame_controls, text="Select file", font=self.font_btn, anchor="center",
            fg_color="darkblue",
            command=self.controller.select_file,
        )
        self.btn_select_file.grid(row=2, column=1, pady=(100, 5),)
        
        
        self.label_file_name = ctk.CTkLabel(
            master=self.frame_controls, width=100,
            text_color="white", font=self.font_file_selected, fg_color="transparent",
            anchor="center",
            text="",
        )
        self.label_file_name.grid(row=3, column=1, pady=(0, 5),)
        

        self.btn_transform_file = ctk.CTkButton(
            master=self.frame_controls, text="Convert file for table", font=self.font_btn, anchor="center",
            fg_color="darkblue",
            command=self.controller.transform_file,
        )
        self.btn_transform_file.grid(row=4, column=1, pady=0,)
        
        
        self.btn_redirect_faq = ctk.CTkButton(
            master=self.frame_controls, text="FAQ", width=20, height=20,
            text_color="red", fg_color="transparent", border_color="darkblue", border_width=1, anchor="center",
            command=self.controller.redirect_to_faq,
        )
        self.btn_redirect_faq.grid(row=5, column=1, padx=(250, 0), pady= (135, 5), sticky="s")
        
    
    def update_file_name(self, file_name):
        self.label_file_name.configure(text=f"Selected: {file_name}")
        
    
    def remove_file_name(self):
        self.label_file_name.configure(text='')
        
    
class Controller():
    def __init__(self):
        self.file_model = File()
        self.view = APPView(self)
        
        
    def select_file(self):
        selected_file = self.file_model.select_file()
        if selected_file:
            self.view.update_file_name(selected_file)
        
        
    def transform_file(self):
        self.file_model.transform_file()
        self.view.remove_file_name()
        
    
    def redirect_to_faq(self):
        link = "https://github.com/mattospedrof"
        webbrowser.open_new_tab(link)
        messagebox.showinfo("Check your browser", "A new tab opened with the FAQ link")
        
        
    def run(self):
        self.view.mainloop()


if __name__ == "__main__":
    controller = Controller()
    controller.run()
