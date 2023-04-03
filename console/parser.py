import string
with open("text.txt", 'r') as file:
    all_text = file.read()
    sentenses = all_text.split('.')
    for i in range(len(sentenses)):
        sentenses[i] = sentenses[i].replace('\n', '')
        sentenses[i] = sentenses[i].replace('!', '')
        sentenses[i] = sentenses[i].replace('`', '')
        sentenses[i] = sentenses[i].replace('~', '')
        sentenses[i] = sentenses[i].replace('"', '')
        sentenses[i] = sentenses[i].replace("'", '')
        sentenses[i] = sentenses[i].replace("(", '')
        sentenses[i] = sentenses[i].replace(")", '')
        sentenses[i] = sentenses[i].replace("?", '')
        sentenses[i] = sentenses[i].replace("”", '')
        sentenses[i] = sentenses[i].replace("“", '')
        #sentenses[i] = sentenses[i].replace("-", '')
        sentenses[i] = sentenses[i].replace("’", '')
        sentenses[i] = sentenses[i].replace("—", '-')
        sentenses[i] = sentenses[i].strip()
        alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
        if (len(sentenses[i]) >= 1) and (not sentenses[i][0] in alphabet):
            sentenses[i] = sentenses[i][1:]
        sentenses[i] = sentenses[i].strip()
    for i in range(len(sentenses)):
        try:
            sentenses.remove('')
        except:
            a = 0
    ans = []
    for i in sentenses:
        if len(i) >= 10:
            ans.append(i) 
print(ans)          
with open("sentenses.txt", 'w') as file:
    for sentense in ans:
        file.write(sentense + '.\n')
