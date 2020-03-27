# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 10:05:01 2020

@author: PXM
"""

import os
import re
import sys
from ner import Parser
from before_prediction_addon_code import replace_entities,replace_entities_original_form
file_name=str(sys.argv[1])
#print(file_name)
file_name_modify=re.sub("(\.).*",'',file_name)
#print(file_name_modify)
read_file_text = open(os.path.join("input",file_name), "r", encoding='utf-8')
f_text = open("File_7.xml", "r", encoding='utf-8')
text = f_text.read()

paragraphed_text = text.split("\n")

## making dictionary of special entities

with open(r'entities.txt',encoding="utf8") as fin:    
     rows = ( line.split('\t') for line in fin )
     dict_for_readable = { row[0]:row[1:] for row in rows }
     
## making dictionary of special entities
with open(r'entities.txt',encoding="utf8") as fin:    
     rows = ( line.split('\t') for line in fin )
     dict_for_original = { row[1]:row[0] for row in rows }

pt = Parser()

pt.load_models()


readable_words=[]
for word in  paragraphed_text:
    replace_entity=replace_entities(word, dict_for_readable)
    readable_words.append(replace_entity)

##prediction post processing
    
    
def post_processing_tagged_text(tagged_text):
    final_output = []
   
    started = False
    inside = False
    only_first_time = True
    only_last_item = False
    for item, tag in tagged_text:

        if tag == 'other' and inside is False:
            final_output.append(item)
        
        if "B-" in tag:
            if only_first_time is True:
                tag_name = tag.replace("B-", "")
                tag_name_with_angular = "<"+tag_name+">"
                only_last_item = True
                only_first_time = False
                started = True
                final_output.append(tag_name_with_angular)
                
            final_output.append(item)
            inside = True
            continue
        
        if inside is True and "I-" in tag:
            final_output.append(item)
            started = False
        
        if tag == 'other' and inside is True and started is False:
         
            if only_last_item is True:
                #tag_name ="</"+tag_name+">"
                replace_word=str(final_output[-1])
                mtc=re.match(r'(.*)(,)',replace_word)
                if mtc!=None:
                    mtc_word=mtc.group(0)
                    rep_word=mtc_word.replace(",",'')
                    final_output[-1]=rep_word
                    tag_name ="</"+tag_name+">,"
                    final_output.append( tag_name)
                    
                else:
                    tag_name ="</"+tag_name+">"
                    final_output.append( tag_name)
                only_first_time = True
                only_last_item = False
                
                
            final_output.append(item)
            inside = False
            started = False
        if inside is False and "I-" in tag:
            final_output.append(item)
        if inside is True and started is True and tag == 'other':
            rep=str(final_output[-2])
            repp=rep.replace(tag_name_with_angular,"")
            final_output[-2]=repp
            #final_output.append("</"+tag_name+">")
            inside = False
            started = False
    if started is True:
        #final_output.append("</"+tag_name+">")
        rep=str(final_output[-2])
        repp=rep.replace(tag_name_with_angular,"")
        final_output[-2]=repp        
        started = False
        inside = False 
    #if inside is True and started is False:
        #final_output.append("</"+tag_name+">")
        #inside = False

    for index, item in enumerate(final_output):

        mtc_1 = re.match(r'<\w+>', item)
        
        if index+1 == len(final_output):
            continue
       
        if mtc_1:
           
            final_output[index] = final_output[index] + final_output[index+1]
            del final_output[index+1]
        
        mtc_2 = re.match(r'</.*>', item)
        if mtc_2 and index != 0:
            final_output[index-1] = final_output[index-1]+final_output[index]
            del final_output[index]
    
    for index, item in enumerate(final_output):
        if item in ['(', ')', ',', '.', ':', '[', ']', '{', '}'] and index != 0:
            final_output[index-1] = final_output[index-1]+final_output[index]
            del final_output[index]	


    return ' '.join(final_output)


##prediction
    
final_text = []
for item in readable_words:
    if item=='':
        final_text.append('\n')
    if item !="":   
        item_text=post_processing_tagged_text(pt.predict(item))
        final_text.append(item_text)

   
 
#str1='\n'.join(final_text)  
def inc_modify(final_text):
    start=False
    inside=False
    
    output=[]
    #x=" hello <casename>Tanbro Fabrics Corp. v. Deering Milliken, Inc.Tanbro Fabrics Corp. v. Deering Milliken, Inc.,Funding Sys. Asset Mgmt. Corp. &#x0026; F/S Computer Corp., 111 B.R. 500 (Bankr. W.D. Pa. 1990).Tanbro Fabrics Corp.</casename> false"
    tagname=""
    for list_line in final_text.split():
        #print(list_line)
        #if '' in list_line:
            #print("yes")
            #output.append('\n')
        #if '' not in list_line: 
            #print("no")
            #for list_word in list_line.split():
                #print(list)       
        mtc=re.match(r"<[a-z]*>[A-Z][a-z]*",list_line)
        mtch=re.match(r"Inc.[A-Z][a-z]*",list_line)
        mtch1=re.match(r"Inc.,[A-Z][a-z]*",list_line)
        mtch2=re.match(r"(.*)</[a-z]*>",list_line)
       
        if mtc!=None:
            #print(mtc.group(0))
            word=mtc.group(0)
            w=re.findall(r"<.*>",word)        
            str2=' '.join(w)
            #print(str2)
            ww=str2.replace("<","")
            www=ww.replace(">","")
            tagname=www
            output.append(word)
            start=True
            inside=True
        if  inside==True and mtc==None and mtch ==None and mtch1==None and mtch2==None:
            output.append(list_line)   
            
        if inside==False and mtc==None and mtch==None and mtch1==None and mtch2==None:
            output.append(list_line)
            
            
        if inside==True and mtc==None and mtch!=None and mtch1==None and mtch2==None:
            m=mtch.group(0)
            words = re.findall('[A-Z][a-z]*', m)
            #print(words)
            for word in words:
                if word=="Inc":
                    output.append("Inc."+"</"+tagname+"> <"+tagname+">")
                    
                else:
                   output .append(word)
                   
        if inside==True and mtc==None and mtch==None and mtch1!=None and mtch2==None:
            m1=mtch1.group(0)
            words = re.findall('[A-Z][a-z]*', m1)
            for word in words:
                if word=="Inc":
                    output.append("Inc."+"</"+tagname+">,<"+tagname+">")
                    
                else:
                   output .append(word)          
                   
        if inside==True and mtc==None and mtch==None and mtch1==None and mtch2!=None:
             
             output.append(list_line)
             inside=False
             start=False
             tagname=""

    return ' '.join(output)
modify_output=[]
for list_ in final_text:
    print(list_)
    if  list_=='':
        modify_output.append('\n')
        print("yes")
    else:
        print("no")
        print(list_)
        mod_output=inc_modify(list_)
        print("mod_output.............",mod_output)
        modify_output.append(mod_output)
        
        

## converting entities to respective readable form to original form

original_words=[]
for words in modify_output:
    replace_entit=replace_entities_original_form(str(words),dict_for_original)
    original_words.append(replace_entit)

##save the predicted output file
s='\n'.join(original_words)
save_file = open("File_7"+".txt", "w",encoding='utf-8')

save_file.write('\n'.join(original_words))

save_file.close()
#read_file_text.close()
f_text.close()



'''


 
    for item in final_output:
        print("item....",item)
        mtch=re.match(r"Inc.[A-Z][a-z]*",item)
        mtch1=re.match(r"Inc.,[A-Z][a-z]*",item)
        mtch2=re.match(r"Inc.,",item)
        if mtch!=None:
            print(mtch.group(0))
            m=mtch.group(0)
            words = re.findall('[A-Z][a-z]*', m)
            for word in words:
                if word=="Inc":
                    final_output.append("Inc."+"</"+tag_name+"> <"+tag_name+">")
                    
                else:
                   final_output .append(word)
        if mtch1!=None:
            print(mtch1.group(0))
            m1=mtch1.group(0)
            words = re.findall('[A-Z][a-z]*', m1)
            for word in words:
                if word=="Inc":
                    final_output.append("Inc."+"</"+tag_name+"> <"+tag_name+">")
                    
                else:
                   final_output .append(word)    
    
        if mtch1==None and mtch2!=None:
            print(mtch2.group(0))
            m2=mtch2.group(0)
            words = re.findall('[A-Z][a-z]*', m2)
            for word in words:
                if word=="Inc":
                    final_output.append("Inc."+"</"+tag_name+">,<"+tag_name+">")
                    
                else:
                   final_output .append(word)
        if mtch==None and mtch1==None and mtch2==None:            
            final_output.append(item)
        started = False