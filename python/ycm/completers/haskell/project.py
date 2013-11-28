import re
from ycm.completers.completer_utils import Which, RunCommand
from functools import partial
from itertools import takewhile


FUNCTION = re.compile( r'^([^\s]+)\s+::\s+(.+)$' )
TYPECLASS = re.compile( r'^class\s+(.+)$' )
TYPE = re.compile( r'^(data|type|newtype)\s+(.+)$' )
GHC_MOD_BIN = Which( 'ghc-mod' )

if not GHC_MOD_BIN:
  raise ImportError(
    "No ghc-mod executable found. Install it with 'cabal install ghc-mod'"
    )


class Project( object ):
  """
  Used by the haskell completer to query and update information about
  projects/modules
  """

  def __init__( self, command_runner=( lambda s, c: RunCommand( c ) ) ):
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
        if str(module).startswith(partial_name):
          if module.real_module:
            rv.append( module )
          Search( module.submodules, level + 1 )

    Search( self._installed_modules, 1 )

    return rv


  def _AddModule( self, name ):
    def Add( cache, name, parent ):
      splitted = name.split( '.', 1 )
      tail = None

      if len(splitted) == 2:
        head, tail = splitted
      else:
        head = splitted[0]

      if head not in cache:
        cache[head] = Module( head, parent, self._RunCommand )
      if tail:
        Add( cache[head].submodules, tail, cache[head] )
      if name == head:
        cache[head].real_module = True

    Add( self._installed_modules, name, None )


class Module( object ):
  """Encapsulates data collected from a haskell module"""

  def __init__( self, name, parent, command_runner ):
    self.name = name
    self.parent = parent
    self._RunCommand = command_runner
    self.real_module = False
    self.submodules = {}


  def __str__( self ):
    def Name( module ):
      rv = ''
      if module.parent:
        rv = Name( module.parent ) + '.'
      return rv + module.name

    return Name( self )


  def QuerySymbols( self, prefix ):
    output = self._RunCommand( [ 'ghc-mod', 'browse', '-d', str(self) ] )
    toSymbol = partial( map, lambda l: Symbol( l, self ) )
    matching = partial( filter, lambda x: x.name.startswith( prefix ) )
    noReturnCode = partial( takewhile, lambda x: isinstance( x, str ) )

    return matching( toSymbol( noReturnCode( output ) ) )



class Symbol(object):
  """Encapsulates a function, datatype or typeclass"""

  def __init__( self, raw, module ):
    self.module = module

    m = FUNCTION.match( raw )
    if m:
      self.type = 'function'
      self.name = m.group( 1 )
      self.signature = m.group( 2 )
      return

    m = TYPECLASS.match( raw )
    if m:
      self.type = 'class'
      self.name = m.group( 1 )
      return

    m = TYPE.match( raw )
    if m:
      self.type = 'type'
      self.kind = m.group( 1 )
      self.name = m.group( 2 )
      return

    raise Exception( 'Unrecognized symbol %s' % raw )


  def __str__( self ):
    if self.type == 'function':
      return '%s :: %s' % (self.name, self.signature,)
    elif self.type == 'class':
      return '%s (class)' % self.name
    elif self.type == 'type':
      return '%s (%s)' % (self.name, self.kind,)


