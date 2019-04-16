import os
import tempfile
FILE_EXTENSION_LENGTH = 0

class FileVault(object):
  def __init__(self):
    pass

  def backup(self, source, target):
    with tempfile.NamedTemporaryFile(delete = False) as conversion:
      for line in open(str(source), "rb") :
        line = line.rstrip()
        conversion.write(line + "\n".encode())

    conversion.close()

    os.rename(str(source), str(f"{source}"[:-FILE_EXTENSION_LENGTH] + ".backup"))
    os.rename(conversion.name, f"{target}")