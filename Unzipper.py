import os
import glob
import zipfile

allFiles = glob.glob(os.path.join(zipfilepath_, '*.zip'))

for file_ in allFiles:
	zip_ref = zipfile.ZipFile(file_)
	zip_ref.extractall(destination_path)
	zip_ref.close()
