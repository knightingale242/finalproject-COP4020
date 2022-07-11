topic = 'AnalysisOfAlgoriths'
PaperID = 11
author_id = 1
title = "testpaper"
file = 'doc.x'
statement = "INSERT INTO paper (PaperID, AuthorID, Title, FilenameOriginal, %s) VALUES (%d, %d, %s, %s, 1)"
values = (topic, PaperID, author_id, title, file)
input = statement % values
print(input)