#include <ChainableLED.h>
 
#define NUM_LEDS  1
 
ChainableLED leds(31, 30, NUM_LEDS);
 
void setup()
{
  leds.init();
}

 
void loop()
{
    leds.setColorRGB(0, 255, 355, 255);
    delay(500);
    leds.setColorRGB(0, 0, 0, 0);
    delay(500);
    
 
  
}
