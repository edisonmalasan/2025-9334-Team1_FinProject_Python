#!/usr/bin/env python
import sys
from omniORB import CORBA, PortableServer
import CosNaming, WhatsTheWord, WhatsTheWord__POA
# Define an implementation of the Echo interface
class Game_i (WhatsTheWord__POA.game_logic.Game):
    def sendLetter(self, letter):
        print("Letter sent: ", letter)

    def endLobby(self):
        print()

    def sendTime(self, player):
        print()


# Initialise the ORB and find the root POA
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")

# Create an instance of Echo_i and an Echo object reference
ei = Game_i()
eo = ei._this()

# Obtain a reference to the root naming context
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContextExt)
if rootContext is None:
    print("Failed to narrow the root naming context")
    sys.exit(1)

# # Bind a context named "test.my_context" to the root context
# name = [CosNaming.NameComponent("test", "my_context")]
# try:
#     testContext = rootContext.bind_new_context(name)
#     print("New test context bound")
#
# except CosNaming.NamingContext.AlreadyBound as ex:
#     print("Test context already exists")
#     obj = rootContext.resolve(name)
#     testContext = obj._narrow(CosNaming.NamingContext)
#     if testContext is None:
#         print("test.mycontext exists but is not a NamingContext")
#         sys.exit(1)

# Bind the Echo object to the test context
name = [CosNaming.NameComponent("Game", ""), ]

try:
    rootContext.bind(name, eo)
    print("New WhatsTheWord object bound")
except CosNaming.NamingContext.AlreadyBound:
    rootContext.rebind(name, eo)
    print("WhatsTheWord binding already existed -- rebound")

# Activate the POA
poaManager = poa._get_the_POAManager()
poaManager.activate()

# Block forever (or until the ORB is shut down)
orb.run()
