import os.path

# import win32com.client


class DocumentConvertor():
    baseDir = ''  # Starting directory for directory walk

    def __init__(self, baseDir):
        self.baseDir = baseDir  # "D:\\Nitin\\sampleTesting\\demo\\test"
        print('base dir'+baseDir)

    def convert(self):
        ppt = win32com.client.Dispatch("PowerPoint.application")
        word = win32com.client.Dispatch("Word.application")
        # for dir_path, dirs, files in os.walk(self.baseDir): # return root,directories,files
        files = os.listdir(self.baseDir) 
        for file_name in files:
            file_path = os.path.join(self.baseDir, file_name)
            file_name, file_extension = os.path.splitext(file_path)
            if file_extension.lower() == '.ppt':  #
                pdf_file = os.path.splitext(
                    file_path)[0] + "_111.pdf"  # 111 for ppt files
                # Skip conversion where pptx file already exists
                if not os.path.isfile(pdf_file):
                    print('Converting: {0}'.format(file_path))
                    try:
                        ppt_doc = ppt.Presentations.Open(
                            file_path, False, False, False)
                        ppt_doc.SaveAs(pdf_file, FileFormat=32)
                        ppt_doc.Close()
                        print('Converted: {0}'.format(pdf_file))
                    except Exception:
                        print('Failed to Convert: {0}'.format(file_path))
            if file_extension.lower() == '.doc':  #
                pdf_file = os.path.splitext(
                    file_path)[0] + "_222.pdf"  # 222 for doc files
                # Skip conversion where docx file already exists
                if not os.path.isfile(pdf_file):
                    print('Converting: {0}'.format(file_path))
                    try:
                        word_doc = word.Documents.Open(
                            file_path, False, False, False)
                        word_doc.SaveAs(pdf_file, FileFormat=17)
                        word_doc.Close()
                        print('Converted: {0}'.format(pdf_file))
                    except Exception:
                        print('Failed to Convert: {0}'.format(file_path))

        ppt.Quit()
        word.Quit()
