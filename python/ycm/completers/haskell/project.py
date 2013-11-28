from ycm.completers.completer_utils import Which, RunCommand


GHC_MOD_BIN = Which('ghc-mod')

if not GHC_MOD_BIN:
  raise ImportError(
    "No ghc-mod executable found. Install it with 'cabal install ghc-mod'"
    )


class Project( object ):
  """
  Used by the haskell completer to query and update information about
  projects/modules
  """

  def __init__( self, command_runner=None ):
    if command_runner:
      # abstract command runner function for easier testing of this class
      self._RunCommand = command_runner

    self.RefreshInstalledModules()


  def RefreshInstalledModules( self ):
    self._installed_modules = {}
    output = self._RunCommand( [ GHC_MOD_BIN, 'list' ] )

    for line in output:
      if not isinstance( line, ( str, ) ):
        break
      self._AddModule( line )

    if line != 0:
      raise Exception( 'Failed to get list of installed modules from ghc-mod' )


  def QueryModules( self, name ):
    parts = name.split( '.' )
    rv = []

    def Search( modules, level ):
      if level > len(parts):
        level = len(parts)

      partial_name = '.'.join(parts[:level])

      for module in modules.values():
        if module.FullyQualifiedName().startswith(partial_name):
          if module.real_module:
            rv.append( module )
          Search( module.submodules, level + 1 )

    Search( self._installed_modules, 1 )

    return sorted(rv, key=lambda m: m.FullyQualifiedName())


  def _RunCommand ( self, cmd ):
    return RunCommand( cmd )


  def _AddModule( self, name ):
    def Add( cache, name, parent ):
      splitted = name.split( '.', 1 )
      tail = None

      if len(splitted) == 2:
        head, tail = splitted
      else:
        head = splitted[0]

      if head not in cache:
        cache[head] = Module( head, parent )
      if tail:
        Add( cache[head].submodules, tail, cache[head] )
      if name == head:
        cache[head].real_module = True

    Add( self._installed_modules, name, None )


class Module( object ):
  """Encapsulates data collected from a haskell module"""

  def __init__( self, name, parent ):
    self.name = name
    self.parent = parent
    self.real_module = False
    self.submodules = {}
    self.symbols = {}


  def FullyQualifiedName( self ):
    def Name( module ):
      rv = ''
      if module.parent:
        rv = Name( module.parent ) + '.'
      return rv + module.name

    return Name( self )


class Symbol(object):
  """Encapsulates a function, datatype or typeclass"""

  def __init__( self, name, type ):
    self._name = name
    self._type = type
