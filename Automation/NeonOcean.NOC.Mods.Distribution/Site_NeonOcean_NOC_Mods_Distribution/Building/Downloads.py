import os
import typing
from importlib import util
from json import decoder

from Site_NeonOcean_NOC_Mods_Distribution import Paths
from Site_NeonOcean_NOC_Mods_Distribution.Tools import IO, Formatting

def BuildDownloads () -> bool:
	automationModule = util.find_spec("Automation")

	if automationModule is None and not _showedWarning:
		print("Failed to build mod distribution index. Environment automation modules are not loaded.")

	IO.ClearDirectory(Paths.DownloadsBuildPath)

	_BuildModDownloads()

	return True

def _BuildModDownloads () -> None:
	from Automation import Distribution, Mods

	with open(os.path.join(Paths.TemplatesPath, "DownloadInstaller.html")) as downloadTemplateFile:
		downloadInstallerTemplate = downloadTemplateFile.read()

	with open(os.path.join(Paths.TemplatesPath, "DownloadInstallerAge.html")) as downloadTemplateFile:
		downloadInstallerAgeTemplate = downloadTemplateFile.read()

	with open(os.path.join(Paths.TemplatesPath, "DownloadFiles.html")) as downloadTemplateFile:
		downloadFilesTemplate = downloadTemplateFile.read()

	with open(os.path.join(Paths.TemplatesPath, "DownloadFilesAge.html")) as downloadTemplateFile:
		downloadFilesAgeTemplate = downloadTemplateFile.read()

	with open(os.path.join(Paths.TemplatesPath, "DownloadSources.html")) as downloadTemplateFile:
		downloadSourcesTemplate = downloadTemplateFile.read()

	with open(os.path.join(Paths.TemplatesPath, "DownloadSourcesAge.html")) as downloadTemplateFile:
		downloadSourcesAgeTemplate = downloadTemplateFile.read()

	for modNamespace, modVersions in Distribution.Releases.items():  # type: str, typing.List[Distribution.ModVersion]
		modBuildPath = os.path.join(Paths.DownloadsBuildPath, "mods", modNamespace.lower())  # type: str

		licensePath = os.path.join(modBuildPath.replace(Paths.DownloadsBuildPath + os.path.sep, ""), _licenseName)  # type: str
		licensePath = licensePath.replace("\\", "/")

		with open(os.path.join(Paths.DownloadsSourcesPath, "mods", modNamespace + ".json")) as modInformationFile:
			modInformation = decoder.JSONDecoder().decode(modInformationFile.read())  # type: dict

		if not modInformation["Mod"]["Age"]:
			modInstallerTemplate = downloadInstallerTemplate  # type: str
			modFilesTemplate = downloadFilesTemplate  # type: str
		else:
			modInstallerTemplate = downloadInstallerAgeTemplate  # type: str
			modFilesTemplate = downloadFilesAgeTemplate  # type: str

		if not modInformation["Sources"]["Age"]:
			sourcesTemplate = downloadSourcesTemplate  # type: str
		else:
			sourcesTemplate = downloadSourcesAgeTemplate  # type: str

		mod = Mods.GetMod(modNamespace)  # type: Mods.Mod
		modLatestVersion = mod.ReleaseLatest  # type: Distribution.ModVersion

		modName = mod.GetName()  # type: typing.Optional[str]

		if modName is None:
			modName = modNamespace

		latestBasePath = os.path.relpath(Paths.DownloadsBuildPath, modBuildPath).replace("\\", "/") + "/.."  # type: str
		latestInstallerPath = os.path.join(modBuildPath, "installer/index.html")  # type: str
		latestInstallerURL = modLatestVersion.InstallerURL  # type: str
		latestFilesPath = os.path.join(modBuildPath, "files/index.html")  # type: str
		latestFilesRelativePath = os.path.relpath(latestFilesPath, Paths.DownloadsBuildPath)  # type: str
		latestFilesURL = modLatestVersion.FilesURL # type: str
		latestSourcesPath = os.path.join(modBuildPath, "sources/index.html")  # type: str
		latestSourcesURL = modLatestVersion.SourcesURL  # type: str

		_WriteDownload(latestInstallerPath, modInstallerTemplate, latestBasePath,
					   modName, str(modLatestVersion.Version), _typeInstaller, str(modLatestVersion.GameVersion), modLatestVersion.ReleaseDate,
					   latestFilesRelativePath, licensePath, latestInstallerURL)

		_WriteDownload(latestFilesPath, modFilesTemplate, latestBasePath,
					   modName, str(modLatestVersion.Version), _typeFiles, str(modLatestVersion.GameVersion), modLatestVersion.ReleaseDate,
					   latestFilesRelativePath, licensePath, latestFilesURL)


		_WriteDownload(latestSourcesPath, sourcesTemplate, latestBasePath,
					   modName, str(modLatestVersion.Version), _typeSources, str(modLatestVersion.GameVersion), modLatestVersion.ReleaseDate,
					   latestFilesRelativePath, licensePath, latestSourcesURL)

		for modVersion in modVersions:  # type: Distribution.ModVersion
			versionBuildPath = os.path.join(modBuildPath, str(modVersion.Version))

			basePath = os.path.relpath(Paths.DownloadsBuildPath, versionBuildPath).replace("\\", "/") + "/.."  # type: str
			installerPath = os.path.join(versionBuildPath, "installer/index.html")  # type: str
			installerURL = modVersion.InstallerURL  # type: str
			filesPath = os.path.join(versionBuildPath, "files/index.html")  # type: str
			filesRelativePath = os.path.relpath(filesPath, Paths.DownloadsBuildPath)  # type: str
			filesURL = modVersion.FilesURL  # type: str
			sourcesPath = os.path.join(versionBuildPath, "sources/index.html")  # type: str
			sourcesURL = modVersion.SourcesURL  # type: str

			_WriteDownload(installerPath, modInstallerTemplate, basePath,
						   modName, str(modVersion.Version), _typeInstaller, str(modLatestVersion.GameVersion), modLatestVersion.ReleaseDate,
						   filesRelativePath, licensePath, installerURL)


			_WriteDownload(filesPath, modFilesTemplate, basePath,
						   modName, str(modVersion.Version), _typeFiles, str(modVersion.GameVersion), modVersion.ReleaseDate,
						   filesRelativePath, licensePath, filesURL)


			_WriteDownload(sourcesPath, sourcesTemplate, basePath,
						   modName, str(modVersion.Version), _typeSources, str(modVersion.GameVersion), modVersion.ReleaseDate,
						   filesRelativePath, licensePath, sourcesURL)

	for modNamespace, modVersions in Distribution.Previews.items():  # type: str, typing.List[Distribution.ModVersion]
		modBuildPath = os.path.join(Paths.DownloadsBuildPath, "Mods", modNamespace)  # type: str

		licensePath = os.path.join(modBuildPath.replace(Paths.DownloadsBuildPath + os.path.sep, ""), _licenseName)  # type: str
		licensePath = licensePath.replace("\\", "/")

		with open(os.path.join(Paths.DownloadsSourcesPath, "mods", modNamespace + ".json")) as modInformationFile:
			modInformation = decoder.JSONDecoder().decode(modInformationFile.read())  # type: dict

		if not modInformation["Mod"]["Age"]:
			modInstallerTemplate = downloadInstallerTemplate  # type: str
			modFilesTemplate = downloadFilesTemplate  # type: str
		else:
			modInstallerTemplate = downloadInstallerAgeTemplate  # type: str
			modFilesTemplate = downloadFilesAgeTemplate  # type: str

		if not modInformation["Sources"]["Age"]:
			sourcesTemplate = downloadSourcesTemplate  # type: str
		else:
			sourcesTemplate = downloadSourcesAgeTemplate  # type: str

		mod = Mods.GetMod(modNamespace)  # type: Mods.Mod
		modName = mod.GetName()  # type: typing.Optional[str]

		for modVersion in modVersions:  # type: Distribution.ModVersion
			versionBuildPath = os.path.join(modBuildPath, str(modVersion.Version), modVersion.ConcealerFolderName)

			basePath = os.path.relpath(Paths.DownloadsBuildPath, versionBuildPath).replace("\\", "/") + "/.."  # type: str
			installerPath = os.path.join(versionBuildPath, "installer/index.html")  # type: str
			installerURL = modVersion.InstallerURL  # type: str
			filesPath = os.path.join(versionBuildPath, "files/index.html")  # type: str
			filesRelativePath = os.path.relpath(filesPath, Paths.DownloadsBuildPath)  # type: str
			filesURL = modVersion.FilesURL  # type: str
			sourcesPath = os.path.join(versionBuildPath, "sources/index.html")  # type: str
			sourcesURL = modVersion.SourcesURL  # type: str

			_WriteDownload(installerPath, modInstallerTemplate, basePath,
						   modName, str(modVersion.Version), _typeFiles, str(modVersion.GameVersion), modVersion.ReleaseDate,
						   filesRelativePath, licensePath, installerURL)


			_WriteDownload(filesPath, modFilesTemplate, basePath,
						   modName, str(modVersion.Version), _typeFiles, str(modVersion.GameVersion), modVersion.ReleaseDate,
						   filesRelativePath, licensePath, filesURL)


			_WriteDownload(sourcesPath, sourcesTemplate, basePath,
						   modName, str(modVersion.Version), _typeSources, str(modVersion.GameVersion), modVersion.ReleaseDate,
						   filesRelativePath, licensePath, sourcesURL)

def _WriteDownload (writeFilePath: str, template: str, basePath: str,
					name: str, version: str, downloadType: str, gameVersion: str, releaseDate: str,
					filesPath: str, licensePath: str, fileURL: str) -> None:
	if not os.path.exists(os.path.dirname(writeFilePath)):
		os.makedirs(os.path.dirname(writeFilePath))

	with open(writeFilePath, "w+") as writeFile:
		writeFile.write(Formatting.FormatDictionary(template, {
			"BasePath": basePath,
			"Name": name,
			"Version": version,
			"FileName": os.path.split(fileURL)[1],
			"Type": downloadType,
			"GameVersion": gameVersion,
			"ReleaseDate": releaseDate,
			"FilesPath": filesPath,
			"LicensePath": licensePath,
			"FileURL": fileURL
		}))

_showedWarning = False  # type: bool

_typeInstaller = "Installer"  # type: str
_typeFiles = "Files"  # type: str
_typeSources = "Sources"  # type: str

_licenseName = "license.html"  # type: str
