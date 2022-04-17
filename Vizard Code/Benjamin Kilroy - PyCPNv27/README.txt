DESCRIPTION OF FILES
====================
1. pyCPN.py is Python module implementing the Comms/CPN functionality.
2. pyEncodeDecode.py contains functions to convert a string to bytes and vice versa.
3. pyCPNClient.py is a simple client that interacts with CPN model HelloNameCPNComm.cpn.                     
   It requests a connection to the model (which is running as a server), 
   sends a string and receives a response. The server closes connection if string 
   quit is sent by the client.
4. HelloNameCPNComm.cpn is a simple net that starts the server and is ready to
   accept a connection request on the specified port. It receives a string from
   the client and appends the string Hello to it and send it back to
   client. This is repeated until quit is received.
5. serverEx.py is a server that works with the client above if not using the CPN model.

HOW TO RUN
===========
1. Start the CPN model HelloNameCPNComm.cpn and click on transition Connect to
   start listening on the port. (or start the serverEx.py if not using CPN)
2. Run pyCPNClient.py via python pyCPNClient.py or load in a Python interactive shell. 
   Type a name (or any sequence of characters) and hit return.
3. On the CPN side click on the appropriate transitions to receive the string
   and send response. (no action required if using serverEx.py)
