#include <stdio.h>
#include "Speedstuff.h"


void Speedstuff::setSpeed(int x){
	speed = x;
}
void Speedstuff::setPower(int x){
	power = x;
}
void Speedstuff::setCommandSetpoint(int x){
	commandSetpoint = x;
}
void Speedstuff::setKp(int x){
	kp = x;
}
void Speedstuff::setKi(int x){
	ki = x;	
}
int Speedstuff::getSpeed(){
	return speed;
}
int Speedstuff::getPower(){
	return power;
}
int Speedstuff::getCommandSetpoint(){
	return commandSetpoint;
}
int Speedstuff::getKp(){
	return kp;
}
int Speedstuff::getKi(){
	return ki;
}

