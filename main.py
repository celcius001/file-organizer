import os
import shutil

path = input("Enter Path: ")
files = os.listdir(path)

for file in files:
    filename, exception = os.path.splitext(file)
    exception = exception[1:]

    if os.path.exists(path+"/"+exception):
        shutil.move(path+"/"+file, path+"/"+exception+"/"+file)
    else:
        os.makedirs(path+"/"+exception)
        shutil.move(path+"/"+file, path+"/"+exception+"/"+file)