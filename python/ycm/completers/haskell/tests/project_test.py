from nose.tools import eq_
from functools import partial
from ycm.completers.haskell.ghcmod import Project


class TestProject( object ):

  def setup( self ):
    self.project = Project( StubRunCommand )


  def QueryModules_test( self ):
    names = partial( map, str )
    f = lambda x: sorted( names( self.project.QueryModules ( x ) ) )

    eq_( [ 'Data.List', 'Data.List.Lazy', 'Data.Map', 'Prelude' ], f( '' ) )
    eq_( [ 'Data.List', 'Data.List.Lazy', 'Data.Map' ], f( 'D' ) )
    eq_( [ 'Data.List', 'Data.List.Lazy' ], f( 'Data.L' ) )
    eq_( [ 'Data.Map' ], f( 'Data.Map' ) )
    eq_( [ 'Prelude' ], f( 'P' ) )


  def QuerySymbols_test( self ):
    symbols = lambda x: lambda y: y.QuerySymbols( x )
    concat = partial( reduce, lambda x, y: x + y )
    names = partial( map, str )
    f = lambda x: sorted(
      names( concat( map(symbols(x), self.project.QueryModules( '' ) ) ) ) )

    eq_( [
      'Maybe a (data)',
      'Monad m (class)',
      'empty :: Map k a',
      'foldl :: (a -> b -> a) -> a -> [a] -> b',
      'insert :: Ord k => k -> a -> Map k a -> Map k a',
      'map :: (a -> b) -> [a] -> [b]',
    ], f( '' ) )

    eq_( [
      'Maybe a (data)',
      'Monad m (class)',
    ], f( 'M' ) )

    eq_( [
      'foldl :: (a -> b -> a) -> a -> [a] -> b',
    ], f( 'f' ) )



modules = [ 'Prelude', 'Data.Map', 'Data.List', 'Data.List.Lazy' ]
symbols = {
  'Prelude': [
    'map :: (a -> b) -> [a] -> [b]',
    'foldl :: (a -> b -> a) -> a -> [a] -> b',
    'class Monad m',
    'data Maybe a',
  ],
  'Data.Map': [
    'empty :: Map k a',
    'insert :: Ord k => k -> a -> Map k a -> Map k a',
  ],
  'Data.List': [],
  'Data.List.Lazy': [],
}


def StubRunCommand( cmd ):
  if cmd[1] == 'list':
    for item in modules:
      yield item
  elif cmd[1] == 'browse':
    for item in symbols[cmd[3]]:
      yield item
  yield 0
