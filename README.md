Custom integratie voor het ophalen van **kosten** (geen verbruik) voor\
elektriciteit en gas bij Mega.\
\
## Features\
- UI configuratie\
- Jaar / maand / dag kosten\
- Token-verval detectie + notificatie\
- Huidige factuurmaand sensor\
- Custom Lovelace kaart\
- HACS compatible\
\
## Installatie\
1. Voeg repo toe aan HACS (Custom repository)\
2. Installeer\
3. Herstart Home Assistant\
4. Voeg integratie toe via UI\
\
## Lovelace kaart\
```yaml\
type: custom:mega-energy-card\
energy: el\
period: month}
