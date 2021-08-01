/*

*/
#ifndef francois_h
#define francois_h

#include "Arduino.h"

class millisTimer
{
  public:
    millisTimer(unsigned long &timer, int temps, bool firstCycle);
    void evaluate();
    void restart();
  private:
    unsigned long &_timer;
    int _temps;
    bool _firstCycle;


};

#endif