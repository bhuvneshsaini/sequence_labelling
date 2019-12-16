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
#f_text = open("01_Trade_Secrets_Rel14_267798.xml", "r", encoding='utf-8')
text = read_file_text.read()

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
        
        if tag == 'other' and inside is True:
            
            if only_last_item is True:
                tag_name = "</"+tag_name+">"
                only_first_time = True
                only_last_item = False
                final_output.append(tag_name)
                
            final_output.append(item)
            inside = False
            started = False
        if inside is False and "I-" in tag:
            final_output.append(item)    
    if started is True:
        final_output.append("</"+tag_name+">")
        started = False
        inside = False 
    if inside is True and started is False:
        final_output.append("</"+tag_name+">")
        inside = False

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

## converting entities to respective readable form to original form

original_words=[]
for words in final_text:
    replace_entit=replace_entities_original_form(str(words),dict_for_original)
    original_words.append(replace_entit)

##save the predicted output file

save_file = open("output/"+file_name_modify+".txt", "w",encoding='utf-8')

save_file.write('\n'.join(original_words))

save_file.close()
read_file_text.close()








