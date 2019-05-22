import os
import typing
from importlib import util

from Site_NeonOcean_NOC_Mods_Distribution import Paths

class FormattingDict(dict):
	def __missing__ (self, key):
		return "{" + key + "}"

def BuildModIndex (modNamespace: str) -> str:
	automationModule = util.find_spec("Automation")

	if automationModule is None and not _showedWarning:
		print("Failed to build mod distribution index. Environment automation modules are not loaded.")

	from Automation import Distribution

	modVersions = Distribution.GetReleaseVersions(modNamespace)

	if modVersions is None:
		return ""

	modVersionsText = ""

	with open(os.path.join(Paths.TemplatesPath, "ModIndexVersion.html")) as versionTemplateFile:
		versionTemplate = versionTemplateFile.read()  # type: str

	for modVersion in modVersions:  # type: Distribution.ModVersion
		versionFormatting = FormattingDict()  # type: typing.Dict[str, typing.Any]

		versionFormatting["VersionNumber"] = modVersion.Version

		versionFormatting["InstallerLink"] = "mods/" + modNamespace + "/" + modVersion.Version + "/installer"
		versionFormatting["FilesLink"] =  "mods/" + modNamespace + "/" + modVersion.Version + "/files"
		versionFormatting["SourcesLink"] =  "mods/" + modNamespace + "/" + modVersion.Version + "/sources"


		versionFormatting["GameVersionNumber"] = modVersion.GameVersion
		versionFormatting["ReleaseDate"] = modVersion.ReleaseDateObject.strftime("%B %d, %Y")

		if modVersionsText == "":
			modVersionsText = versionTemplate.format_map(versionFormatting)
		else:
			modVersionsText += "\n" + versionTemplate.format_map(versionFormatting)

	return modVersionsText

_showedWarning = False  # type: bool
