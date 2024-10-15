# ATMega328P-Analog-Input
Firmware for an ATMega328P, coupled with ardiuno nano. This firmware package configures the MCU to enable the ADC on specified analog input pins for signal capture. 

MCU --> ATMega328P on a arduinonano
Peripheral --> KY-028 Digital Temperature Sensor Module (specifically using the A0 analog signal pin)
  - Note, any input analog signal can work with this setup. A temperature sensor was tested, so was a PWM signal from another arduino. 


we are using portC, the analog read in on PC5 
1. Enable the ADEN bit within the ADCSRA register
2. Once the ADC has calculated a value, it is then stored within the ADCH and ADCL registers. That is Analog-to-Digital-Convertor-HIGH/LOW. The data is presetned 
"right adjusted", or little endian.
3. Access the data within ADCH, this will then re-enable access to ADCH and ADCL from the ADC.
4. Start the conversion by disabling the power reduction ADC bit, PRADC, by writing a 0 and writing a 1 to the start conversion bit to ADSC. 
5. (OPTIONAL) Automatically trigger a conversion by setting the auto triggering but, ADATE, within ADCSRA. For this we will also need to specify the trigger
and we do this by setting the ADC trigger select bits, ADTS, in ADCSRB. When triggering a snap of the input signal for convserion, ADIF flag will be raised. If we put the pin on auto trigger mode, then we also need to write a logical 1 
to ADSC in ADCSRA. You will need to manually write to the ADSC in ADCSRA a 1 to enable the auto triggering. This will continue on its own in free-running mode. 


## Contents
- PlatformIo Initialization
- src/main.c --> Firmware
- python/readSerial.py --> Python script for analog visualization


## Pinout of Arduino
A5 --> Input Analog PIN\
AREF --> Jumper wire over to 5V

## Dependencies 
### Main Firmware
- [PlatformIO](https://platformio.org/) --> Used for creating the packages firmware, flashing, and deploying onto ATMega328P MCU.
- [Avrdudes/AVR](https://github.com/avrdudes/avr-libc)
- [Arduino C Library](https://docs.arduino.cc/libraries/)
### Analog Signal Visualization
- [Matplotlib](https://matplotlib.org/) -> Visualizing continous time varying temperature
- [Numpy](https://numpy.org/) -> array and matrix handling 
- [Pyserial](https://pyserial.readthedocs.io/en/latest/index.html) -> read incoming data from COM port
