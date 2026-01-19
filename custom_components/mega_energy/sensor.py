{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from homeassistant.components.sensor import SensorEntity\
from homeassistant.const import CURRENCY_EURO\
from datetime import datetime\
from .coordinator import MegaCoordinator\
\
SENSORS = [\
    ("EL", "YEAR"),\
    ("EL", "MONTH"),\
    ("EL", "DAY"),\
    ("GAS", "YEAR"),\
    ("GAS", "MONTH"),\
    ("GAS", "DAY"),\
]\
\
async def async_setup_entry(hass, entry, async_add_entities):\
    coordinator = MegaCoordinator(hass, entry.data)\
    await coordinator.async_config_entry_first_refresh()\
\
    sensors = [\
        MegaCostSensor(coordinator, market, interval)\
        for market, interval in SENSORS\
    ]\
    sensors.append(MegaTokenSensor(coordinator))\
    sensors.append(MegaBillingMonthSensor())\
\
    async_add_entities(sensors)\
\
class MegaCostSensor(SensorEntity):\
    def __init__(self, coordinator, market, interval):\
        self.coordinator = coordinator\
        self.market = market\
        self.interval = interval\
        self._attr_name = f"Mega \{market.lower()\} kost \{interval.lower()\}"\
        self._attr_device_class = "monetary"\
        self._attr_native_unit_of_measurement = CURRENCY_EURO\
\
    @property\
    def native_value(self):\
        return self.coordinator.costs.get(f"\{self.market\}_\{self.interval\}")\
\
class MegaTokenSensor(SensorEntity):\
    _attr_name = "Mega token status"\
    _attr_icon = "mdi:key-alert"\
\
    def __init__(self, coordinator):\
        self.coordinator = coordinator\
\
    @property\
    def native_value(self):\
        return self.coordinator.token_status\
\
class MegaBillingMonthSensor(SensorEntity):\
    _attr_name = "Mega huidige factuurmaand"\
    _attr_icon = "mdi:calendar-month"\
\
    @property\
    def native_value(self):\
        return datetime.now().strftime("%Y-%m")}