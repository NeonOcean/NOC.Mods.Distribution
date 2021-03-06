import os
import typing
from distutils import dir_util
from importlib import util
from json import decoder

from Site_NeonOcean_NOC_Mods_Distribution import Paths
from Site_NeonOcean_NOC_Mods_Distribution.Tools import IO, Formatting

def BuildDocuments () -> bool:
	IO.ClearDirectory(Paths.DocumentsBuildPath)

	_BuildDocuments()
	return True

def _BuildDocuments () -> None:
	if os.path.exists(Paths.DocumentsSourcesIncludedPath):
		dir_util.copy_tree(Paths.DocumentsSourcesIncludedPath, Paths.DocumentsBuildPath)

	for directoryRoot, directoryNames, fileNames in os.walk(Paths.DocumentsConfigDocumentsPath):  # type: str, typing.List[str], typing.List[str]
		for fileName in fileNames:  # type: str
			if os.path.splitext(fileName)[1] == ".json":
				documentConfigFilePath = os.path.join(directoryRoot, fileName)  # type: str

				try:
					documentFilePath, documentText = _ReadDocumentConfig(documentConfigFilePath)  # type: str, str
				except Exception as e:
					raise Exception("Failed to read document config from '" + documentConfigFilePath + "'.") from e

				documentDirectoryPath = os.path.dirname(documentFilePath)  # type: str

				if not os.path.exists(documentDirectoryPath):
					os.makedirs(documentDirectoryPath)

				with open(documentFilePath, "w+") as documentFile:
					documentFile.write(documentText)

def _ReadDocumentConfig (documentConfigFilePath: str) -> typing.Tuple[str, str]:
	"""
	:return:
	Document build path,
	Document text,
	Indexing information
	"""

	with open(documentConfigFilePath) as documentConfigFile:
		documentConfig = decoder.JSONDecoder().decode(documentConfigFile.read())  # type: dict

	documentTemplateConfigFilePath = os.path.join(Paths.DocumentsConfigTemplatesPath, documentConfig["TemplateConfig"])  # type: str

	with open(documentTemplateConfigFilePath) as documentTemplateConfigFile:
		documentTemplateConfig = decoder.JSONDecoder().decode(documentTemplateConfigFile.read())  # type: dict

	documentFileExtension = documentConfig["FileExtension"]  # type: str

	documentRelativeFilePath = os.path.splitext(documentConfigFilePath.replace(Paths.DocumentsConfigDocumentsPath + os.path.sep, ""))[0] + "." + documentFileExtension  # type: str
	documentRelativeFilePath.replace(os.path.altsep, os.path.sep)

	documentFilePath = os.path.join(Paths.DocumentsBuildPath, documentRelativeFilePath)

	documentAdditionalValues = {
		"DocumentPath": documentRelativeFilePath
	}

	documentValues = _ReadValues(documentConfig, documentAdditionalValues)  # type: dict
	documentValues["DocumentPath"] = documentRelativeFilePath

	if documentValues.get("BasePath") is None:
		documentRelativeFilePathParts = documentRelativeFilePath.split(os.path.sep)  # type: typing.List[str]
		documentBasePath = "../" * (len(documentRelativeFilePathParts) - 1)

		documentValues["BasePath"] = documentBasePath

	documentText = _ReadDocument(documentValues, documentTemplateConfig["Document"])  # type: str

	return documentFilePath, documentText

def _ReadValues (configDictionary: dict, additionalValues: dict = None) -> dict:
	combinedDictionary = dict()  # type: dict

	configDictionaryValues = configDictionary.get("Values")  # type: dict

	if configDictionaryValues is not None:
		combinedDictionary.update(configDictionaryValues)

	configDictionarySources = configDictionary.get("Sources")  # type: dict

	if configDictionarySources is not None:
		for sourceKey, sourceFileName in configDictionarySources.items():
			sourceFilePath = os.path.join(Paths.DocumentsSourcesPath, sourceFileName)  # type: str
			sourceIncludedFilePath = os.path.join(Paths.DocumentsSourcesIncludedPath, sourceFileName)  # type: str

			if os.path.exists(sourceFilePath):
				with open(sourceFilePath) as sourceFile:
					configDictionarySources[sourceKey] = sourceFile.read()
			else:
				if os.path.exists(sourceIncludedFilePath):
					with open(sourceIncludedFilePath) as sourceIncludedFile:
						configDictionarySources[sourceKey] = sourceIncludedFile.read()
				else:
					raise Exception("Cannot find source file '" + sourceFileName + "'.")

		combinedDictionary.update(configDictionarySources)

	if additionalValues is not None:
		combinedDictionary.update(additionalValues)

	configDictionaryScripts = configDictionary.get("Scripts")  # type: dict

	if configDictionaryScripts is not None:
		for scriptKey, scriptDictionary in configDictionaryScripts.items():
			scriptModule = util.find_spec(scriptDictionary["Module"]).loader.load_module()

			scriptInputs = list()  # type: typing.List[typing.Any]

			for scriptInput in scriptDictionary["Inputs"]:
				scriptInputs.append(combinedDictionary[scriptInput])

			scriptOutput = getattr(scriptModule, scriptDictionary["Function"])(*scriptInputs)

			combinedDictionary[scriptKey] = scriptOutput

	return combinedDictionary

def _ReadDocument (documentValues: dict, documentDictionary: dict) -> str:
	templateFilePath = os.path.join(Paths.TemplatesPath, documentDictionary["Template"])  # type: str

	with open(templateFilePath) as templateFile:
		template = templateFile.read()  # type: str

	formattingDictionary = documentDictionary.get("Formatting")  # type: dict

	if formattingDictionary is None:
		documentText = template
	else:
		formattingDictionary = dict(formattingDictionary)  # type: typing.Dict[str, str]

		for formattingKey, formattingValue in formattingDictionary.items():  # type: str, object
			if isinstance(formattingValue, str):
				if formattingValue != "":
					formattingDictionary[formattingKey] = documentValues[formattingValue]
				else:
					formattingDictionary[formattingKey] = ""

			elif isinstance(formattingValue, list):
				formattingCombinedValue = ""  # type: str

				for formattingListValue in formattingValue:  # type: str
					if isinstance(formattingListValue, str):
						if formattingCombinedValue != "":
							formattingCombinedValue += "\n" + documentValues[formattingListValue]
						else:
							formattingCombinedValue = documentValues[formattingListValue]

					elif isinstance(formattingListValue, dict):
						if formattingCombinedValue != "":
							formattingCombinedValue += "\n\n" + _ReadDocument(documentValues, formattingListValue)
						else:
							formattingCombinedValue = _ReadDocument(documentValues, formattingListValue)

				formattingDictionary[formattingKey] = formattingCombinedValue

			elif isinstance(formattingValue, dict):
				formattingDictionary[formattingKey] = _ReadDocument(documentValues, formattingValue)

		documentText = Formatting.FormatDictionary(template, formattingDictionary)

	return documentText
