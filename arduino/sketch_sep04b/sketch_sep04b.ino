
/* 
 * Example of using the ChainableRGB library for controlling a Grove RGB.
 * This code fades in an out colors in a strip of leds.
 */


#include <ChainableLED.h>

#define NUM_LEDS  1

ChainableLED leds(30, 31, NUM_LEDS);

void setup()
{
  leds.init();
}

byte power = 0;

void loop()
{
  leds.setColorRGB(0, 255, 255, 255);
  delay(500);
  leds.setColorRGB(0, 0, 0, 0);

  delay(500);
}
