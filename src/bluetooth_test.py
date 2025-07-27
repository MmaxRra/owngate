
import bleak as ble


# Plejd device
class plejd_device:

    def __init__(self, device_name, device_address): 
        
        self.name    = device_name
        self.address = device_address

    def __str__(self): return f"{self.name} {self.address}"


# Stored plejd devices
plejd_devices = []


# Scan for plejd devices
async def scan():

    # Scan and iterate thru found devices
    devices = await ble.BleakScanner.discover()
    for device in devices: 
        
        # Remove non-plejd devices
        if(device.name == "P mesh"): plejd_devices.append(plejd_device(device.name, device.address))      

    # Display found devices
    #for d in plejd_devices: print(d)
    return plejd_devices


# Connect to device
async def connect(device):

    # Connect to device with address [device.address]
    async with ble.BleakClient(device.address) as client:

        if client.is_connected: 
            
            services = client.services
            for s in services: print(s)

        else: print("Failed to connect to device")


# Main entry
async def main():
   
    plejd_devices = await scan()
    await connect(plejd_devices[0])


# Run Main
import asyncio
if __name__ == "__main__": asyncio.run(main())