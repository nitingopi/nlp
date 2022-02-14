# Resume Phrase Matcher code
# importing all required libraries

import PyPDF2
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
import pandas as pd
from collections import Counter
import en_core_web_sm
from spacy.matcher import PhraseMatcher

class DocPlotter:
    doc_path = ''
    template_path = ''
    only_files = ''
    nlp = en_core_web_sm.load()

    def __init__(self, doc_path, template_path):
        self.doc_path = doc_path
        self.template_path = template_path
        self.only_files = [os.path.join(self.doc_path, f) for f in os.listdir(self.doc_path) if
                     os.path.isfile(os.path.join(self.doc_path, f))]

    
    def create_profile(self,file,text):
        """
        reads csv template using pandas
        reads text from the file given
        create data frame for each file like below:
          Candidate Name Skill        Keyword          Count
        0  cv1             ST        statistical models    5
        1  cv1             ST        probability           1 
        
        Keyword arguments:
        file -- input file
        text -- text extracted from file

        Return value:
        dataf -- dataframe created from each file using template document.
        """
        text = str(text)
        text = text.replace("\\n", "")
        text = text.lower()
        headers = pd.read_csv(self.template_path,  nrows=0)
        key_list = headers.columns.tolist()
        keyword_dict = pd.read_csv(self.template_path)
        key_dict = {}
        # creates a dictionary 
        # key = skill
        # value = list containing subskills
        for key in key_list:
            key_dict[key] = [self.nlp(text) for text in keyword_dict[key].dropna(axis=0)]

        matcher = PhraseMatcher(self.nlp.vocab)
        for key in key_dict.keys():
            start = key.index('(')+1
            end = key.index(')') 
            key_place = key[start:end]
            matcher.add(key_place, None, *key_dict[key])

        doc = self.nlp(text)

        d = []
        matches = matcher(doc)
        for match_id, start, end in matches:
            rule_id = self.nlp.vocab.strings[match_id]  
            print("rule id ",rule_id)
            span = doc[start: end]  # get the matched slice of thde doc
            print("span ",span)
            d.append((rule_id, span.text))
        # creates string separated by \n
        # each line has following text
        # e.g. -> 'ST statistical models (5)
        #          ST probability (1)'
        keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i, j in Counter(d).items())

        # convertimg string of keywords to dataframe
        # e.g. -> Skill         Keyword           Count
        #      0      ST      statistical models      5
        #      1      ST      probability             1
        
        df = pd.read_csv(StringIO(keywords), names=['Keywords_List'])
        df1 = pd.DataFrame(df.Keywords_List.str.split(' ', 1).tolist(), columns=['Skill', 'Keyword'])
        df2 = pd.DataFrame(df1.Keyword.str.split('(', 1).tolist(), columns=['Keyword', 'Count'])
        df3 = pd.concat([df1['Skill'], df2['Keyword'], df2['Count']], axis=1)
        df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))

        base = os.path.basename(file)
        filename = os.path.splitext(base)[0]

        name = filename.split('_')
        name2 = name[0]
        name2 = name2.lower()
        ## converting str to dataframe
        name3 = pd.read_csv(StringIO(name2), names=['Candidate Name'])

        dataf = pd.concat([name3['Candidate Name'], df3['Skill'], df3['Keyword'], df3['Count']], axis=1)
        dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace=True)

        return (dataf)


# function ends


# code to count words under each category and visulaize it through Matplotlib

    def plot_data(self, final_database):
        """
        Takes input of final dataframe of all the resume documents
        Plots the dataframe using matplotlib

        Keyword arguments:
        final_database -- final dataframe of all the resume documents
        """   
        final_database2 = final_database['Keyword'].groupby(
            [final_database['Candidate Name'], final_database['Skill']]).count().unstack()
        final_database2.reset_index(inplace=True)
        final_database2.fillna(0, inplace=True)
        new_data = final_database2.iloc[:, 1:]
        new_data.index = final_database2['Candidate Name']
        # execute the below line if you want to see the candidate profile in a csv format
        sample2=new_data.to_csv('sample.csv')
        import matplotlib.pyplot as plt

        plt.rcParams.update({'font.size': 10})
        ax = new_data.plot.barh(title="Resume keywords by category", legend=True, figsize=(25, 7), stacked=True)
        # uncomment the below block to display skills and count in the chart
        """ labels = []
        for j in new_data.columns:
            for i in new_data.index:
                label = str(j) + ": " + str(new_data.loc[i][j])
                labels.append(label)
        patches = ax.patches
        for label, rect in zip(labels, patches):
            width = rect.get_width()
            if width > 0:
                x = rect.get_x()
                y = rect.get_y()
                height = rect.get_height()
                ax.text(x + width / 2., y + height / 2., label, ha='center', va='center') """
        plt.show()

