from tkinter import *
from tkinter.filedialog import askdirectory, askopenfile, askopenfilename
from tkinter.constants import *
from tkinter import messagebox

import ArrangeCV2

root = Tk()
root.title("CV classification")
root.geometry("700x300")

skills = []
selectedSkills = []
doc_var = StringVar()
# myskills = StringVar()
template_var = StringVar()


def show_process_finished_msg():
    """
    This method dislays the messge 'process finished' when the process is finished.
    """
    messagebox.showinfo("CV segragation", "Process finished")
    root.destroy() # this line will be executed after the messagebox is closed


def submit_handler():
    """
    Retrieves the path of template file and resume folder.
    Calls method get_content from ArrangeCV2 class and passes the path of template and documents.
    """
    doc_path = doc_var.get().replace("/", "\\")
    template_path = template_var.get().replace("/", "\\")
    handler = ArrangeCV2.ArrangeCV(doc_path, template_path)
    handler.get_content()
    show_process_finished_msg()


def cancel_handler():
    """
    Closes the UI.
    """
    root.destroy()


def open_docs():
    """
    shows dialogue box to open the resume documents 
    """
    doc_path = askdirectory()
    doc_var.set(doc_path)


def open_template():
    """
    shows the dialogue box to open the template file
    """
    template_path = askopenfilename()
    template_var.set(template_path)


def create_widgets():
    """
    create the GUI
    get the path of templates
    get the path of resume  
    """
    row_count = 0

    # create label for template browser
    title_template = Label(root, padx=40, pady=50, text="Please select path to template", font=("bold", 14))
    title_template.grid(row=row_count, sticky=W)

    # create template browser
    template_path = Entry(root, width=40, textvariable=template_var)
    template_path.grid(row=row_count, sticky=W, padx=350)
    temp_browse_btn = Button(root, text='Browse', command=open_template)
    temp_browse_btn.grid(row=row_count, sticky=W, padx=600)

    # create label for file browser
    row_count += 1
    title_docs = Label(root, padx=40, pady=10, text="Please select path to resumes", font=("bold", 14))
    title_docs.grid(sticky=W)

    # create file browser
    docs_path = Entry(root, width=40, textvariable=doc_var)
    docs_path.grid(row=row_count, sticky=W, padx=350)
    docs_browse_btn = Button(root, text='Browse', command=open_docs)
    docs_browse_btn.grid(row=row_count,  sticky=W,  padx=600)

    # create submit and cancel button
    row_count += 1
    submit_btn = Button(root, text='Submit', width=10, command=submit_handler)
    submit_btn.grid(row=row_count, sticky=W, padx=350, pady=25)
    cancel_btn = Button(root, text='Close', width=10, command=cancel_handler)
    cancel_btn.grid(row=row_count, sticky=W, padx=450,  pady=25)


create_widgets()
root.mainloop()
