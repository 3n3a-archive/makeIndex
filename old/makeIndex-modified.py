import os
from pathlib import 

indexTextStart = """<!DOCTYPE html>
<html>
<head>
    <title>Index of {folderPath}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, intial-scale=1">
    <link rel="preload" href="https://cdn.jsdelivr.net/npm/spcss@0.4.0" as="style">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/spcss@0.4.0">
</head>
<body>
    <h2>Index of {folderPath}</h2>
    <hr>
    <ul>
		<li>
			<a href='../'>../</a>
		</li>
"""
indexTextEnd = """
	</ul>
</body>
</html>
"""

def index_folder(folderPath):
	print("Indexing: " + folderPath +'/')
	#Getting the content of the folder
	files = os.listdir(folderPath)
	#If Root folder, correcting folder name
	root = folderPath
	if folderPath == '.':
		root = 'Root'
	indexText = indexTextStart.format(folderPath=root)
	for file in files:
		#Avoiding index.html files
		if file != 'index.html':
			indexText += "\t\t<li>\n\t\t\t<a href='" + file + "'>" + file + "</a>\n\t\t</li>\n"
		#Recursive call to continue indexing
		if os.path.isdir(folderPath+'/'+file):
			index_folder(folderPath + '/' + file)
	indexText += indexTextEnd
	#Create or override previous index.html
	index = open(folderPath+'/index.html', "w") # TODO: save with io library
	#Save indexed content to file
	index.write(indexText)

#Indexing root directory (Script position)
index_folder('.')