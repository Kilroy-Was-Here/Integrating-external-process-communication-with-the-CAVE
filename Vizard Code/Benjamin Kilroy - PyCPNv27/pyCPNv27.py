# Python implementation of Comms/CPN similar to Java/CPN for use with CPN Tools.
# Author: Vijay Gehlot
# Version: 0.1 
# Created: 2019-04-30
# Revision of orignial PyCPN targeted to Python v 2.7
# Based on: JavaCPN.java by Guy Gallasch and distributed by cpntools.org
# Currently not much in terms of meaningful exceptions
# Tested with Python v 2.7.10 and CPN Tools v 4.0.1

import socket
import sys
import struct

class PyCPN:

    def __init__(self):
        self.socket = None

    def connect(self, hostName, port):
        self.socket = socket.create_connection((hostName, port))
    
    def accept(self,port):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(('', port)) # bind and listen from any
        serverSocket.listen(0) # v2.7 requires explicit param
        self.socket, client_addr = serverSocket.accept()
        serverSocket.close()
    
    
    # Method used to send a byte array via an established
    # connection. This method takes a byte arra (encoded string) object
    # as the argument.  The segmentation into packets occurs in this method. 
    # Bytes are read from the byte array object, a maximum
    # of 127 at a time, and a single byte header is added indicating the
    # number of payload bytes (header is 1 to 127) or that there is more data 
    # in a following packet (header is 255). The data packets formed are then
    # transmitted to the external process through methods acting on the
    # output stream of the socket. 
    # NOTE: For v 2.7 issue with ascii decode of header 255 so scaled down to 127 
 
    def send(self,sendBytes):
        # convert bytes to list for conveneience
        encoded_string = sendBytes.encode()
        bytes_to_send = bytearray(encoded_string)
        # While there are more than 127 bytes still to send ...
        while len(bytes_to_send) > 63: #127:
            # ... create a byte packet, ...
            #packet = [] 
            packet = bytearray('')
            # ... set the header to 127 (old 255), ... issue with ascii decoding of 255 in 2.7
            packet.append(127)
            # ... read 63 (old 127) bytes from the sequence of bytes to send, ...
            for i in range(63): #range(127):
                packet.append(bytes_to_send[i])
            # Update bytes to send
            bytes_to_send = bytes_to_send[63:] #bytes_to_send[127:]
            # Send the packet to the external process
            #self.socket.sendall(bytes(packet))
            self.socket.sendall(packet.decode())
            
        # Create a packet for any remaining data
        #packet = [] 
        packet = bytearray('')
        # Set the header appropriately
        packet.append(len(bytes_to_send))
        # Read the remaining bytes into the packet
        for i in range(len(bytes_to_send)):
            packet.append(bytes_to_send[i])
        # Send the packet to the external process
        #self.socket.sendall(bytes(packet))
        #self.socket.sendall(packet.decode('latin_1'))
        self.socket.sendall(packet.decode())
        
 
    
    # Method used to receive a byte array stream from an established
    # connection. This method has no arguments.  It uses methods that
    # act on the input stream of the socket to firstly receive a header
    # byte, and then receive the number of payload bytes specified in the
    # header, from the external process.  The payload bytes are stored in a
    # byte array object as each segment of payload data is
    # received. This process is repeated until all data has been received for
    # the current transmission. 
    def receive(self):
        # The complete sequence of bytes received from the external process
        receivedBytes = ''
        # The header received from the external process
        header = None
        # The total number of payload bytes received from the external process for
        # a packet, if not all are received immediately.
        totalNumberRead = None
        
        while True:
            # Read a header byte from the input stream
            header = self.socket.recv(1)
            iheader = struct.unpack('>B',header)[0] #int.from_bytes(header, byteorder='big')
            if iheader >= 63: #127:
                payload_len = 63 #127
            else:
                payload_len = iheader
            # Read the payload_len bytes from the input stream
            # Reset the total bytes received to 0 for this iteration 
            totalNumberRead = 0
            # Payload bytes received from the external process for a packet
            chunks = ''
            # Loop until all data has been read for this packet.
            while totalNumberRead < payload_len:
                # Try to read all bytes in this packet
                chunk = self.socket.recv(payload_len - totalNumberRead)
                if chunk == '':
                    raise RuntimeError("socket connection broken")
                #chunks.append(chunk)
                chunks += chunk
                totalNumberRead += len(chunk)
            receivedBytes += chunks
            # If no more bytes to follow, break from the loop.
            if iheader <= 63: #127:
                break
        # Return the received bytes
        #return b''.join(receivedBytes)
        return receivedBytes

    # Method to disconnect the established connection. 
    def disconnect(self):
        self.socket.close()

