from scenes import *

class Game:
    _ShouldExit: bool = False
    _CurrentScene: Scene = None
    _NextScene: Scene = None

    def __init__( self ):
        pass

    def Update( self ):
        if ( self._NextScene ):
            self._CurrentScene = self._NextScene
            self._NextScene = None
            self._CurrentScene.Start( self )

        self._CurrentScene.Update( self )

    def SetScene( self, scene: Scene ):
        self._NextScene = scene

    def ShouldExit( self ) -> bool:
        return self._ShouldExit

    def Exit( self ):
        self._ShouldExit = True

