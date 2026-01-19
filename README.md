{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Mega Energy Costs (Home Assistant)\
\
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