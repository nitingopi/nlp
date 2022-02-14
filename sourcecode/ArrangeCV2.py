import os
from shutil import copyfile

# import docx2txt
import PyPDF2



import AnyToPdfConvertor
import pandas as pd

import ResumeMatcherVer2


class ArrangeCV:
    doc_path = ''
    template_path = ''
    keys = []
    Dict = {}

    def __init__(self, doc_path, template_path):
        self.doc_path = doc_path
        self.template_path = template_path
  

    def searchInPdf(self, document):
        """
        extracts the text from pdf

        Keyword arguments:
        document -- input file    
        """
        pdfFileObj = open(document, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        numpages = pdfReader.numPages
        pageStr = ""
        for i in range(0, numpages):
            pageObj = pdfReader.getPage(i)
            pageStr += pageObj.extractText()
        print(f'{document} -- {pageStr}')
        return pageStr

    def searchn_in_txt(self, document):
        """
        extracts the text from txt file

        Keyword arguments:
        document -- input file    
        """
        my_str = open(document, encoding="utf-8").read()
        return my_str

    def search_in_doc(self, document):
        """
        extracts the text from doc file

        Keyword arguments:
        document -- input file    
        """
        # my_str = docx2txt.process(document)
        # return my_str
        return ""


    def get_content(self):
        """
        extracts text from each file
        creates dataframe from each file
        plots final ouput
        """
        print(self.doc_path)
        if os.path.exists(self.doc_path):
            # gets instance of document convertor
            # convertor = AnyToPdfConvertor.DocumentConvertor(
            #     self.doc_path) 
            # convert .doc and .ppt to .pdf     
            # convertor.convert()

            final_database = pd.DataFrame()
            # gets instance of resume matcher
            resume_matcher = ResumeMatcherVer2.DocPlotter(self.doc_path, self.template_path)
            # loops through each file
            # creates final data frame
            for record in os.listdir(self.doc_path):
                document = self.doc_path + '/' + record
                print(f'document == {document}')
                if os.path.isfile(document):
                    text = ''
                    if document.endswith(".txt"):
                        text = self.searchn_in_txt(document)
                    if document.endswith(".pdf"):
                        text = self.searchInPdf(document)
                    if document.endswith(".docx"):
                        text = self.search_in_doc(document)
                    print(f'text = {text}')
                    if text != '':
                        # create data frame for each resume like below:
                        #   Candidate Name Subject Keyword               Count
                        # 0 cv1             ST      statistical models    5
                        # 1 cv1             ST      probability           1 
                        dat = resume_matcher.create_profile(document,text)
                        # append all the dataframes into final data frame
                        final_database = final_database.append(dat)
            print(final_database)
            # plots data collected from final dataframe
            resume_matcher.plot_data(final_database)


if __name__ == "__main__":
    template_path = "/home/nitin/python_ws/NLP_ver2/template/template.csv"
    doc_path = "/home/nitin/python_ws/NLP_ver2/resume"
    obj = ArrangeCV(doc_path, template_path)
    obj.get_content()
