#!/usr/bin/env python

import re
from ycm.completers.completer import Completer
from ycm.server import responses


RE_IMPORT = re.compile(r'^import')

class GhcmodCompleter( Completer ):
  """
  A Completer that uses ghc-mod to provide semantic completions for haskell
  """


  def __init__( self, user_options, project=None ):
    self.project = project
    super( GhcmodCompleter, self ).__init__( user_options )


  def SupportedFiletypes( self ):
    return [ 'haskell' ]


  def ShouldUseNowInner( self, request_data ):
    return False


  def ComputeCandidatesInner( self, request_data ):
    rv = [
      responses.BuildCompletionData('foo', '[Function]', 'Some class'),
      responses.BuildCompletionData('foofoo', '[Method]'),
      responses.BuildCompletionData('foobarfoo', '[Class]'),
    ]

    return rv

