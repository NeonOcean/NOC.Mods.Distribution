import os
import json
import typing

from Site_NeonOcean_NOC_Mods_Distribution import Paths
from Site_NeonOcean_NOC_Mods_Distribution.Tools import IO

def BuildPromotions () -> bool:
	IO.ClearDirectory(Paths.PromotionsBuildPath)

	_BuildPromotions()
	return True

def _BuildPromotions () -> None:
	promotionConfigs = list()  # type:  typing.List[typing.Dict[str, typing.Any]]

	for directoryRoot, directoryNames, fileNames in os.walk(Paths.PromotionsSourcesPath):  # type: str, typing.List[str], typing.List[str]
		for fileName in fileNames:  # type: str
			if os.path.splitext(fileName)[1] == ".json":
				promotionConfigFilePath = os.path.join(directoryRoot, fileName)  # type: str

				try:
					promotionConfig = _ReadPromotionConfig(promotionConfigFilePath)  # type: dict
				except Exception as e:
					raise Exception("Failed to read promotion config from '" + promotionConfigFilePath + "'.") from e

				promotionConfigs.append(promotionConfig)

	promotionsDirectory = os.path.join(Paths.PromotionsBuildPath, "promotions")  # type: str
	promotionsFilePath = os.path.join(promotionsDirectory, "promotions.json")  # type: str

	if not os.path.exists(promotionsDirectory):
		os.makedirs(promotionsDirectory)

	with open(promotionsFilePath, "w+") as promotionsFile:
		promotionsFile.write(json.JSONEncoder(indent = "\t").encode(promotionConfigs))

def _ReadPromotionConfig (promotionConfigFilePath: str) -> typing.Dict[str, typing.Any]:
	with open(promotionConfigFilePath) as promotionConfigFile:
		promotionConfig = json.JSONDecoder().decode(promotionConfigFile.read())  # type: dict

	return promotionConfig