
def replace_entities(item, dict_for_readable):
    item_list=[]
    item=item.split()
    for items in item:
        if items !="":
            if items not in dict_for_readable.keys():
                item_list.append(items)
            if items in dict_for_readable.keys():             
                new_item=items.replace(items,str(dict_for_readable[items]))
                #print(new_item)
                new_items=new_item.replace('[','')             
                new_items=new_items.replace(']','')
                new_items = new_items.split('\\n')
                new_items = "".join(new_items)               
                new_items=new_items.replace("'",'')
                item_list.append(new_items)
    final_item_list=' '.join(item_list)
    return final_item_list




## function for changing back readable entities to their original form
def replace_entities_original_form(items, dict_for_original):
    item_list=[]
    join_item_list=[]
    itemst=items.split()    
    for item in itemst:
        if itemst==[]:
            item_list.append('\n')
        #print(item)
        if item !="":
            items=item+'\n' ## adding '\n' at the end os readable form because in dictionary '\n' added
            if items not in dict_for_original.keys():
                item_list.append(item)
            if items in dict_for_original.keys():
                new_item=items.replace(item,str(dict_for_original[items]))
                new_item = new_item.replace("\n",'') ##removing '\n'(that is automatically add) at the end of original word 
                item_list.append(new_item)
        
    join_item_list.append(' '.join(item_list))
    item_list.clear()
    final_item_list=''.join(join_item_list)
    
    return final_item_list




