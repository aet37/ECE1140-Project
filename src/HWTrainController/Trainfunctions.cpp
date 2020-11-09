#include <iostream>
#include "Trainfunctions.h"


void Trainfunctions::setTrackSignal(int x){
	trackSignal = x;
}
void Trainfunctions::setServiceBrake(int x){
	serviceBrake = x;
}
void Trainfunctions::setEmergencyBrake(int x){
	emergencyBrake = x;
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
