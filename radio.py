import nrf24l01 as rf
from machine import SPI, Pin
import struct
from time import sleep

payload_size = 20
send_pipe = b"\xe1\xf0\xf0\xf0\xf0"
receive_pipe = b"\xd2\xf0\xf0\xf0\xf0"

role = 'transmitter'

csn = Pin(7, mode=Pin.OUT, value=1)
ce = Pin(4, mode=Pin.OUT, value=0)

def setup():
    print("initializing ...")
    nrf = rf.NRF24L01(SPI(0), csn, ce, payload_size=payload_size)
    nrf.open_tx_pipe(send_pipe)
    nrf.open_rx_pipe(1, receive_pipe)
    nrf.start_listening()
    return nrf

def send(nrf, msg):
    print("sending message.", msg)
    nrf.stop_listening()
    for n in range(len(msg)):
        try:
            encoded_string = msg[n].encode()
            byte_array = bytearray(encoded_string)
            buf = struct.pack("s", byte_array)
            nrf.send(buf)
            print(role,"message",msg[n],"sent")
            
        except OSError:
            print(role,"Sorry message not sent")
    nrf.send("\n")
    nrf.start_listening()
    
nrf = setup()
nrf.start_listening()
msg_string = ""

while True:
    msg = ""
    if role == "send":
        send(nrf, "Yello world")
        send(nrf, "Test")
    else:
        # Check for Messages
        if nrf.any():
            package = nrf.recv()          
            message = struct.unpack("s",package)
            msg = message[0].decode()

            # Check for the new line character
            if (msg == "\n") and (len(msg_string) <= 20):
                print("full message",msg_string, msg)
                msg_string = ""
            else:
                if len(msg_string) <= 20:
                    msg_string = msg_string + msg
                else:
                    msg_string = ""