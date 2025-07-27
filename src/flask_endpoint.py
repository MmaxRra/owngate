
from fastapi import FastAPI
from pydantic import BaseModel

from interface.plejd_light import PlejdLight
import asyncio


# Create API app
app = FastAPI()


# Definera inkommande JSON-data
class Value(BaseModel):
    state: str       # "on" eller "off"
    dim: int | None = None  # valfri dimnivå (%)

class ActionRequest(BaseModel):
    room: str        # t.ex. "Vardagsrum"
    action: str      # t.ex. "toggle"
    value: Value     # värde-objektet


# Stored plejd devices
plejd_devices = {
    "Vardagsrum": PlejdLight("C0:70:46:B8:ED:F7", "", "Vardagsrum"),
    "Sovrum":     PlejdLight("DA:94:C6:25:F3:2D", "", "Sovrum"),
    "Fasad":      PlejdLight("C9:D3:38:C4:3D:1D", "", "Fasad"),
    "Loft":       PlejdLight("F2:87:A0:03:52:D2", "", "Loft"),
    "Hall":       PlejdLight("DD:F2:8F:13:44:93", "", "Hall"),
    "Kök":        PlejdLight("FE:51:44:6C:B8:1E", "", "Kök")
}

# Pass some action to devices
@app.post("/action")
async def parse_command(req: ActionRequest):

    # Get room
    room = req.room
    if room not in plejd_devices: return {"error": f"Unknown room: {room}"}
    
    # Get device for room
    device = plejd_devices[room]

    # Pass action too plejd_interface
    await device.run_action({"action": req.action, "value": req.value})
    return {"success": True}


# Example json data 
# { ... }   

# Add new device
@app.post("/new")
def new_device(json_data: dict):

    pass


# Example json data 
# { ... }   

# states of specific device or all devices
@app.get("/states")
def get_states(json_data: dict):

    pass
