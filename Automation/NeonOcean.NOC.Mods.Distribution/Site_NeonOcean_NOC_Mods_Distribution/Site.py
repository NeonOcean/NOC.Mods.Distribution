import os
import typing
from json import decoder

from Site_NeonOcean_NOC_Mods_Distribution import Paths

_site = None  # type: Site
_siteData = None  # type: typing.Dict[str, typing.Any]

class Site:
	def __init__ (self, informationDictionary: typing.Dict[str, typing.Any]):
		self.Namespace = informationDictionary["Namespace"]  # type: str
		self.Domain = informationDictionary["Domain"]  # type: str

		self.GithubName = informationDictionary["Github Name"]  # type: str

def GetCurrentSite () -> Site:
	return _site

def GetSiteData () -> typing.Dict[str, typing.Any]:
	return _siteData

def _Setup () -> None:
	global _site, _siteData

	informationFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.normpath(__file__))), "Site.json")  # type: str

	try:
		with open(os.path.join(informationFilePath)) as informationFile:
			_site = Site(decoder.JSONDecoder().decode(informationFile.read()))
	except Exception as e:
		raise Exception("Failed to read site information for '" + informationFilePath + "'. \n") from e

	_siteData = {
		"Namespace": GetCurrentSite().Namespace,
		"Domain": GetCurrentSite().Domain,

		"GithubName": GetCurrentSite().GithubName,

		"BuildPath": Paths.BuildPath,
		"HostingPath": Paths.BuildPath
	}

_Setup()
