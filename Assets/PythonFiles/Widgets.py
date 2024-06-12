import re

import customtkinter as ctk
import tkinter.font as ft
import tkinter.messagebox as msg
import tkinter.filedialog as fd
from PIL import Image, ImageTk
import Assets.PythonFiles.Variable as vary
import main as mn


class MainWindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(f'{vary.width}x{vary.height}')
        self.title('Text Editor')
        self.minsize(765, 340)
        self.iconbitmap('Assets/Images/icon.ico')
        self.configure(fg_color=vary.bg_clr)

        self.protocol('WM_DELETE_WINDOW', self.close_event_handler)
        self.bind('<Configure>', self.resize_event_handler)

        self.arranging_home_widgets()

    def arranging_home_widgets(self):
        # Defining frames
        self.home_widget = ctk.CTkFrame(self, fg_color=vary.bg_clr)
        self.settings_widget = ctk.CTkScrollableFrame(self, fg_color=vary.bg_clr, width=vary.width, height=vary.height)

        self.tool_panel = ctk.CTkFrame(self.home_widget, fg_color=vary.bg_clr)
        self.status_bar = ctk.CTkFrame(self.home_widget, fg_color=vary.bg_clr)

        self.option_menu_panel = ctk.CTkFrame(self.tool_panel, fg_color=vary.bg_clr)
        self.undo_redo_panel = ctk.CTkFrame(self.tool_panel, fg_color=vary.bg_clr)
        self.file_btn_panel = ctk.CTkFrame(self.tool_panel, fg_color=vary.bg_clr)

        # Defining label
        self.status = ctk.CTkLabel(self.status_bar, text=vary.status, text_color=vary.txt_clr)

        # Defining text filed
        self.text_field = ctk.CTkTextbox(
            self.home_widget, width=vary.width, font=(vary.font, vary.font_size), undo=True,
            fg_color=vary.txt_panel_clr, text_color=vary.font_clr
        )
        self.text_field.insert('1.0', vary.text)

        # Defining button icons
        self.img_1 = Image.open(f'Assets/Images/open-{vary.themes}.png')
        self.res_img_1 = self.img_1.resize((35, 35))
        self.open = ImageTk.PhotoImage(self.res_img_1)

        self.img_2 = Image.open(f'Assets/Images/new-{vary.themes}.png')
        self.res_img_2 = self.img_2.resize((35, 35))
        self.new = ImageTk.PhotoImage(self.res_img_2)

        self.img_3 = Image.open(f'Assets/Images/save-{vary.themes}.png')
        self.res_img_3 = self.img_3.resize((35, 35))
        self.save = ImageTk.PhotoImage(self.res_img_3)

        self.img_4 = Image.open(f'Assets/Images/clear-{vary.themes}.png')
        self.res_img_4 = self.img_4.resize((35, 35))
        self.clear = ImageTk.PhotoImage(self.res_img_4)

        self.img_5 = Image.open(f'Assets/Images/settings-{vary.themes}.png')
        self.res_img_5 = self.img_5.resize((35, 35))
        self.settings = ImageTk.PhotoImage(self.res_img_5)

        self.img_6 = Image.open(f'Assets/Images/undo-{vary.themes}.png')
        self.res_img_6 = self.img_6.resize((35, 35))
        self.undo = ImageTk.PhotoImage(self.res_img_6)

        self.img_7 = Image.open(f'Assets/Images/redo-{vary.themes}.png')
        self.res_img_7 = self.img_7.resize((35, 35))
        self.redo = ImageTk.PhotoImage(self.res_img_7)

        # Defining top panel widgets
        self.new_btn = ctk.CTkButton(
            self.file_btn_panel, text='', width=40, height=40, fg_color=vary.bg_clr, image=self.new,
            hover_color=vary.widget_clr, text_color=vary.txt_clr
        )
        self.open_btn = ctk.CTkButton(
            self.file_btn_panel, text='', width=40, height=40, fg_color=vary.bg_clr, image=self.open,
            hover_color=vary.widget_clr, text_color=vary.txt_clr
        )
        self.save_btn = ctk.CTkButton(
            self.file_btn_panel, text='', width=40, height=40, fg_color=vary.bg_clr, image=self.save,
            hover_color=vary.widget_clr, text_color=vary.txt_clr
        )
        self.delete_btn = ctk.CTkButton(
            self.file_btn_panel, text='', width=40, height=40, fg_color=vary.bg_clr, image=self.clear,
            hover_color=vary.widget_clr, text_color=vary.txt_clr
        )
        self.settings_btn = ctk.CTkButton(
            self.tool_panel, text='', width=40, height=40, fg_color=vary.bg_clr, image=self.settings,
            hover_color=vary.widget_clr, text_color=vary.txt_clr
        )
        self.undo_btn = ctk.CTkButton(
            self.undo_redo_panel, text='', width=40, height=40, fg_color=vary.bg_clr, image=self.undo,
            hover_color=vary.widget_clr, text_color=vary.txt_clr
        )
        self.redo_btn = ctk.CTkButton(
            self.undo_redo_panel, text='', width=40, height=40, fg_color=vary.bg_clr, image=self.redo,
            hover_color=vary.widget_clr, text_color=vary.txt_clr
        )
        self.theme_btn = ctk.CTkButton(
            self.settings_widget, text='        App Theme', text_color=vary.txt_clr, width=vary.width - 10, height=50,
            font=('Arial', 14), fg_color=vary.widget_clr, anchor='w', hover_color=vary.widget_hover_clr
        )

        self.font_btn = ctk.CTkButton(
            self.settings_widget, text='        Font properties', text_color=vary.txt_clr, width=vary.width - 10,
            height=50, font=('Arial', 14), fg_color=vary.widget_clr, anchor='w', hover_color=vary.widget_hover_clr
        )

        # Binding buttons to functions
        self.new_btn.bind('<Button-1>', lambda x: mn.RunApp())
        self.save_btn.bind('<Button-1>', self.save_btn_action)
        self.open_btn.bind('<Button-1>', self.open_btn_action)
        self.delete_btn.bind('<Button-1>', self.delete_btn_action)

        self.undo_btn.bind('<Button-1>', lambda x: self.text_field.edit_undo())
        self.redo_btn.bind('<Button-1>', lambda x: self.text_field.edit_redo())

        self.settings_btn.bind('<Button-1>', self.settings_btn_action)

        # Binding text filed to function
        self.text_field.bind('<KeyRelease>', self.word_count_action)

        # Defining option menus
        self.font_family = ctk.CTkOptionMenu(
            self.option_menu_panel, values=ft.families(), command=lambda x:self.font_chooser_action(0), width=200, height=40,
            fg_color=vary.widget_clr, button_color=vary.widget_clr, button_hover_color=vary.widget_hover_clr,
            text_color=vary.txt_clr, dropdown_fg_color=vary.widget_clr, dropdown_hover_color=vary.widget_hover_clr,
            dropdown_text_color=vary.txt_clr
        )
        self.font_size = ctk.CTkOptionMenu(
            self.option_menu_panel, values=vary.sizes, command=lambda x:self.font_chooser_action(0), width=60, height=40,
            fg_color=vary.widget_clr, button_color=vary.widget_clr, button_hover_color=vary.widget_hover_clr,
            text_color=vary.txt_clr, dropdown_fg_color=vary.widget_clr, dropdown_hover_color=vary.widget_hover_clr,
            dropdown_text_color=vary.txt_clr
        )
        self.font_family.set(vary.font)
        self.font_size.set(vary.font_size)

        # Placing labels
        self.status.grid(row=0, column=0, padx=10, pady=0, sticky='w')

        # Placing frames
        self.home_widget.pack()
        self.tool_panel.grid(row=0, column=0)
        self.status_bar.grid(row=2, column=0, sticky='w', pady=0)
        self.option_menu_panel.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.undo_redo_panel.grid(row=0, column=1, padx=10, pady=10)
        self.file_btn_panel.grid(row=0, column=2, padx=10, pady=10)

        # PLacing text filed
        self.text_field.grid(row=1, column=0)

        # Placing buttons
        self.undo_btn.grid(row=0, column=0)
        self.redo_btn.grid(row=0, column=1)
        self.open_btn.grid(row=0, column=1)
        self.new_btn.grid(row=0, column=0)
        self.save_btn.grid(row=0, column=2)
        self.delete_btn.grid(row=0, column=3)
        self.settings_btn.grid(row=0, column=3, padx=10, pady=10, sticky='e')

        # Placing option menus
        self.font_family.grid(row=0, column=0, padx=5, pady=5)
        self.font_size.grid(row=0, column=1, padx=5, pady=5)

    def word_count_action(self, args):
        words = self.text_field.get('1.0', 'end-1c')
        vary.word_count = len(re.findall('\w', words))

        vary.line_count = int(self.text_field.index('end-1c').split('.')[0])

        vary.status = f'Words: {vary.word_count}      Lines: {vary.line_count}      Font family: {vary.font}      Font size: {vary.font_size}'
        self.status.configure(text=vary.status)

    def settings_btn_action(self, args):
        if not vary.settings:
            self.home_widget.pack_forget()
            vary.settings = True
        else:
            self.home_widget.pack()
            vary.settings = False
        vary.text = self.text_field.get('1.0', 'end')
        self.arranging_settings_widgets()

    def back_btn_action(self, args):
        if vary.settings:
            self.settings_widget.pack_forget()
            vary.settings = False
        else:
            self.settings_widget.pack()
            vary.settings = True

        self.arranging_home_widgets()

    def arranging_settings_widgets(self):
        # Defining frames
        self.top_panel = ctk.CTkFrame(self.settings_widget, fg_color=vary.bg_clr)
        self.theme_panel = ctk.CTkFrame(self.settings_widget, fg_color=vary.bg_clr)
        self.font_panel = ctk.CTkFrame(self.settings_widget, fg_color=vary.bg_clr)

        # Defining button icons
        self.img_8 = Image.open(f'Assets/Images/back-{vary.themes}.png')
        self.res_img_8 = self.img_8.resize((35, 35))
        self.back = ImageTk.PhotoImage(self.res_img_8)

        # Defining labels
        self.lbl = ctk.CTkLabel(self.top_panel, text='Settings', text_color=vary.txt_clr, font=('Arial', 35))
        self.lbl_1 = ctk.CTkLabel(self.font_panel, text='Font name: ', text_color=vary.txt_clr)
        self.lbl_2 = ctk.CTkLabel(self.font_panel, text='Font size: ', text_color=vary.txt_clr)
        self.lbl_3 = ctk.CTkLabel(self.font_panel, text='Font color: ', text_color=vary.txt_clr)
        self.ex_lbl = ctk.CTkLabel(
            self.font_panel, text='This is how your text look like', text_color=vary.font_clr,
            font=(vary.font, vary.font_size)
        )

        # Defining option menus
        self.font_family_1 = ctk.CTkOptionMenu(
            self.font_panel, values=ft.families(), command=lambda x:self.font_chooser_action(1), width=200, height=40,
            fg_color=vary.widget_clr, button_color=vary.widget_clr, button_hover_color=vary.widget_hover_clr,
            text_color=vary.txt_clr, dropdown_fg_color=vary.widget_clr, dropdown_hover_color=vary.widget_hover_clr,
            dropdown_text_color=vary.txt_clr
        )
        self.font_size_1 = ctk.CTkOptionMenu(
            self.font_panel, values=vary.sizes, command=lambda x:self.font_chooser_action(1), width=200, height=40,
            fg_color=vary.widget_clr, button_color=vary.widget_clr, button_hover_color=vary.widget_hover_clr,
            text_color=vary.txt_clr, dropdown_fg_color=vary.widget_clr, dropdown_hover_color=vary.widget_hover_clr,
            dropdown_text_color=vary.txt_clr
        )

        self.font_color = ctk.CTkOptionMenu(
            self.font_panel, values=vary.font_clrs, command=self.change_font_color, width=200, height=40,
            fg_color=vary.widget_clr, button_color=vary.widget_clr, button_hover_color=vary.widget_hover_clr,
            text_color=vary.txt_clr, dropdown_fg_color=vary.widget_clr, dropdown_hover_color=vary.widget_hover_clr,
            dropdown_text_color=vary.txt_clr
        )

        self.font_family_1.set(vary.font)
        self.font_size_1.set(vary.font_size)
        self.font_color.set(vary.font_clr)

        # Defining Buttons
        self.back_btn = ctk.CTkButton(
            self.top_panel, text='', width=40, height=40, fg_color=vary.bg_clr, image=self.back,
            hover_color=vary.widget_clr, text_color=vary.txt_clr
        )

        # Defining radio buttons
        self.dark = ctk.CTkRadioButton(
            self.theme_panel, text='Dark theme', command=lambda: self.radio_btn_action(None, 0),
            text_color=vary.txt_clr)
        self.light = ctk.CTkRadioButton(
            self.theme_panel, text='Light theme', command=lambda: self.radio_btn_action(None, 1),
            text_color=vary.txt_clr)

        if vary.themes == 'dark':
            self.dark.select(True)
        elif vary.themes == 'light':
            self.light.select(True)

        # Binding buttons to functions
        self.back_btn.bind('<Button-1>', self.back_btn_action)

        # Placing frames
        self.settings_widget.pack()
        self.top_panel.grid(row=0, column=0, padx=5, pady=5)

        # Placing labels
        self.lbl.grid(row=0, column=1, padx=5, pady=5)
        self.lbl_1.grid(row=0, column=0, padx=25, pady=5)
        self.lbl_2.grid(row=1, column=0, padx=25, pady=5)
        self.lbl_3.grid(row=2, column=0, padx=25, pady=5)
        self.ex_lbl.grid(row=3, column=0, columnspan=2, padx=25, pady=5)

        # Placing option menus
        self.font_family_1.grid(row=0, column=1, padx=25, pady=5)
        self.font_size_1.grid(row=1, column=1, padx=25, pady=5)
        self.font_color.grid(row=2, column=1, padx=25, pady=5)

        # Placing buttons
        self.back_btn.grid(row=0, column=0, padx=5, pady=5)
        self.theme_btn.grid(row=1, column=0, padx=5, pady=5)
        self.font_btn.grid(row=3, column=0, padx=5, pady=5)

        # Placing radio buttons
        self.dark.grid(row=0, column=0, padx=25, pady=5)
        self.light.grid(row=1, column=0, padx=25, pady=5)

        self.theme_panel.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.font_panel.grid(row=4, column=0, padx=5, pady=5, sticky='w')

    def change_font_color(self, args):
        vary.font_clr = self.font_color.get()
        self.change_fonts()

    def radio_btn_action(self, args, what):
        if what == 0:
            self.light.deselect(False)
            self.dark.select(True)
            vary.themes = 'dark'

            vary.widget_clr = '#303030'
            vary.widget_hover_clr = '#292929'
            vary.txt_panel_clr = '#1D1E1E'
            vary.txt_clr = '#F8F8F8'
            vary.bg_clr = '#242424'

        else:
            self.dark.deselect(False)
            self.light.select(True)
            vary.themes = 'light'

            vary.widget_clr = '#D0D0D0'
            vary.widget_hover_clr = '#B0B0B0'
            vary.txt_panel_clr = '#C0C0C0'
            vary.txt_clr = '#000000'
            vary.bg_clr = '#FFFFFF'

        self.change_widgets_theme()

    def change_widgets_theme(self):
        frame_array = [
            self.settings_widget, self.top_panel, self.theme_panel, self.home_widget, self.tool_panel, self.status_bar,
            self.option_menu_panel, self.file_btn_panel, self.undo_redo_panel, self.font_panel
        ]
        lbl_array = [self.lbl, self.lbl_1, self.lbl_2, self.lbl_3, self.status]
        btn_array = [self.theme_btn, self.font_btn]
        img_btn_array = [
            self.back_btn, self.open_btn, self.save_btn, self.delete_btn, self.undo_btn,
            self.redo_btn, self.settings_btn, self.new_btn
        ]
        text_panel_array = [self.text_field]
        option_menu_array = [self.font_size, self.font_family, self.font_family_1, self.font_size_1, self.font_color]
        radio_array = [self.dark, self.light]

        for i in frame_array:
            i.configure(fg_color=vary.bg_clr)

        for i in text_panel_array:
            i.configure(text_color=vary.font_clr)
            i.configure(fg_color=vary.txt_panel_clr)
            i.configure(font=(vary.font, vary.font_size))

        for i in lbl_array:
            i.configure(text_color=vary.txt_clr)

        for i in radio_array:
            i.configure(text_color=vary.txt_clr)

        for i in btn_array:
            i.configure(text_color=vary.txt_clr)
            i.configure(fg_color=vary.widget_clr)
            i.configure(hover_color=vary.widget_hover_clr)

        for i in img_btn_array:
            i.configure(fg_color=vary.bg_clr)
            i.configure(hover_color=vary.widget_clr)

        for i in option_menu_array:
            i.configure(text_color=vary.txt_clr)
            i.configure(fg_color=vary.widget_clr)
            i.configure(button_hover_color=vary.widget_hover_clr)
            i.configure(button_color=vary.widget_clr)
            i.configure(dropdown_fg_color=vary.widget_clr)
            i.configure(dropdown_hover_color=vary.widget_hover_clr)
            i.configure(dropdown_text_color=vary.txt_clr)

    def change_fonts(self):
        vary.status = f'Words: {vary.word_count}      Lines: {vary.line_count}      Font family: {vary.font}      Font size: {vary.font_size}'
        self.status.configure(text=vary.status)
        text_panel_array = [self.text_field]

        for i in text_panel_array:
            i.configure(text_color=vary.font_clr)
            i.configure(fg_color=vary.txt_panel_clr)
            i.configure(font=(vary.font, vary.font_size))

        try:
            self.ex_lbl.configure(text_color=vary.font_clr)
            self.ex_lbl.configure(font=(vary.font, vary.font_size))
        except:
            pass

    def delete_btn_action(self, args):
        if msg.askyesno('Clear', 'Are you sure you want to\nclear everything?'):
            self.text_field.delete('1.0', 'end')
        self.word_count_action(None)

    def open_btn_action(self, args):
        try:
            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            )

            f = fd.askopenfile(filetypes=filetypes)
            txt = f.read()
            self.text_field.delete('1.0', 'end')
            self.text_field.insert('1.0', txt)
            self.word_count_action(None)

        except Exception as e:
            print(e)

    def save_btn_action(self, args):
        try:
            f = fd.asksaveasfile(initialfile='Untitled.txt',
                                 defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])

            f.write(self.text_field.get('1.0', 'end'))

        except Exception as e:
            print(e)

    def font_chooser_action(self, args):
        if args == 0:
            vary.font = self.font_family.get()
            vary.font_size = int(self.font_size.get())
        elif args == 1:
            vary.font = self.font_family_1.get()
            vary.font_size = int(self.font_size_1.get())

        self.change_fonts()

    def resize_event_handler(self, args):
        vary.width = self.winfo_width()
        vary.height = self.winfo_height()

        text_field_array = [self.text_field]
        frame_array = [self.settings_widget]
        btn_array = [self.theme_btn, self.font_btn]

        for i in text_field_array:
            i.configure(width=vary.width)
            i.configure(height=(vary.height - 90))

        for i in frame_array:
            i.configure(width=vary.width)
            i.configure(height=vary.height)

        for i in btn_array:
            i.configure(width=vary.width)

    def close_event_handler(self):
        vary.width = self.winfo_width()
        vary.height = self.winfo_height()

        width = open('Assets/Data/width.txt', 'w').write(str(vary.width))
        height = open('Assets/Data/height.txt', 'w').write(str(vary.height))
        bg_clr = open('Assets/Data/bg_clr.txt', 'w').write(vary.bg_clr)
        txt_clr = open('Assets/Data/txt_clr.txt', 'w').write(vary.txt_clr)
        font_clr = open('Assets/Data/font_clr.txt', 'w').write(vary.font_clr)
        font = open('Assets/Data/font_fam.txt', 'w').write(vary.font)
        font_size = open('Assets/Data/font_size.txt', 'w').write(str(vary.font_size))
        txt_panel_clr = open('Assets/Data/txt_panel_clr.txt', 'w').write(vary.txt_panel_clr)
        widget_clr = open('Assets/Data/widget_clr.txt', 'w').write(vary.widget_clr)
        widget_hover_clr = open('Assets/Data/widget_hover_clr.txt', 'w').write(vary.widget_hover_clr)
        theme = open('Assets/Data/theme.txt', 'w').write(vary.themes)

        if msg.askyesno('Exit', 'Are you sure?'):
            self.quit()
