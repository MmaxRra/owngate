
from dataclasses import dataclass
from bleak import BleakClient

import interface.device_actions as action
from ble.ble_characteristics import *
from ble.ble_crypto import auth_response


@dataclass
class DeviceState:
    
    available: bool
    obj_state: bool
    dim: int


class DeviceLight():


    # Init ligth object
    def __init__(self, device_address: str, AES_KEY: str, name: str):
        
        self.address = device_address
        self.name    = name
        self.state   = DeviceState(True, False, 0)
        self.AES_KEY = AES_KEY
    

    # Handle action
    async def run_action(self, inf: dict):

        async with BleakClient(self.address) as client:
            
            try: 
                await self._authenticate(client)
                await self._run_action(client, inf)
                client.disconnect()

            except Exception as e: print(f"[{self.address}] Error during action: {e}")
    

    # Authenticate with device
    async def _authenticate(self, client: BleakClient):

        challenge = await client.read_gatt_char(UUID_AUTH)
        response = auth_response(self.AES_KEY, challenge)
        await client.write_gatt_char(UUID_AUTH, response, response=True)
    
    
    # Run action on device
    async def _run_action(self, client: BleakClient, inf: dict):

        if inf["action"] == "get_state": await action._get_state(self, client)
        elif inf["action"] == "toggle":

            state = inf.get("value", {}).get("state")
            dim = inf.get("value", {}).get("dim")

            if state == "on": await action._toggle_on(self, dim, client)
            elif state == "off": await action._toggle_off(self, client)


    # Logging
    def __str__(self): 
        
        return f"<DeviceLight name={self.name}, address={self.address}, dim={self.state.dim}, state={self.state.obj_state}>"