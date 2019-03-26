import glob
import os
import shutil
import typing
import zipfile

def ZipDirectory (rootDirectoryPath: str, destinationFilePath: str) -> None:
	if not os.path.exists(os.path.dirname(destinationFilePath)):
		os.makedirs(os.path.dirname(destinationFilePath))

	archive = zipfile.ZipFile(destinationFilePath, "w")  # type: zipfile.ZipFile

	for directoryRoot, directoryNames, fileNames in os.walk(rootDirectoryPath):  # type: str, typing.List[str], typing.List[str]
		if directoryRoot != rootDirectoryPath:
			archive.write(directoryRoot, arcname = directoryRoot.replace(rootDirectoryPath + os.path.sep, ""))

		for i in fileNames:
			path = os.path.join(directoryRoot, i)  # type: str
			archive.write(path, arcname = path.replace(rootDirectoryPath + os.path.sep, ""))

	archive.close()

def ClearDirectory (directoryPath: str) -> None:
	if not os.path.exists(directoryPath):
		return

	files = glob.glob(directoryPath + os.path.sep + "*")

	for previousBuildFile in files:  # type: str
		if os.path.isdir(previousBuildFile):
			shutil.rmtree(previousBuildFile)
		else:
			os.remove(previousBuildFile)
