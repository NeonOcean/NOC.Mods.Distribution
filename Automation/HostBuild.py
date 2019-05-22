import sys
import os
from importlib import util

from http import server
import socketserver

def CreateBuildServer (buildDirectory: str) -> server.SimpleHTTPRequestHandler:
	class BuildServer (server.SimpleHTTPRequestHandler):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs, directory = buildDirectory)
			
	return BuildServer

if __name__ == "__main__":
	sys.path.append(os.path.join(os.path.dirname(__file__), "NeonOcean.NOC.Main"))
	Paths = util.find_spec("Site_NeonOcean_NOC_Main.Paths").loader.load_module()
	
	port = 8000  # type: int
	
	with socketserver.ThreadingTCPServer(("", port), CreateBuildServer(Paths.BuildPath)) as buildServer:
		print("Starting server for the directory '" + Paths.BuildPath + "' on port " + str(port))
		buildServer.serve_forever()