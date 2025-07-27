
import bleak as ble


# UUID CHARACTERISTICS
BLE_UUID_SUFFIX  = "6085-4726-be45-040c957391b5"
UUID_SERVICE    = f"31ba0001-{BLE_UUID_SUFFIX}"
UUID_LIGHTLEVEL = f"31ba0003-{BLE_UUID_SUFFIX}"
UUID_DATA       = f"31ba0004-{BLE_UUID_SUFFIX}"
UUID_LASTDATA   = f"31ba0005-{BLE_UUID_SUFFIX}"
UUID_AUTH       = f"31ba0009-{BLE_UUID_SUFFIX}"
UUID_PING       = f"31ba000a-{BLE_UUID_SUFFIX}"

# Stored plejd devices
_devices = []

# Plejd device
class _device:

    def __init__(self, device_name, device_address): 
        
        self.name    = device_name
        self.id      = device_address
        self.AES_KEY = None

    def __str__(self): return f"{self.name} {self.id}"


import binascii, struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

#                AES KEY   DEVICE ID  PAYLOAD DATA
def encrypt_data(key: str, addr: str, data: bytearray) -> bytearray:

    # Final output
    output = b""

    # Format for encryption
    key  = binascii.a2b_hex(key.replace("-", ""))
    addr = binascii.a2b_hex(addr.replace(":", ""))

    cipher = Cipher(algorithms.AES(bytearray(key)), modes.ECB(), backend=default_backend())
    cipher = cipher.encryptor()

    buf = addr + addr + addr[:4]
    cipher = cipher.update(buf)
    
    for i, d in enumerate(data): output += struct.pack("B", d ^ cipher[i % 16])
    return output


# Format manufacturer data
def format_manufacturer_data(data: bytes) -> str:
    
    byte_list = ' '.join(f"{b:02X}" for b in data)
    return f"Bytes:  {byte_list}"


# Scan for plejd devices
async def scan():

    # Scan and iterate thru found devices
    devices = await ble.BleakScanner.discover(return_adv=True)
    for address, adv_data in devices.items(): 

        device_inf = adv_data[1]
        if device_inf.local_name == "P mesh": 
            
            _devices.append(_device(device_inf.local_name, address))
            #for cid, raw_data in device_inf.manufacturer_data.items():
            #
            #    print(f"Manufacturer ID: {cid:#06x}")
            #    print(format_manufacturer_data(raw_data))

    # Display found devices
    for d in _devices: print(d)
    return _devices


# Callback for notifications
def handle_notification(sender: str, data: bytearray):

    print(f"Notification from {sender}: {data.hex()}")

# Connect to device
async def connect(device):

    # Connect to device with address [device.id]
    async with ble.BleakClient(device.id) as client:

        try:

            #await client.start_notify(PLEJD_PING, handle_notification)
            challenge = await client.read_gatt_char(UUID_AUTH)
            print(challenge)
                
            #payload_final = encrypt_data(device.AES_KEY, device.id, binascii.a2b_hex(payload.replace(" ", "")))
            #await client.write_gatt_char(PLEJD_FUNCTION_UUID, payload_final)
            
        except Exception as e: print(e)


# Main entry
async def main():
   
    _devices = await scan()
    await connect(_devices[0])
    
# Run Main
import asyncio
if __name__ == "__main__": asyncio.run(main())