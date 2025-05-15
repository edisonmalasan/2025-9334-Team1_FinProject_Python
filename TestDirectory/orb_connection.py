import sys

from WhatsTheWord.referenceClasses import Player
from omniORB import CORBA, PortableServer
import CosNaming, WhatsTheWord

class ORBConnector():
    def __init__(self):
        self.orb = CORBA.ORB_init(["-ORBInitRef", "NameService=corbaloc:iiop:localhost:10050/NameService"], CORBA.ORB_ID)

        # Obtain a reference to the root naming context
        self.obj = self.orb.resolve_initial_references("NameService")
        self.ncRef = self.obj._narrow(CosNaming.NamingContextExt)

        self.obj_poa = self.orb.resolve_initial_references("RootPOA")
        self.rootpoa = self.obj_poa._narrow(PortableServer.POA)
        self.rootpoa._get_the_POAManager().activate()

        if self.ncRef is None:
            print("Failed to narrow the root naming context")
            sys.exit(1)

        # Resolve the name "test.my_context/ExampleEcho.Object"
        self.gameName = [CosNaming.NameComponent("Game", ""), ]

        try:
            self.obj = self.ncRef.resolve(self.gameName)
        except CosNaming.NamingContext.NotFound as ex:
            print("Game Name not found")
            sys.exit(1)

        # Narrow the object to an Example::Echo
        self.game = self.obj._narrow(WhatsTheWord.game_logic.Game)

        self.playerServiceName = [CosNaming.NameComponent("PlayerService", ""), ]

        try:
            self.obj = self.ncRef.resolve(self.playerServiceName)
        except CosNaming.NamingContext.NotFound as ex:
            print("PlayerService Name not found")
            sys.exit(1)

        self.playerService = self.obj._narrow(WhatsTheWord.client.player.PlayerService)

        if self.game is None:
            print("Object reference is not an WhatsTheWord::Game")
            sys.exit(1)

        if self.playerService is None:
            print("Object reference is not an WhatsTheWord::PlayerService")
            sys.exit(1)

    def getORB(self):
        return self.orb

    def getPlayerService(self):
        return self.playerService

    def getGame(self):
        return self.game

    def close(self):
        self.orb.destroy()