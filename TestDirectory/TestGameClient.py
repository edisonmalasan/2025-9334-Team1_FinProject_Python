import sys
from omniORB import CORBA, PortableServer
import CosNaming, WhatsTheWord

# Initialise the ORB
def main():
    # sys.argv.extend(["-ORBInitRef","NameService=corbaloc:iiop:localhost:10050/NameService"])
    orb = CORBA.ORB_init(["-ORBInitRef","NameService=corbaloc:iiop:localhost:10050/NameService"], CORBA.ORB_ID)

    # Obtain a reference to the root naming context
    obj = orb.resolve_initial_references("NameService")
    ncRef = obj._narrow(CosNaming.NamingContextExt)

    if ncRef is None:
        print("Failed to narrow the root naming context")
        sys.exit(1)

    # Resolve the name "test.my_context/ExampleEcho.Object"
    name = [CosNaming.NameComponent("Game", ""), ]

    try:
        obj = ncRef.resolve(name)
    except CosNaming.NamingContext.NotFound as ex:
        print("Name not found")
        sys.exit(1)

    # Narrow the object to an Example::Echo
    eo = obj._narrow(WhatsTheWord.game_logic.Game)

    if eo is None:
        print("Object reference is not an WhatsTheWord::Game")
        sys.exit(1)

    # Invoke the echoString operation
    eo.sendLetter('a')

if __name__ == "__main__":
    main()