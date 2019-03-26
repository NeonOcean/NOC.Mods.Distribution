import sys
import typing

from Site_NeonOcean_NOC_Mods_Distribution import Site
from Site_NeonOcean_NOC_Mods_Distribution.Building import Documents, Downloads, Merging, Promotions
from Site_NeonOcean_NOC_Mods_Distribution.Tools import Exceptions

def BuildSite () -> bool:
	print("Building Website '" + Site.GetCurrentSite().Namespace + "'.")

	sitePhases = _siteBuildPhases  # type: typing.List[typing.Callable]

	for phase in sitePhases:  # type: typing.Callable
		try:
			if not phase():
				print("Forced to skip all or part of phase '" + phase.__name__ + "'.\n" + \
					  "Phase: '" + phase.__name__ + "' Site: '" + Site.GetCurrentSite().Namespace + "'", file = sys.stderr)
		except Exception as e:
			print("Failed to complete site build phase.\n" + \
				  "Phase: '" + phase.__name__ + "' Site: '" + Site.GetCurrentSite().Namespace + "'\n" + \
				  Exceptions.FormatException(e), file = sys.stderr)

			return False

	try:
		Merging.Merge()
	except Exception as e:
		print("Failed to merge site components.\n" + \
			  "Site: '" + Site.GetCurrentSite().Namespace + "' \n" + \
			  Exceptions.FormatException(e), file = sys.stderr)

		return False

	return True

def BuildPublishing () -> None:
	pass

_siteBuildPhases = [
	Documents.BuildDocuments,
	Downloads.BuildDownloads,
	Promotions.BuildPromotions
]