'''
f_text = open('04_Trade_Secrets_Rel14_267798.txt', "r",encoding='utf-8')

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
## function for changing entities to their respective readable form
'''
def replace_entities(item, dict_for_readable):
    new_list=[]
    item=item.split()
    for items in item:
        if items !="":
            if items not in dict_for_readable.keys():
                new_list.append(items)
            if items in dict_for_readable.keys():             
                new_item=items.replace(items,str(dict_for_readable[items]))
                print(new_item)
                new_items=new_item.replace('[','')             
                new_items=new_items.replace(']','')
                new_items = new_items.split('\\n')
                new_items = "".join(new_items)               
                new_items=new_items.replace("'",'')
                new_list.append(new_items)
    t=' '.join(new_list)
    return t

## converting entities to respective readable form
'''   
l=[]
for word in  paragraphed_text:
    print(word)
    replace_entity=replace_entities(word,dict_for_readable)
    print(replace_entity)
    l.append(replace_entity)
'''


## function for changing back readable entities to their original form
def replace_entities_original_form(items, dict_for_original):
    n_list=[]
    n=[]
    itemst=items.split()
  
   
    
        
    for item in itemst:
        if itemst==[]:
            n_list.append('\n')
        
        print(item)
        if item !="":
            items=item+'\n' ## adding '\n' at the end os readable form because in dictionary '\n' added
            if items not in dict_for_original.keys():
                n_list.append(item)
            if items in dict_for_original.keys():
                new_item=items.replace(item,str(dict_for_original[items]))
                new_item = new_item.replace("\n",'') ##removing '\n'(that is automatically add) at the end of original word 
                n_list.append(new_item)
        
    n.append(' '.join(n_list))
    n_list.clear()
    tt=''.join(n)
    
    return tt

## converting entities to respective readable form to original form
'''
ll=[]
for words in l:
    print(words)
    #print(repitem(word))
    replace_entit=replace_entities_original_form(str(words),dict_for_original)
    print(replace_entit)
    ll.append(replace_entit)
     
'''


