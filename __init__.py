import sys
import signal
import pickle

try:
  assert sys.version_info.major == 3
except AssertionError:
  sys.exit('EXIT: i require python3')

# {{{
class ShellState:
  def __init__(self,statefile):
    self.statefile = statefile
    self.state = self.readstate()

    if self.state is None:
      self.log = {}
    else:
      self.log = self.state.log

  def readstate(self):
    try:
      pfile = open(self.statefile,'rb')
      state = pickle.load(pfile)
      pfile.close()
      return state
    except FileNotFoundError:
      return None

  def writestate(self,state):
    pfile = open(self.statefile,'wb')
    pickle.dump(state,pfile)
    pfile.close()

  def initialize(self):
    self.writestate({})

  def exit_handler(self,errormessage=None):
    print()
    if errormessage:
      print(errormessage)
    print("saving state...")
    self.writestate(self)
    print("exiting...")
    sys.exit(0)

  def signal_handler(self,signal,frame):
    self.exit_handler()
# }}}
