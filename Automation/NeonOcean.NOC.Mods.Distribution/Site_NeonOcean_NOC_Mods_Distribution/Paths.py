import os

AutomationPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.normpath(__file__))))  # type: str
RootPath = os.path.dirname(AutomationPath)  # type: str

BuildPath = os.path.join(RootPath, "Build")  # type: str

DocumentsPath = os.path.join(RootPath, "Documents")  # type: str
DocumentsBuildPath = os.path.join(DocumentsPath, "Build")  # type: str
DocumentsConfigPath = os.path.join(DocumentsPath, "Config")  # type: str
DocumentsConfigDocumentsPath = os.path.join(DocumentsConfigPath, "Documents")  # type: str
DocumentsConfigTemplatesPath = os.path.join(DocumentsConfigPath, "Templates")  # type: str
DocumentsSourcesPath = os.path.join(DocumentsPath, "Sources")  # type: str
DocumentsSourcesIncludedPath = os.path.join(DocumentsPath, "Sources Included")  # type: str

DownloadsPath = os.path.join(RootPath, "Downloads")  # type: str
DownloadsBuildPath = os.path.join(DownloadsPath, "Build")  # type: str
DownloadsSourcesPath = os.path.join(DownloadsPath, "Downloads")  # type: str

PromotionsPath = os.path.join(RootPath, "Promotions")  # type: str
PromotionsBuildPath = os.path.join(PromotionsPath, "Build")  # type: str
PromotionsSourcesPath = os.path.join(PromotionsPath, "Promotions")  # type: str

ModsPath = os.path.join(RootPath, "Mods")  # type: str

TemplatesPath = os.path.join(RootPath, "Templates")  # type: str

LoosePath = os.path.join(RootPath, "Loose")  # type: str