import os
import glob
import zipfile

allFiles = glob.glob(os.path.join(unzipper_source, '*.zip'))

for file_ in allFiles:
	zip_ref = zipfile.ZipFile(file_)
	zip_ref.extractall(unzipper_destination)
	zip_ref.close()
