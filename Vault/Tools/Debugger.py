class Log(object):
  def __init__(self):
    pass

  def create(self):
    directory = str(Log(self).windowsTEMP)
    file = "payload.log"
    script = directory + file

    script = open(script, "w+")
    script.write("Payload Debugging File")
    script.close()

  def write(self, context):
    directory = str(Log(self).windowsTEMP)
    file = "payload.log"
    script = directory + file

    script = open(script, "w")
    script.write(str(context))
    script.close()

  @property
  def windowsTEMP(self):
    directory = "C:\\Temp\\"
    return directory

  @property
  def linuxTEMP(self):
    directory = "/tmp/"
    return directory