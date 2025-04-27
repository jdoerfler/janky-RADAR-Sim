Check janky.jpg for a rough idea about what we're working with, except moving to an RPi4 instead of Pico

Transceiver library - https://nrf24.github.io/pyRF24/index.html 

Questions to resolve include but are not limited to:
- Physical case for the Rpi and antennas and such
- UI for the Fighter and SAM
- How limited hardware interface can handle 'sending' and 'receiving' radar or how we can simulate it (e.g. moving average of 'packets acknowledged'/'packets sent')
- game parameters and easy variations
- building out user-friendly configuration, such as the ability to open the case and toggle some settings via button.
