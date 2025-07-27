## Enheter

### Uppkoppling

Anslutning använder sig av lokal bluetooth mesh kontroll för att bygga ett nätverk.

Dvs. ett BLE (Bluetooth Low Energy) mesh nätverk.

### Gateway brygga

Plejd gateway ansluter till lokalt nätverk. Och lyssnar för mesh trafik som sedan synkroniseras till molnet.

### Remote kontroll

Plejd appen går genom målnet till gatewayen. Gatewayn transmitterar över BLE till enheter.

### Cloud Sync

Configurerar ändringar gjorda i appen är synkronsierade genom gateway till resten
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

## Teknik

Plejd-enheter använder Bluetooth Low Energy (BLE) 4.2, och kommunicerar över ett proprietärt mesh-protokoll ovanpå BLE.

- Maximal användbar paketstorlek via BLE 4.2 är **251 bytes** (att MTU är ökad från 23 till 251).
- Teoretisk maxhastighet för BLE 4.2 är ca **1 Mbps**, men i praktiken får man **~800 kbit/s** under goda förhållanden.
- Mesh-nätverket är **ej baserat på Bluetooth Mesh-standarden** (t.ex. som Zephyr eller SIG Bluetooth Mesh), utan är en egen lösning anpassad för Plejd-enheters behov.

### Säkerhet

Varje Plejd enhet har en AES nyckel bundet till sig som används för att kryptera data som skickas till/från enheten. Dessa AES nycklar tas fram genom reverse engineering av olika ble paket. Man måste alltså veta AES nycklarna för varje enhet.

### Autentisering

Autentiseringen sker genom följande process:

- Anslut till enhet
- Ta emot challenge
- Generera response med AES
- Skicka response (auth req.)
- Skicka paket (med AES)

### Identifiering och märkning av enheter

Varje enhet har från manufacturerat tilldelats en unik identifierare. Denna identifierare användes även som den statiska MAC-adressen för enheten, dvs. den MAC-adress som används för anslutning och interaktion med enheten.