#include <iostream>
#include "Failures.h"

Failures::Failures(){
	engineFailure = 0;
	signalFailure = 0;
	brakeFailure = 0;
}
void Failures::setEngineFailure(int x){
	engineFailure = x;
}
void Failures::setSignalFailure(int x){
	signalFailure = x;
}
void Failures::setBrakeFailure(int x){
	brakeFailure = x;
}
int Failures::getEngineFailure(){
	return engineFailure;
}
int Failures::getSignalFailure(){
	return signalFailure;
}
int Failures::getBrakeFailure(){
	return brakeFailure;
}
