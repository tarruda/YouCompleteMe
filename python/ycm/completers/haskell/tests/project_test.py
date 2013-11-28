from nose.tools import eq_
from functools import partial
from ycm.completers.haskell.project import Project
from pprint import pprint


class TestProject( object ):

  def setup( self ):
    self.project = Project( StubRunCommand )


  def QueryModules_test(self):
    names = partial( map, lambda m: m.FullyQualifiedName() )

    eq_( [ 'Data.List', 'Data.List.Lazy', 'Data.Map', 'Prelude' ],
        names( self.project.QueryModules( '' ) ) )
    eq_( [ 'Data.List', 'Data.List.Lazy', 'Data.Map' ],
        names( self.project.QueryModules( 'D' ) ) )
    eq_( [ 'Data.List', 'Data.List.Lazy' ],
        names( self.project.QueryModules( 'Data.L' ) ) )
    eq_( [ 'Data.Map' ],
        names( self.project.QueryModules( 'Data.Map' ) ) )
    eq_( [ 'Prelude' ],
        names( self.project.QueryModules( 'P' ) ) )


def StubRunCommand( cmd ):
  if cmd[1] == 'list':
    for item in [ 'Prelude', 'Data.Map', 'Data.List', 'Data.List.Lazy' ]:
      yield item

  yield 0
