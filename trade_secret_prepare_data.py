import os
import re
import nltk.data


file_path=r"C:\Users\PXM\Desktop\Implement_official_project\Entity_Recognition_WK-PLI\data\Sequence_label\new_data\test" # Please change the name of the directory here if needed
file_name=[filename for filename in os.listdir(file_path)] # Iterating over the list of the directory available in file path
print(len(file_name))

# This list contains text with tagged element inside it
data=[]
final_output_pre = []
final_output = []
# Currently this function is not in used, Please keep this function, may be we need custom method in future of data processing
def split_unicode(item):
	llist = re.split(r'(&#x\w{3,10};)', i)
	lllist = [t+" "+"other" for t in llist]
	lllist = [k for k in lllist if k]
	return lllist


def tag_line(filename):
	next_line_index_value = None
	with open(filename,'r') as f:
		contents=f.read()
		seperated_text_data = nltk.sent_tokenize(contents);

	for index, text in enumerate(seperated_text_data):

	    start=re.search(r'<(.*)>', text)

	    if start!=None or next_line_index_value == index:
	    	data.append(text)

	    if start!=None:
	    	next_line_index_value = index+1

#Iterating over tagged filename in particular direction(which has already been set above to the variable file_path, file_name) 
for item in file_name:
    
    file_fullname = os.path.join(file_path, item)
    tag_line(file_fullname)
    print(file_fullname)
    #break


inside = False
mtc_group = None
for index, item in enumerate(data):
	final_output.append('\n') #seperating the sentence with newline
	a_list = re.split(r'(<.*>)', item)
	for text in a_list:
		#removing the angular bracket from tagged text i.e. "<SN>" ==> "SN" and "</SN>" ==> "SN"
		text=re.sub('>','> ',str(text))
		text=re.sub('</',' </',text)
		for word in text.split():
			match=re.search(r'<\w+>',word)
			match1=re.search(r'</.*>',word)

			# If text is outside the tagged text
			if match is None and match1 is None and inside is False:

				another_text_splitting = nltk.word_tokenize(word)
				for i in word.split():

					if "[fn]" in i or "[/fn]" in i:
						i = i.replace("[fn]", "")
						i = i.replace("[/fn]", "")

					#Removed the code for spliting unicode
					# m = re.search(r'(&#x\d{4,10};)', i)
					# if m:
					# 	result = split_unicode(i)
					# 	if len(result) > 0:
					# 		final_output.extend(result)
					# 		continue

					#separating special character associated with word and treat as single entity
					item = re.split(r'(\(|\)|,|:|\[|\])', i)
					item = [k for k in item if k]
					txts = [j+" "+"other" for j in item]
					if len(txts) > 0:
						final_output.extend(txts)
						continue
				continue

			# checking opening tag in text
			if match1 is None and match is not None:
				mtc_group = match.group(0)
				mtc_group = re.sub("<", "", mtc_group)
				mtc_group = re.sub(">", "", mtc_group)
				inside = True
				FIRST_ITEM  = True
				continue

			# Checking for text inside the tagged text
			if match is None and match1 is None and inside is True:
				# Checking first item inside the tagged text and suffix with "B-TAG_NAME" otherwise "I_TAG_NAME"
				if FIRST_ITEM is True:
					txt = word+" "+"B-"+mtc_group
					final_output.append(txt)
					FIRST_ITEM = False
				else:
					item = re.split(r'(\(|\)|,|:)', word)
					item = [i for i in item if i]
					txt = [i+" "+"I-"+mtc_group for i in item]
					final_output.extend(txt)
				continue

			# Identifying the closing tag here
			if match is None and match1 is not None and inside is True:
				inside = False
				continue


final_output = final_output[1:] #Removing extra newline from top of the tokenize text

f = open("trade_test_data.txt", "a+") #Here you can change or edit the name of the file



for index, item in enumerate(final_output):
	print("item.....",item)
	if index == 0:
		continue
	if index == len(final_output)-2:
		break

	# Removing newline from S I-CASE \n SF I-CASE
	if item=='\n' and '-Case' in final_output[index-1] and '-Case' in final_output[index+2]:
		del final_output[index]
        
	# Removing newline from P. other \n Co. other
	if final_output[index-1].endswith('. other') is True and final_output[index+1].endswith('. other') is True:
		if item =='\n':
			del final_output[index]

	# Removing newline inbetween tagged text
	if final_output[index-1].endswith('.  I-Case') is True and final_output[index+1].endswith('.  I-Case') is True:
		if item == '\n':
			del final_output[index]

	# Removing newline in between open and closed paranthesis
	if final_output[index-1].endswith('. other') is True and final_output[index+2].endswith(') other') is True:
		if item == '\n':
			del final_output[index]

	# Improvised the code for sentence separation on top of the nltk.sent_tokenize. i.e. narrownly. Other \n In Other \n Words Other
	if final_output[index] != ". other" and final_output[index+1] == '\n' and final_output[index+2].replace(" other", "").istitle() is True and final_output[index].endswith('. other'):
		temp_text = final_output[index].replace(" other", "")
		if temp_text.endswith("."):
			temp_text_split = re.split(r'(\.)', temp_text)
			temp_text_split = [el for el in temp_text_split if el]
			temp_text_split = [eltk+" "+"other" for eltk in temp_text_split]
			if len(temp_text_split) == 2:
				final_output[index] = temp_text_split[0]
				final_output.insert(index+1, temp_text_split[1])

	# Checking for the case of opening and ending tag separation inbetween i.e. DSSFE I-Case \n CClbkaf I-Case
	if final_output[index] == '\n' and final_output[index-1].find("I-") != -1 and final_output[index+1].find("I-") != -1:
		if item == '\n':
			del final_output[index]

	# Checking for the case "B. B-Casename \n C. I-Casename"
	if final_output[index] == '\n' and final_output[index-1].replace(" other", "").find(".") >= 1 and final_output[index+1].replace(" other", "").find(".") != -1:
		if item == '\n':
			del final_output[index]

# Splitting ending text with "." to separate line
last_item = final_output[-1].replace(" other", "")
if last_item.endswith("."):
	last_item_split = re.split(r'(\.)', last_item)
	last_item_split = [el for el in last_item_split if el]
	last_item_split = [eltk+" "+"other" for eltk in last_item_split]
	if len(last_item_split) == 2:
		final_output[-1] = last_item_split[0]
		final_output.append(last_item_split[1])

# Fixing double newline for sentence seperation

for item in final_output:
	if item == '\n':
		final_output_pre.append(item)
	else:
		final_output_pre.append(item)
		final_output_pre.append("\n")

# removing newline from end of the list
if final_output_pre[-1] == '\n':
	del final_output_pre[-1]

#writing to the file

f.write(''.join(final_output_pre))

f.close()
