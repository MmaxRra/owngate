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

## Teknik

Plejd enheter använder sig av bluetooth 4.2 med mesh protokoll.
De har en möjlighet till 251 bytes per paket på ca 803 kbit/s.

### Säkerhet

Plejd enheterna använder sig av Elliptic Curve Diffie-Hellman (ECDH) för att generera AES nycklar när enheten först plir pair genom appen.. Efter detta besparas nycklarna i minne på enhten.

Man måste alltså vet AES nycklarna för enheterna i förväg?

Detta följer det schemat utav: 

- [Hitta enhet genom scanning]
- [Anslut till enhet]
- [Ta emot challenge]
- [Generera response med AES]
- [Skicka response (auth req.)]
- [Ta emot response (auth resp.)]
- [Skicka kontroll paket (med AES)]

### Identifiering och märkning av enheter

För att kunna tilldela AES nycklar till rätt enhet efter reverse engineering av dom 
så behöver man ha en vis identifiering för enheter.

MAC-adressen kan vara känslig då de kan ändras.
Metoden för att hämta unik data görs genom:

```python
bleak.BleakScanner.discover(return_adv=True)
```

Denna metod returnerar en dictionary av hittade enheter i samband med deras MAC-adresser samt metadata.

Information om manufacturer hämtas genom följande:

```python

    def format_manufacturer_data(data: bytes) -> str:
    
       byte_list = ' '.join(f"{b:02X}" for b in data)
       return (f"Bytes:  {byte_list}")
    

    for address, adv_data in devices.items(): 

       device_inf = adv_data[1]
       for cid, raw_data in device_inf.manufacturer_data.items():

              print(f"Manufacturer ID: {cid:#06x}")
              print(format_manufacturer_data(raw_data))
```

Vilket ger information i formatet:

```
Manufacturer ID: 0x0377            
Bytes:  07 00 00 16 D2 52 03 A0 87 F2 12 68 97 3B 6C B6 00
```

Analys av paket ger:

```
likew:  07 00 00 16 xx xx xx xx xx xx 12 68 yy yy yy yy 00

07 00 00 16	: Enhets typ? + System ID? 	[något med typ av enhet]
xx .. .. xx  	: Unikt ID			[diffande bland enheter]
12 68         : Mesh? 			[samma för alla enheter]
yy .. .. yy   : Firmware version          [framtaget genom tester]
00 		: padding/end		
```

Där xx .. .. xx kommer användas som identifierar för enheter.