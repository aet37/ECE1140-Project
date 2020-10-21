#include <iostream>
#include "Trainfunctions.h"

void Trainfunctions::setMode(int x){
	mode = x;
}
// void Trainfunctions::setTrackSignal(int x){
// 	trackSignal = x;
// }
void Trainfunctions::setServiceBrake(int x){
	serviceBrake = x;
}
void Trainfunctions::setEmergencyBrake(int x){
	emergencyBrake = x;
}
int Trainfunctions::getMode(){
	return mode;
}
int Trainfunctions::getTrackSignal(){
	return trackSignal;
}
int Trainfunctions::getServiceBrake(){
	return serviceBrake;
}
int Trainfunctions::getEmergencyBrake(){
	return emergencyBrake;
}
