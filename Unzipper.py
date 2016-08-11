import os
import glob
import zipfile

allFiles = glob.glob(os.path.join(zipfilePath_, '*.zip'))

for file_ in allFiles:
	zip_ref = zipfile.ZipFile(file_)
	zip_ref.extractall(destinationfile_path)
	zip_ref.close()
