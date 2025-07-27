# owngate (inofficiell)

Ett projekt för lokal styrning av Plejd-belysningsenheter med kompatibilitet för Google Home Assistant styrning. 

Projektet ersätter behovet av molnbaserad gateway genom lokal anslutning direkt via Bluetooth.

---

## 🚧 Work in Progress

Detta är ett hobbyprojekt som inte är affilierat med Plejd AB. Se [DISCLAIMER.md](./DISCLAIMER.md) för mer information.

---

## ✨ Funktioner

- Ansluter till enheter via BLE
- Autentisering via AES-baserad challenge-response
- Skickar styrkommandon lokalt (t.ex. dim, toggle)
- Kompatibel med integration till andra system (t.ex. Home Assistant, REST API)

---

## 🔧 Teknisk översikt

### Kommunikation

- Bluetooth 4.2 + Mesh
- GATT-baserad kommunikation
- AES-kryptering används för alla styrpaket

### Begränsningar

- Kräver att du har dina egna AES-nycklar (.env)
- Styrning måste ske lokalt (ingen molntjänst används)

---

## 🧪 Exempel

```json
{
  "room": "Vardagsrum",
  "action": "toggle",
  "value": {
    "state": "on",
    "dim": 75
  }
}