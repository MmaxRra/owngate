# Funktionalitet

## Enheter

### Uppkoppling

Anslutning använder sig av lokal bluetooth mesh kontroll för att bygga ett nätverk.

Dvs. ett BLE (Bluetooth Low Energy) mesh nätverk.

### Gateway brygga

Plejd gateway ansluter till lokalt nätverk.
Och lyssnar för mesh trafik som sedan synkroniseras till molnet.

### Remote kontroll

Plejd appen går genom målnet till gatewayen. 
Gatewayn transmitterar över BLE till enheter.

### Cloud Sync

Configurerar ändringar gjorda i appen är
synkronsierade genom gateway till resten
av nätverket.

Håller data konsekvent mellan alla enheter.

## Arsitektur överblick

```
[ Plejd App (Phone/Tablet) ]         [ Internet ]
            │                             │
     (Remote command)              (Cloud Server)
            │                             │
     ┌──────▼──────┐                 ┌────▼─────┐
     │ Plejd Cloud │◄───────►───────►│ Gateway  │
     └─────────────┘    HTTPS        └────┬─────┘
                                           │
                                    Bluetooth Mesh
                                           │
                          ┌────────┬─────────────┬─────────┐
                          ▼        ▼             ▼         ▼
                      Plejd Dimmers, Relays, Scene Controllers...
```

