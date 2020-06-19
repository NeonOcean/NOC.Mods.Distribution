import typing
from importlib import util
from json import encoder

from Site_NeonOcean_NOC_Mods_Distribution import Mods

_showedWarning = False  # type: bool

def GetLatestText () -> str:
	automationModule = util.find_spec("Automation")

	if automationModule is None and not _showedWarning:
		print("Failed to build mod distribution index. Environment automation modules are not loaded.")
		return ""

	from Automation import Distribution

	latestDictionary = dict()  # type: typing.Dict[str, typing.Dict[str, str]]

	for releaseNamespace in Distribution.Releases.keys():
		latestReleaseVersion = GetLatestReleaseVersion(releaseNamespace)  # type: str

		releaseNamespaceDictionary = latestDictionary.get(releaseNamespace)  # type: typing.Dict[str, str]

		if releaseNamespaceDictionary is None:
			releaseNamespaceDictionary = dict()
			latestDictionary[releaseNamespace] = releaseNamespaceDictionary

		releaseNamespaceDictionary["Release"] = latestReleaseVersion

		try:
			releasedMod = Mods.GetModConfig(releaseNamespace)
		except:
			continue

		for releaseLegacyNamespace in releasedMod.LegacyNamespaces:  # type: str
			releaseLegacyNamespaceDictionary = latestDictionary.get(releaseLegacyNamespace)  # type: typing.Dict[str, str]

			if releaseLegacyNamespaceDictionary is None:
				releaseLegacyNamespaceDictionary = dict()
				latestDictionary[releaseLegacyNamespace] = releaseLegacyNamespaceDictionary

			releaseLegacyNamespaceDictionary["Release"] = latestReleaseVersion

	for previewNamespace in Distribution.Previews.keys():
		latestPreviewVersion = GetLatestPreviewVersion(previewNamespace)  # type: str

		previewNamespaceDictionary = latestDictionary.get(previewNamespace)  # type: typing.Dict[str, str]

		if previewNamespaceDictionary is None:
			previewNamespaceDictionary = dict()
			latestDictionary[previewNamespace] = previewNamespaceDictionary

		previewNamespaceDictionary["Preview"] = latestPreviewVersion

		try:
			previewedMod = Mods.GetModConfig(previewNamespace)
		except:
			continue

		for previewLegacyNamespace in previewedMod.LegacyNamespaces:  # type: str
			previewLegacyNamespaceDictionary = latestDictionary.get(previewLegacyNamespace)  # type: typing.Dict[str, str]

			if previewLegacyNamespaceDictionary is None:
				previewLegacyNamespaceDictionary = dict()
				latestDictionary[previewLegacyNamespace] = previewLegacyNamespaceDictionary

			previewLegacyNamespaceDictionary["Preview"] = latestPreviewVersion

	return encoder.JSONEncoder(indent = "\t").encode(latestDictionary)

def GetLatestRelease (namespace: str) -> typing.Optional[typing.Any]:
	automationModule = util.find_spec("Automation")

	if automationModule is None and not _showedWarning:
		print("Failed to build mod distribution index. Environment automation modules are not loaded.")
		return None

	from Automation import Distribution

	return Distribution.GetReleaseLatest(namespace)

def GetLatestPreview (namespace: str) -> typing.Optional[typing.Any]:
	automationModule = util.find_spec("Automation")

	if automationModule is None and not _showedWarning:
		print("Failed to build mod distribution index. Environment automation modules are not loaded.")
		return None

	from Automation import Distribution

	return Distribution.GetPreviewLatest(namespace)

def GetLatestReleaseVersion (namespace: str) -> str:
	latestVersion = GetLatestRelease(namespace)

	if latestVersion is None:
		return ""

	return latestVersion.Version

def GetLatestPreviewVersion (namespace: str) -> str:
	latestVersion = GetLatestPreview(namespace)

	if latestVersion is None:
		return ""

	return latestVersion.Version
