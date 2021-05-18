import io
import json
import re
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def extraction(path):

    output_string = StringIO()
    with open(path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    t1=output_string.getvalue() #contenu de fichier pdf
    #jusqu'a ici nous avons lus notre fichier pdf

    #extraire des competences CT SKILLS
    CT_Skills = []#liste qui contient les compétences ordonnées
    for line in t1.splitlines():
        x = re.findall("^CT Skills", line)
        if x:
            a=line.replace("CT Skills ", " ")
            CT_Skills.append(a)

    #extraire des competences CT domaine
    CS_Domain = []#liste qui contient les cs ordonnées
    for line in t1.splitlines():
        x = re.findall("^CS Domain", line)
        if x:
            a=line.replace("CS Domain - ", " ")
            CS_Domain.append(a)

    #extraire la page des noms des exercices
    fp = open(path, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    device = TextConverter(rsrcmgr, retstr,  laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    page_no = 4

    for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        if pageNumber == page_no:
            interpreter.process_page(page)

    data = retstr.getvalue()

    list0=[]
    for line in data.splitlines():
        x = re.findall("^page", line)

        if not x:
            a=line.replace("^page", " ")
            list0.append(a)

    for i in list0:
        if i=='' or i==' 5' :
            list0.remove(i)
    list1=list0[:len(list0)-3]
    for j in range(0,len(list1)):
        if list1[j]=="Contents":
            list2=list1[(j+1):]
            list3=list1[:(j)]
    list=list2 + list3 #liste qui contient les noms d'exercices ordonnés
    zip0= zip(list,CT_Skills)
    zip1= zip(list,CS_Domain)
    d1=dict(zip0)#dictionnaire contient comme clés les noms des exercices et comme valeurs les competences
    d2=dict(zip1)#dictionnaire contient comme clés les noms des exercices et comme valeurs les CS domaines
    #les noeds des exercices
    j=20
    dict_id={}
    noed_ex=''#string des noeds des exercices
    for i in list:
        ex_obj='{"type":"node","id":"'+str(j)+'","labels":["exercice"],"properties":{"name":"'+i+'"}}'
        j+=1
        noed_ex+=ex_obj+"\n"
        dict_id[i]=j


    #les noeds des relations:
    #relation abstraction-ses exercices, résultat dans string_relationship_abs
    c2=100
    string_relationship_abs=''
    for key,value in d1.items():
        if(("Abstraction" in value)==True):
            for i, j in dict_id.items():
                if key==i:
                    strin='{"id":"'+str(c2)+'","type":"relationship","label":"Treated by","start":{"id":"3","labels":["Abstraction"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c2+=1
                    string_relationship_abs+=strin+"\n"
    ctsk1=string_relationship_abs

    #relation algorithmic thinking-ses exercices, résultat dans string_relationship_algo_think
    c3 = 150
    string_relationship_think = ''
    for key, value in d1.items():
        if (("Algorithmic Thinking" in value) == True):
            for i, j in dict_id.items():
                if key == i:
                    strin = '{"id":"'+str(c3)+'","type":"relationship","label":"Treated by","start":{"id":"4","labels":["Algorithmic Thinking"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c3 += 1
                    string_relationship_think+=strin+"\n"
    ctsk2=string_relationship_think

    #relation decomposition-ses exercices, résultat dans string_relationship_dec
    c4 = 200
    string_relationship_dec = ''
    for key, value in d1.items():
        if (("Decomposition" in value) == True):
            for i, j in dict_id.items():
                if key == i:
                    strin = '{"id":"'+str(c4)+'","type":"relationship","label":"Treated by","start":{"id":"5","labels":["Decomposition"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c4+=1
                    string_relationship_dec+=strin+"\n"
    ctsk3=string_relationship_dec

    #relation evaluation-ses exercices, résultat dans string_relationship_ev
    c5 = 250
    string_relationship_ev = ''
    for key, value in d1.items():
        if (("Evaluation" in value) == True):
            for i, j in dict_id.items():
                if key == i:
                    strin = '{"id":"'+str(c5)+'","type":"relationship","label":"Treated by","start":{"id":"6","labels":["Evaluation"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c5 += 1
                    string_relationship_ev += strin + "\n"
    ctsk4=string_relationship_ev

    #relation generalisation-ses exercices, résultat dans string_relationship_gen
    c6 = 300
    string_relationship_gen = ''
    for key, value in d1.items():
        if (("Generalisation" in value) == True):
            for i, j in dict_id.items():
                if key == i:
                    strin = '{"id":"'+str(c6)+'","type":"relationship","label":"Treated by","start":{"id":"7","labels":["Generalisation"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c6 += 1
                    string_relationship_gen += strin + "\n"
    ctsk5=string_relationship_gen

    c7 = 350
    string_relationship_alg_nd_prog = ''
    for key, value in d2.items():
        if (("Algorithms and programming" in value) == True):
            for i, j in dict_id.items():
                if key == i:
                    strin = '{"id":"'+str(c7)+'","type":"relationship","label":"Treated by","start":{"id":"8","labels":["Algorithms and programming"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c7 += 1
                    string_relationship_alg_nd_prog += strin + "\n"
    csdo1 = string_relationship_alg_nd_prog

    c8 = 400
    string_relationship_data_struc_repr = ''
    for key, value in d2.items():
        if (("Data, data structures and representations" in value) == True):
            for i, j in dict_id.items():
                if key == i:
                    strin = '{"id":"'+str(c8)+'","type":"relationship","label":"Treated by","start":{"id":"9","labels":["Data, data structures and representations"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c8 += 1
                    string_relationship_data_struc_repr += strin + "\n"
    csdo2 = string_relationship_data_struc_repr

    c9 = 450
    string_relationship_comp_proc_hard = ''
    for key, value in d2.items():
        if (("Computer processes and hardware" in value) == True):
            for i, j in dict_id.items():
                if key == i:
                    strin = '{"id":"'+str(c9)+'","type":"relationship","label":"Treated by","start":{"id":"10","labels":["Computer processes and hardware"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c9 += 1
                    string_relationship_comp_proc_hard += strin + "\n"
    csdo3 = string_relationship_comp_proc_hard

    c10 = 500
    string_relationship_comm_net= ''
    for key, value in d2.items():
        if (("Communication and networking" in value) == True):
            for i, j in dict_id.items():
                if key == i:
                    strin = '{"id":"'+str(c9)+'","type":"relationship","label":"Treated by","start":{"id":"11","labels":["Communication and networking"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c10 += 1
                    string_relationship_comm_net += strin + "\n"
    csdo4 = string_relationship_comm_net

    c11 = 500
    string_relationship_int_sys_soc = ''
    for key, value in d2.items():
        if (("Interactions, systems and society" in value) == True):
            for i, j in dict_id.items():
                if key == i:
                    strin = '{"id":"'+str(c9)+'","type":"relationship","label":"Treated by","start":{"id":"12","labels":["Interactions, systems and society"]},"end":{"id":"'+str(j)+'",labels":["'+str(i)+'"]"}}'
                    c11 += 1
                    string_relationship_int_sys_soc += strin + "\n"
    csdo5 = string_relationship_int_sys_soc


    f01=open("input01.txt","r")
    input_txt01=f01.read()
    f02=open("input02.txt","r")
    input_txt02=f02.read()
    output_text=input_txt01+noed_ex+input_txt02+"\n"+ctsk1+ctsk2+ctsk3+ctsk4+ctsk5+csdo1+csdo2+csdo3+csdo4+csdo5
    f1=open("output.txt","w+")
    f1.write(output_text)


    return d1

