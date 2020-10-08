#include <iostream>
#include "Insidetrain.h"

void Insidetrain::setLights(int x){
	lights = x;
}
void Insidetrain::setDoors(int x){
	doors = x;
}
void Insidetrain::setEmergencyPassengerBrake(int x){
	emergencyPassengerBrake = x;
}
void Insidetrain::setTemperature(int x){
	temperature = x;
}
void Insidetrain::setAdvertisements(int x){
	advertisements = x;
}
void Insidetrain::setAnnouncements(int x){
	announcements = x;
}
int Insidetrain::getLights(){
	return lights;
}
int Insidetrain::getDoors(){
	return doors;
}
int Insidetrain::getEmergencyPassengerBrake(){
	return emergencyPassengerBrake;
}
int Insidetrain::getTemperature(){
	return temperature;
}
int Insidetrain::getAdvertisements(){
	return advertisements;
}
int Insidetrain::getAnnouncements(){
	return announcements;
}
