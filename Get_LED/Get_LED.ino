#include <cvzone.h>

SerialData serialData(2, 1); //(numOfValsRec,digitsPerValRec)
int valsRec[2]; // array of int with size numOfValsRec 

void setup() {
  pinMode(8, OUTPUT);
  serialData.begin();
}

void loop() {

  serialData.Get(valsRec);
digitalWrite(8, valsRec[0]);

}
