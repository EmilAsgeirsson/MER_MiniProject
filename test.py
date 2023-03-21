from Encoder.scripts.encoder import Encoder
from time import sleep

#encoder = Encoder(port="COM3")
ports = Encoder.check_for_COM()
print(ports)



"""
encoder.start_thread()
count = 0
while True:
    print(encoder.get_data())
    count += 1
    if count > 9:
        break
    sleep(1)

encoder.end_thread()
"""