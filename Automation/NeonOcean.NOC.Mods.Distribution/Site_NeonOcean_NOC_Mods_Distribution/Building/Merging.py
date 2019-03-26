import os
from distutils import dir_util

from Site_NeonOcean_NOC_Mods_Distribution import Paths
from Site_NeonOcean_NOC_Mods_Distribution.Tools import IO

def Merge () -> None:
	IO.ClearDirectory(Paths.BuildPath)

	_MergeLoose()
	_MergeDocuments()
	_MergeDownloads()
	_MergePromotions()

def _MergeLoose () -> None:
	if os.path.exists(Paths.LoosePath):
		dir_util.copy_tree(Paths.LoosePath, Paths.BuildPath)

def _MergeDocuments () -> None:
	if os.path.exists(Paths.DocumentsBuildPath):
		dir_util.copy_tree(Paths.DocumentsBuildPath, Paths.BuildPath)

def _MergeDownloads () -> None:
	if os.path.exists(Paths.DownloadsBuildPath):
		dir_util.copy_tree(Paths.DownloadsBuildPath, Paths.BuildPath)

def _MergePromotions () -> None:
	if os.path.exists(Paths.PromotionsBuildPath):
		dir_util.copy_tree(Paths.PromotionsBuildPath, Paths.BuildPath)