from xml.dom.minidom import parseString

# get some xml data from a file
file = open('qstatf.xml','r')
data = file.read()
file.close()

dom = parseString(data)

# get the first instance of the xml tag
xmlTag = dom.getElementsByTagName('slots_total')[0].toxml()
# strip the tag
xmlData = xmlTag.replace('<slots_total>','').replace('</slots_total>','')
print xmlTag
print xmlData
