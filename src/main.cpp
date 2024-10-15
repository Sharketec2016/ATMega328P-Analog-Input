#include <avr/io.h>
#include <util/delay.h>
#include "Arduino.h"
#include <avr/interrupt.h>


/*
MCU --> ATMega328P on a arduinonano
Peripheral --> KY-028 Digital Temperature Sensor Module (specifically using the A0 analog signal pin)
  - Note, any input analog signal can work with this setup. A temperature sensor was tested, so was a PWM signal from another arduino. 


we are using portC, the analog read in on PC5 
1. We need to enable the ADEN bit within the ADCSRA register
2. Once the ADC has calculated a value, it is then stored within the ADCH and ADCL registers. That is Analog-to-Digital-Convertor-HIGH/LOW. The data is presetned 
"right adjusted".
3. When we access the data within ADCH, this will then re-enable access to ADCH and ADCL from the ADC.
4. We need to start the conversion by disabling the power reduction ADC bit, PRADC, by writing a 0 and writing a 1 to the start conversion bit, ADSC. 
5. (OPTIONAL) we can automatically trigger a conversion by setting the auto triggering but, ADATE, within ADCSRA. For this we will also need to specify the trigger
and we do this by setting the ADC trigger select bits, ADTS, in ADCSRB. 
6. When we trigger a snap of the input signal for convserion, ADIF flag will be raised. If we put the pin on auto trigger mode, then we also need to write a logical 1 
to ADSC in ADCSRA. 

We need to manually write to the ADSC in ADCSRA a 1 to enable the auto triggering. This will continue on its own in free-running mode. 


*/

int reg1 = 0x79;
int reg2 = 0x78;
short offset = 0.035;

void setupADC();
void startConversion();
float grabAns();


void startConversion(){
  /*
  Function to start the conversion of the ADC values by writing a 1 to ADSC place in ADC status register A
  */
  ADCSRA |= _BV(ADSC); //analogus to (1 << ADSC) 
}

void setupADC(){
  /*
  Function to setup the ADC into a state where it will be able to read the input values. 
  ADMUX is set such that an external voltage is passed for the reference and setting up ADC5 for single ended input use.
  ADCSRA  is the ADC status register A, and is enabled to accept input. ADATE is also set to auto trigger a capture of the read values.

  ADPS0,1,2 are set as to set a division factor between system clock freq and input clock on ADC. Here the ATMega328P has a 16 MHz clock, and the division factor is 128.
  */
  ADMUX = 0b00000101; 
  ADCSRA = _BV(ADEN) | _BV(ADPS0) | _BV(ADPS1) | _BV(ADPS2) | _BV(ADATE);
  ADCSRB = 0x00;
  ADLAR = 0;
  DIDR0 |= (1 << ADC5D);


  startConversion();

}

float grabAns(){
  
  uint8_t low  = ADCL;
  uint8_t high = ADCH;


  uint16_t adc = (high << 8) | low;		// 0<= result <=1023
  float adcVoltage = ((5.0 * adc) / 1024.0);
  
 
  return adcVoltage;

}

void setup(){
  DDRC &= ~(1 << DDC5);
  Serial.begin(115200);
}

int main(void){
  setup();
  setupADC();

  while(1){
    float ans = grabAns();
    Serial.print("Measured voltage: "); 
    Serial.println(ans);
    
  }

}