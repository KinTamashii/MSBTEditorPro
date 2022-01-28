from msbt import *
from util import *
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import sys, os

script_dir = os.path.dirname(sys.argv[0])
resources_dir = script_dir+'/resources/'
cache_file_dir = script_dir+"/cache/cache.txt"

class gui():
    def __init__(self):
        self.msbt = None
        self.file_open = False
        self.modified = False


        self.window = tk.Tk()
        self.window.title("Msbt Editor Pro v.0.10")
        self.window.configure(bg="#323232")
        self.window.minsize(width = 864, height = 550)
        self.window.geometry("864x550")
        self.window['padx'] = 5
        self.window['pady'] = 5

        menubar = tk.Menu(self.window)

        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Open", command= lambda: self.open_file())
        filemenu.add_command(label="Save", command= lambda: self.save())
        filemenu.add_command(label="Save As", command= lambda: self.save_as())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        cleantextmenu = tk.Menu(menubar, tearoff=0)
        cleantextmenu.add_command(label="Clean Export", command= lambda: self.clean_export())
        cleantextmenu.add_command(label="Batch Clean Export", command= lambda: self.batch_clean_export())
        cleantextmenu.add_separator()
        cleantextmenu.add_command(label="Auto Import", command= lambda: self.clean_import())
        cleantextmenu.add_command(label="Batch Auto Import", command= lambda: self.batch_clean_import())
        menubar.add_cascade(label="Clean Text", menu=cleantextmenu)

        codedtextmenu = tk.Menu(menubar, tearoff=0)
        codedtextmenu.add_command(label="Coded Export", command= lambda: self.coded_export())
        codedtextmenu.add_command(label="Batch Coded Export", command= lambda: self.batch_coded_export())
        codedtextmenu.add_separator()
        codedtextmenu.add_command(label="Import", command= lambda: self.coded_import())
        codedtextmenu.add_command(label="Batch Import", command= lambda: self.batch_coded_import())
        menubar.add_cascade(label="Coded Text", menu=codedtextmenu)

        self.window.config(menu=menubar)

        

        labels_list_frame = tk.Frame(self.window)
        labels_list_frame.grid(row=0,column=0, sticky=tk.NSEW)

        self.labels_label = tk.Label(labels_list_frame, text="String")
        self.labels_label.grid(row=0, columnspan=4)



        labels_listbox_subframe = tk.Frame(labels_list_frame)
        labels_listbox_subframe['padx'] = 5
        labels_listbox_subframe.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW)
        
        self.Labels_List = []
        self.labels_listbox_value = tk.StringVar(value=self.Labels_List)
        scrollbar = tk.Scrollbar(labels_listbox_subframe)
        self.labels_listbox = tk.Listbox(labels_listbox_subframe, listvariable=self.labels_listbox_value, yscrollcommand = scrollbar.set, exportselection=False)
        self.labels_listbox.bind("<<ListboxSelect>>", lambda _: self.listbox_change())
        scrollbar.config(command = self.labels_listbox.yview)
        self.labels_listbox.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)

        labels_listbox_subframe.grid_rowconfigure(0, weight=1)
        labels_listbox_subframe.grid_columnconfigure(0, weight=1)
        labels_listbox_subframe.grid_columnconfigure(1, weight=0)

        self.label_entry_var = tk.StringVar()
        label_entry = tk.Entry(labels_list_frame, textvariable=self.label_entry_var)
        label_entry.grid(row=2, column=0, sticky=tk.EW)

        save_icon_image = ImageTk.PhotoImage(Image.open(resources_dir+"save_icon.png"))
        self.save_label_button = tk.Button(labels_list_frame, image=save_icon_image, bg="#323232", state='disabled', command=lambda: self.save_label())
        self.save_label_button.grid(row=2, column=1)

        add_icon_image = ImageTk.PhotoImage(Image.open(resources_dir+"add_icon.png"))
        self.add_label_button = tk.Button(labels_list_frame, image=add_icon_image, bg="#323232", state='disabled', command=lambda: self.add_label())
        self.add_label_button.grid(row=2, column=2)

        remove_icon_image = ImageTk.PhotoImage(Image.open(resources_dir+"remove_icon.png"))
        self.remove_label_button = tk.Button(labels_list_frame, image=remove_icon_image, bg="#323232", state='disabled', command=lambda: self.remove_label())
        self.remove_label_button.grid(row=2, column=3)




        labels_list_frame.grid_rowconfigure(0, weight=0)
        labels_list_frame.grid_rowconfigure(1, weight=1)
        labels_list_frame.grid_rowconfigure(2, weight=0)
        labels_list_frame.grid_columnconfigure(0, weight=1)


    


        current_string_frame = tk.Frame(self.window)
        current_string_frame.grid(row=0, column=1, sticky=tk.NSEW)

        edit_label = tk.Label(current_string_frame, text="Edit")
        edit_label.grid(row=0, column=0)


        self.edit_string_text = CallbackText(current_string_frame)
        self.edit_string_text.bind("<<TextModified>>", lambda x : self.edit_text_change())
        self.edit_string_text.grid(row=1, column=0, sticky=tk.NSEW)

        self.restore_original_text_button = ttk.Button(current_string_frame, text="Restore Original", command=lambda: self.restore_original_text())
        self.restore_original_text_button['state'] = 'disabled'
        self.restore_original_text_button.grid(row=2, column=0)

        self.original_string_text = tk.Text(current_string_frame, state='disabled', height=15)
        self.original_string_text.grid(row=3, column=0, sticky=tk.EW)

        current_string_frame.grid_rowconfigure(0,weight=0)
        current_string_frame.grid_rowconfigure(1,weight=1)
        current_string_frame.grid_rowconfigure(2,weight=0)
        current_string_frame.grid_rowconfigure(3,weight=0)
        current_string_frame.grid_columnconfigure(0,weight=1)
        current_string_frame.grid_columnconfigure(1,weight=0)

        self.window.grid_rowconfigure(0,weight=1)
        self.window.grid_columnconfigure(0,weight=0)
        self.window.grid_columnconfigure(1,weight=1)

        self.window.mainloop()

    def open_file(self):
        if self.modified == True:
            match ConfirmationPrompt(self.window, "Msbt Editor Pro v.0.10", "Would you like to save before opening another file?", ("Yes", "No", "Cancel"), 2).choice:
                case 0:
                    self.save()
                    self.open_msbt()
                case 1:
                    self.open_msbt()
                case 2:
                    pass

        else:
            self.open_msbt()

    def open_msbt(self):
        new_dir = filedialog.askopenfilename(parent=self.window,
                                initialdir=get_initial_directory(cache_file_dir),
                                title="Please select an msbt file:",
                                filetypes=[("MSBT Files", ".msbt")])
        if new_dir != '': # If the user didn't cancel, the directory will not be empty.
            self.msbt_dir = new_dir
            self.window.title("Msbt Editor Pro v.0.10.0 - "+self.msbt_dir[self.msbt_dir.rindex("/")+1:])
            # Save the last directory the user was in.
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(self.msbt_dir[:self.msbt_dir.rindex("/")+1])
            cache_file.close()

            self.save_dir = self.msbt_dir
            self.msbt = msbt(self.msbt_dir)
            self.modified = False
            if self.msbt.has_labels:
                Label_List_Copy = self.msbt.lbl1.Labels.copy()
                Label_List_Copy.sort(key=lambda x: x.Index)
                self.Labels_List = [i.name for i in Label_List_Copy]
                self.save_label_button['state'] = 'normal'
                self.add_label_button['state'] = 'normal'
                self.remove_label_button['state'] = 'normal'
            else:
                self.Labels_List = [i for i in self.msbt.txt2.Strings]
                self.save_label_button['state'] = 'disabled'
                self.add_label_button['state'] = 'disabled'
                self.remove_label_button['state'] = 'disabled'
                
            self.labels_listbox_value.set(self.Labels_List)

            if len(self.Labels_List) > 0:
                self.labels_listbox.selection_set(0)
                self.listbox_change()
                self.restore_original_text_button['state'] = 'normal'

    def listbox_change(self):
        
        cur_index = self.labels_listbox.curselection()[0]
        self.labels_label.configure(text=f"String {cur_index}")
        self.label_entry_var.set(self.labels_listbox.get( cur_index ))

        # Prevent text from overwriting itself.
        self.edit_string_text.unbind("<<TextModified>>")
        self.edit_string_text.delete(1.0, tk.END)
        self.edit_string_text.insert(1.0, self.msbt.txt2.Strings[ cur_index ])
        self.edit_string_text.bind("<<TextModified>>", lambda x : self.edit_text_change())

        self.original_string_text['state'] = 'normal'
        self.original_string_text.delete(1.0, tk.END)
        self.original_string_text.insert(1.0, self.msbt.txt2.Original_Strings[ cur_index ])
        self.original_string_text['state'] = 'disabled'
        

    def edit_text_change(self):
        self.modified = True
        self.msbt.txt2.Strings[ self.labels_listbox.curselection()[0] ] = self.edit_string_text.get("1.0","end-1c")

    def restore_original_text(self):
        cur_index = self.labels_listbox.curselection()[0]
        self.edit_string_text.unbind("<<TextModified>>")
        self.msbt.txt2.Strings[cur_index] = self.msbt.txt2.Original_Strings[cur_index]
        
        self.edit_string_text.delete(1.0, tk.END)
        self.edit_string_text.insert(1.0, self.msbt.txt2.Strings[ cur_index ])
        self.edit_string_text.bind("<<TextModified>>", lambda x : self.edit_text_change())


    def save_label(self):
        new_label = self.label_entry_var.get()[:64]
        if new_label in self.Labels_List:
            pass
        else:
            cur_index = self.labels_listbox.curselection()[0]
            for i in range(len(self.msbt.lbl1.Labels)):
                if self.msbt.lbl1.Labels[i].name == self.Labels_List[cur_index]:
                    break
            self.msbt.rename_label(self.msbt.lbl1.Labels[i], new_label)
            self.Labels_List[cur_index] = new_label
            self.labels_listbox_value.set(self.Labels_List)
            self.modified = True

    def add_label(self):
        new_label = self.label_entry_var.get()[:64]
        if new_label in self.Labels_List:
            pass
        else:
            self.Labels_List += [new_label]
            self.labels_listbox_value.set(self.Labels_List)
            self.msbt.add_label(new_label)
            self.modified = True

    def remove_label(self):
        cur_index = self.labels_listbox.curselection()[0]
        match ConfirmationPrompt(self.window, "Msbt Editor Pro v.0.10", f"Are you sure you want to delete \"{self.Labels_List[cur_index]}\"?", ("Yes", "No"), 1).choice:
            case 0:
                for i in range(len(self.msbt.lbl1.Labels)):
                    if self.msbt.lbl1.Labels[i].name == self.Labels_List[cur_index]:
                        break
                self.msbt.remove_label(self.msbt.lbl1.Labels[i])
                self.Labels_List = self.Labels_List[:cur_index] + self.Labels_List[cur_index+1:]
                self.labels_listbox_value.set(self.Labels_List)
                self.modified = True
            case 1:
                pass


    def save(self):
        self.msbt.save(self.save_dir)
        self.modified = False

        # Update text when file is saved.
        self.original_string_text['state'] = 'normal'
        self.original_string_text.delete(1.0, tk.END)
        self.original_string_text.insert(1.0, self.msbt.txt2.Original_Strings[ self.labels_listbox.curselection()[0] ])
        self.original_string_text['state'] = 'disabled'

    def save_as(self):
        new_dir = filedialog.asksaveasfilename(parent=self.window,
                                        initialdir=get_initial_directory(cache_file_dir),
                                        title="Please create a name for your msbt file:",
                                filetypes=[("MSBT Files", ".msbt")])
        if new_dir != '':
            self.save_dir = new_dir

            # Save the last directory the user was in.
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(self.save_dir[:self.save_dir.rindex("/")+1])
            cache_file.close()

            self.save()


    def coded_export(self): # Export one msbt file to csv with control codes.
        csv_dir = filedialog.asksaveasfilename(parent=self.window,
                                        initialdir=get_initial_directory(cache_file_dir),
                                        title="Please create a name for your csv file:",
                                filetypes=[("Comma Seperated Value Files", ".csv")])
        if csv_dir != '' and self.msbt != None:
            # Save the last directory the user was in.
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(csv_dir[:csv_dir.rindex("/")+1])
            cache_file.close()
            coded_export(self.msbt, csv_dir)

    def batch_coded_export(self): # Export all msbt files in a directory to csv with control codes.
        msbt_folder_dir = filedialog.askdirectory(parent=self.window,
                            initialdir=get_initial_directory(cache_file_dir),
                            message="Please select a folder containing the msbt files:")

        if msbt_folder_dir != '':
            # Save the last directory the user was in.
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(msbt_folder_dir[:msbt_folder_dir.rindex("/")+1])
            cache_file.close()

            msbt_folder_dir += "/"

            csv_dir = filedialog.askdirectory(parent=self.window,
                            initialdir=get_initial_directory(cache_file_dir),
                            message="Please select a folder to export the files to:")

            if csv_dir != '':
                # Save the last directory the user was in.
                cache_file = open(cache_file_dir, 'w')
                cache_file.write(csv_dir[:csv_dir.rindex("/")+1])
                cache_file.close()

                csv_dir += "/"

                batch_coded_export(msbt_folder_dir, csv_dir)

    def coded_import(self): # Import one csv file to a msbt with control codes.
        csv_dir = filedialog.askopenfilename(parent=self.window,
                                initialdir=get_initial_directory(cache_file_dir),
                                title="Please select a csv file with \"coded\" strings:",
                                filetypes=[("Comma Seperated Value Files", ".csv")])
        if csv_dir != '' and self.msbt != None:
            # Save the last directory the user was in.
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(csv_dir[:csv_dir.rindex("/")+1])
            cache_file.close()
            coded_import(self.msbt, csv_dir, self.save_dir)
            self.modified = False
            
            cur_index = self.labels_listbox.curselection()[0]

            self.edit_string_text.unbind("<<TextModified>>")
            self.edit_string_text.delete(1.0, tk.END)
            self.edit_string_text.insert(1.0, self.msbt.txt2.Strings[ cur_index ])
            self.edit_string_text.bind("<<TextModified>>", lambda x : self.edit_text_change())

            self.original_string_text['state'] = 'normal'
            self.original_string_text.delete(1.0, tk.END)
            self.original_string_text.insert(1.0, self.msbt.txt2.Original_Strings[ cur_index ])
            self.original_string_text['state'] = 'disabled'

    def batch_coded_import(self): # Import all csv files in a directory to msbt with control codes.
        msbt_folder_dir = filedialog.askdirectory(parent=self.window,
                            initialdir=get_initial_directory(cache_file_dir),
                            message="Please select a folder containing the msbt files:")

        if msbt_folder_dir != '':
            # Save the last directory the user was in.
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(msbt_folder_dir[:msbt_folder_dir.rindex("/")+1])
            cache_file.close()

            msbt_folder_dir += "/"

            csv_dir = filedialog.askdirectory(parent=self.window,
                            initialdir=get_initial_directory(cache_file_dir),
                            message="Please select a folder containing the csv files:")

            if csv_dir != '':
                # Save the last directory the user was in.
                cache_file = open(cache_file_dir, 'w')
                cache_file.write(csv_dir[:csv_dir.rindex("/")+1])
                cache_file.close()

                csv_dir += "/"

                save_dir = filedialog.askdirectory(parent=self.window,
                                initialdir=get_initial_directory(cache_file_dir),
                                message="Please select a folder to save the new msbt files to:")

                if save_dir != '':
                    # Save the last directory the user was in.
                    cache_file = open(cache_file_dir, 'w')
                    cache_file.write(save_dir[:save_dir.rindex("/")+1])
                    cache_file.close()

                    save_dir += "/"

                    batch_coded_import(msbt_folder_dir, csv_dir, save_dir)

    def clean_export(self): # Export one msbt file to csv without codes.
        csv_dir = filedialog.asksaveasfilename(parent=self.window,
                                        initialdir=get_initial_directory(cache_file_dir),
                                        title="Please create a name for your csv file:",
                                filetypes=[("Comma Seperated Value Files", ".csv")])
        if csv_dir != '' and self.msbt != None:
            # Save the last directory the user was in.
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(csv_dir[:csv_dir.rindex("/")+1])
            cache_file.close()
            clean_export(self.msbt, csv_dir)

    def batch_clean_export(self): # Export all msbt files in a directory to csv without codes.
        msbt_folder_dir = filedialog.askdirectory(parent=self.window,
                            initialdir=get_initial_directory(cache_file_dir),
                            message="Please select a folder containing the msbt files:")

        if msbt_folder_dir != '':
            # Save the last directory the user was in.
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(msbt_folder_dir[:msbt_folder_dir.rindex("/")+1])
            cache_file.close()

            msbt_folder_dir += "/"

            csv_dir = filedialog.askdirectory(parent=self.window,
                            initialdir=get_initial_directory(cache_file_dir),
                            message="Please select a folder to export the files to:")

            if csv_dir != '':
                # Save the last directory the user was in.
                cache_file = open(cache_file_dir, 'w')
                cache_file.write(csv_dir[:csv_dir.rindex("/")+1])
                cache_file.close()

                csv_dir += "/"

                batch_clean_export(msbt_folder_dir, csv_dir)

    def clean_import(self): # Automatically format strings with control codes in a csv while importing it to an msbt.
        csv_dir = filedialog.askopenfilename(parent=self.window,
                                initialdir=get_initial_directory(cache_file_dir),
                                title="Please select a csv file with \"clean\" strings:",
                                filetypes=[("Comma Seperated Value Files", ".csv")])
        if csv_dir != '' and self.msbt != None:
            # Save the last directory the user was in.
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(csv_dir[:csv_dir.rindex("/")+1])
            cache_file.close()
            clean_import(self.msbt, csv_dir, self.save_dir)
            self.modified = False
            
            cur_index = self.labels_listbox.curselection()[0]

            self.edit_string_text.unbind("<<TextModified>>")
            self.edit_string_text.delete(1.0, tk.END)
            self.edit_string_text.insert(1.0, self.msbt.txt2.Strings[ cur_index ])
            self.edit_string_text.bind("<<TextModified>>", lambda x : self.edit_text_change())

            self.original_string_text['state'] = 'normal'
            self.original_string_text.delete(1.0, tk.END)
            self.original_string_text.insert(1.0, self.msbt.txt2.Original_Strings[ cur_index ])
            self.original_string_text['state'] = 'disabled'

    def batch_clean_import(self): # Automatically format strings with control codes in all csv in a directory while importing to msbt.
        msbt_folder_dir = filedialog.askdirectory(parent=self.window,
                            initialdir=get_initial_directory(cache_file_dir),
                            message="Please select a folder containing the msbt files:")

        if msbt_folder_dir != '':
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(msbt_folder_dir[:msbt_folder_dir.rindex("/")+1])
            cache_file.close()

            msbt_folder_dir += "/"

            csv_dir = filedialog.askdirectory(parent=self.window,
                            initialdir=get_initial_directory(cache_file_dir),
                            message="Please select a folder containing the \"clean\" csv files:")

            if csv_dir != '':
                # Save the last directory the user was in.
                cache_file = open(cache_file_dir, 'w')
                cache_file.write(csv_dir[:csv_dir.rindex("/")+1])
                cache_file.close()

                csv_dir += "/"

                save_dir = filedialog.askdirectory(parent=self.window,
                                initialdir=get_initial_directory(cache_file_dir),
                                message="Please select a folder to save the new msbt files to:")

                if save_dir != '':
                    # Save the last directory the user was in.
                    cache_file = open(cache_file_dir, 'w')
                    cache_file.write(save_dir[:save_dir.rindex("/")+1])
                    cache_file.close()

                    save_dir += "/"

                    batch_clean_import(msbt_folder_dir, csv_dir, save_dir)



gui()