
import re
#from nltk import sent_tokenize
from ner import Parser
from before_prediction_addon_code import replace_entities,replace_entities_original_form

f_text = open('01_Trade_Secrets_Rel14_267798.txt', "r",encoding='utf-8')

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


l=[]
for word in  paragraphed_text:
   # print(word)
    replace_entity=replace_entities(word, dict_for_readable)
    #print(replace_entity)
    l.append(replace_entity)

#paragraphed_text = [item for item in paragraphed_text if paragraphed_text]


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
            #inter = True
        
        if tag == 'other' and inside is True:
            
            if only_last_item is True:
                tag_name = "</"+tag_name+">"
                only_first_time = True
                only_last_item = False
                final_output.append(tag_name)
                
            final_output.append(item)
            inside = False
            started = False
            #inter = False
        if inside is False and "I-" in tag:
            final_output.append(item)    
    if started is True:
        final_output.append("</"+tag_name+">")
        started = False
    
        #inter = False
        
    for index, item in enumerate(final_output):

        mtc_1 = re.match(r'<\w+>', item)
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
list1=[]
for item in l:
    if item=='':
        final_text.append('\n')
    if item !="":
        #import pdb
        #pdb.set_trace()
        pred=pt.predict(item)
        list1.append(pred)
        item_text=post_processing_tagged_text(pt.predict(item))
        final_text.append(item_text)

## converting entities to respective readable form to original form

ll=[]
for words in final_text:
    print(words)
    #print(repitem(word))
    replace_entit=replace_entities_original_form(str(words),dict_for_original)
    #print(replace_entit)
    ll.append(replace_entit)

##save the predicted output file

f = open("tagged_text01.xml", "w",encoding='utf-8')

f.write('\n'.join(ll))

f.close()
f_text.close()








