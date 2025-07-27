
from interface.device_light import DeviceLight
from bleak import BleakClient

# Toggle lightobj on
async def _toggle_on(lightobj: DeviceLight, dim: None, client: BleakClient):

    # Set dim
    if dim is not None: dim = int(dim)

    lightobj.state.obj_state = True
    lightobj.state.dim = dim

    pass
    
# Toggle lightobj off
async def _toggle_off(lightobj: DeviceLight, client: BleakClient):

    lightobj.state.obj_state = False
    pass

# Get lightobj state
async def _get_state(lightobj: DeviceLight, client: BleakClient):

    pass