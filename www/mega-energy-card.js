{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 class MegaEnergyCard extends HTMLElement \{\
  setConfig(config) \{\
    this.config = config;\
  \}\
\
  async set hass(hass) \{\
    this._hass = hass;\
    if (!this.chart) \{\
      this.render();\
    \}\
  \}\
\
  render() \{\
    const energy = this.config.energy || "el";\
    const period = this.config.period || "month";\
    const entity = `sensor.mega_$\{energy\}_kost_$\{period\}`;\
    const state = this._hass.states[entity];\
\
    this.innerHTML = `\
      <ha-card header="Mega Energy Kosten">\
        <div style="padding:16px">\
          <div style="font-size:2em">\'80 $\{state ? state.state : "?"\}</div>\
        </div>\
      </ha-card>\
    `;\
  \}\
\}\
\
customElements.define("mega-energy-card", MegaEnergyCard);}