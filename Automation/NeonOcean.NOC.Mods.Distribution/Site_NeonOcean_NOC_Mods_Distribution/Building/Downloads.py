import os
import typing
from importlib import util
from json import decoder

from Site_NeonOcean_NOC_Mods_Distribution import Paths
from Site_NeonOcean_NOC_Mods_Distribution.Tools import IO

def BuildDownloads () -> bool:
	automationModule = util.find_spec("Automation")

	if automationModule is None and not _showedWarning:
		print("Failed to build mod distribution index. Environment automation modules are not loaded.")

	IO.ClearDirectory(Paths.DownloadsBuildPath)

	_BuildModDownloads()

	return True

def _BuildModDownloads () -> None:
	from Automation import Distribution

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
		modBuildPath = os.path.join(Paths.DownloadsBuildPath, "Mods", modNamespace)  # type: str

		licensePath = os.path.join(modBuildPath.replace(Paths.DownloadsBuildPath + os.path.sep, ""), _licenseName).replace("\\", "/")  # type: str
		licensePath = licensePath.replace("\\", "/")

		with open(os.path.join(Paths.DownloadsSourcesPath, "Mods", modNamespace + ".json")) as modInformationFile:
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

		modLatestVersion = Distribution.GetReleaseLatest(modNamespace)  # type: Distribution.ModVersion

		latestBasePath = os.path.relpath(Paths.DownloadsBuildPath, modBuildPath).replace("\\", "/")  # type: str
		latestInstallerPath = os.path.join(modBuildPath, "installer.html")  # type: str
		latestInstallerFilePath = os.path.join(_releasesURL, modLatestVersion.InstallerFilePath).replace("\\", "/")  # type: str
		latestFilesPath = os.path.join(modBuildPath, "files.html")  # type: str
		latestFilesRelativePath = os.path.relpath(latestFilesPath, Paths.DownloadsBuildPath)  # type: str
		latestFilesFilePath = os.path.join(_releasesURL, modLatestVersion.SourcesFilePath).replace("\\", "/")  # type: str
		latestSourcesPath = os.path.join(modBuildPath, "sources.html")  # type: str
		latestSourcesFilePath = os.path.join(_releasesURL, modLatestVersion.SourcesFilePath).replace("\\", "/")  # type: str

		_WriteDownload(latestInstallerPath, modInstallerTemplate, latestBasePath,
					   modNamespace, modLatestVersion.Version, _typeInstaller, modLatestVersion.GameVersion, modLatestVersion.ReleaseDate,
					   latestFilesRelativePath, licensePath, latestInstallerFilePath)

		_WriteDownload(latestFilesPath, modFilesTemplate, latestBasePath,
					   modNamespace, modLatestVersion.Version, _typeFiles, modLatestVersion.GameVersion, modLatestVersion.ReleaseDate,
					   latestFilesRelativePath, licensePath, latestFilesFilePath)


		_WriteDownload(latestSourcesPath, sourcesTemplate, latestBasePath,
					   modNamespace, modLatestVersion.Version, _typeSources, modLatestVersion.GameVersion, modLatestVersion.ReleaseDate,
					   latestFilesRelativePath, licensePath, latestSourcesFilePath)

		for modVersion in modVersions:  # type: Distribution.ModVersion
			versionBuildPath = os.path.join(modBuildPath, modVersion.Version)

			basePath = os.path.relpath(Paths.DownloadsBuildPath, versionBuildPath).replace("\\", "/")  # type: str
			installerPath = os.path.join(versionBuildPath, "installer.html")  # type: str
			installerFilePath = os.path.join(_releasesURL, modVersion.InstallerFilePath).replace("\\", "/")  # type: str
			filesPath = os.path.join(versionBuildPath, "files.html")  # type: str
			filesRelativePath = os.path.relpath(filesPath, Paths.DownloadsBuildPath)  # type: str
			filesFilePath =  os.path.join(_releasesURL, modVersion.FilesFilePath).replace("\\", "/")  # type: str
			sourcesPath = os.path.join(versionBuildPath, "sources.html")  # type: str
			sourcesFilePath = os.path.join(_releasesURL, modVersion.SourcesFilePath).replace("\\", "/")  # type: str

			_WriteDownload(installerPath, modInstallerTemplate, basePath,
						   modNamespace, modVersion.Version, _typeInstaller, modLatestVersion.GameVersion, modLatestVersion.ReleaseDate,
						   filesRelativePath, licensePath, installerFilePath)


			_WriteDownload(filesPath, modFilesTemplate, basePath,
						   modNamespace, modVersion.Version, _typeFiles, modVersion.GameVersion, modVersion.ReleaseDate,
						   filesRelativePath, licensePath, filesFilePath)


			_WriteDownload(sourcesPath, sourcesTemplate, basePath,
						   modNamespace, modVersion.Version, _typeSources, modVersion.GameVersion, modVersion.ReleaseDate,
						   filesRelativePath, licensePath, sourcesFilePath)

	for modNamespace, modVersions in Distribution.Previews.items():  # type: str, typing.List[Distribution.ModVersion]
		modBuildPath = os.path.join(Paths.DownloadsBuildPath, "Mods", modNamespace)  # type: str

		licensePath = os.path.join(modBuildPath.replace(Paths.DownloadsBuildPath + os.path.sep, ""), _licenseName).replace("\\", "/")  # type: str
		licensePath = licensePath.replace("\\", "/")

		with open(os.path.join(Paths.DownloadsSourcesPath, "Mods", modNamespace + ".json")) as modInformationFile:
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

		for modVersion in modVersions:  # type: Distribution.ModVersion
			versionBuildPath = os.path.join(modBuildPath, modVersion.Version, modVersion.ConcealerFolderName)

			basePath = os.path.relpath(Paths.DownloadsBuildPath, versionBuildPath).replace("\\", "/")  # type: str
			installerPath = os.path.join(versionBuildPath, "installer.html")  # type: str
			installerFilePath = os.path.join(_previewsURL, modVersion.InstallerFilePath).replace("\\", "/")  # type: str
			filesPath = os.path.join(versionBuildPath, "files.html")  # type: str
			filesRelativePath = os.path.relpath(filesPath, Paths.DownloadsBuildPath)  # type: str
			filesFilePath = os.path.join(_previewsURL, modVersion.FilesFilePath).replace("\\", "/")  # type: str
			sourcesPath = os.path.join(versionBuildPath, "sources.html")  # type: str
			sourcesFilePath = os.path.join(_previewsURL, modVersion.SourcesFilePath).replace("\\", "/")  # type: str

			_WriteDownload(installerPath, modInstallerTemplate, basePath,
						   modNamespace, modVersion.Version, _typeFiles, modVersion.GameVersion, modVersion.ReleaseDate,
						   filesRelativePath, licensePath, installerFilePath)


			_WriteDownload(filesPath, modFilesTemplate, basePath,
						   modNamespace, modVersion.Version, _typeFiles, modVersion.GameVersion, modVersion.ReleaseDate,
						   filesRelativePath, licensePath, filesFilePath)


			_WriteDownload(sourcesPath, sourcesTemplate, basePath,
						   modNamespace, modVersion.Version, _typeSources, modVersion.GameVersion, modVersion.ReleaseDate,
						   filesRelativePath, licensePath, sourcesFilePath)

def _WriteDownload (writeFilePath: str, template: str, basePath: str,
					Name: str, Version: str, Type: str, gameVersion: str, releaseDate: str,
					filesPath: str, licensePath: str, fileURL: str) -> None:
	if not os.path.exists(os.path.dirname(writeFilePath)):
		os.makedirs(os.path.dirname(writeFilePath))

	with open(writeFilePath, "w+") as writeFile:
		writeFile.write(template.format_map({
			"Base Path": basePath,
			"Name": Name,
			"Version": Version,
			"File Name": os.path.split(fileURL)[1],
			"Type": Type,
			"Game Version": gameVersion,
			"Release Date": releaseDate,
			"Files Path": filesPath,
			"License Path": licensePath,
			"File URL": fileURL
		}))

_showedWarning = False  # type: bool

# noinspection SpellCheckingInspection
_releasesURL = "https://releases.mods.neonoceancreations.com"  # type: str
# noinspection SpellCheckingInspection
_previewsURL = "https://previews.mods.neonoceancreations.com"  # type: str

_typeInstaller = "Installer"  # type: str
_typeFiles = "Files"  # type: str
_typeSources = "Sources"  # type: str

_licenseName = "license.html"  # type: str
