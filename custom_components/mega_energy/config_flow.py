{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from homeassistant import config_entries\
import voluptuous as vol\
from .const import *\
\
class MegaEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):\
    VERSION = 1\
\
    async def async_step_user(self, user_input=None):\
        if user_input:\
            return self.async_create_entry(\
                title="Mega Energy",\
                data=user_input,\
            )\
\
        schema = vol.Schema(\{\
            vol.Required(CONF_TOKEN): str,\
            vol.Required(CONF_CUSTOMER_ID): str,\
            vol.Required(CONF_CONTRACT_ID): str,\
            vol.Required(CONF_POINT_ID): str,\
            vol.Required(CONF_DGO_GLN): str,\
            vol.Required(CONF_POSTAL_CODE): str,\
        \})\
\
        return self.async_show_form(step_id="user", data_schema=schema)}