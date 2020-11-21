#include <stdio.h>
#include "Speedstuff.h"
#include <string>

Speedstuff::Speedstuff(){
	speed = 0;
	power = 0;
	commandSpeed=0;
	kp=0;
	ki=0;
	mode=0;
}

Speedstuff::Speedstuff(int speeed, int commandspeeed){
	speed = 0;
	power = 0;
	commandSpeed=0;
	kp=0;
	ki=0;
	mode=0;
}

void Speedstuff::calculatePower(){
	power = (kp + ki) * commandSpeed;
}
void Speedstuff::calculatePower(int x){
	int Verror = commandSpeed - speed, uk, uk1, ek, ek1;
	ek = Verror;
	// max power is 120
	if (power < 120)
    {
        uk = uk1 + (x/2) * (ek + ek1);
    }
    else
    {
        uk = uk1;
    }

	power = (kp * ek) + (ki * uk);

    uk1 = uk;
    ek1 = ek;
}
void Speedstuff::setMode(std::string x){
	if(x=="Override"){
		mode=1;
	} else {
		mode=0;
	}
}
void Speedstuff::setSpeed(int x){
	speed = x;
}
void Speedstuff::setPower(int x){
	power = x;
}
void Speedstuff::setcommandSpeed(int x){
	commandSpeed = x;
}
void Speedstuff::setKp(int x){
	kp = x;
}
void Speedstuff::setKi(int x){
	ki = x;	
}
int Speedstuff::getMode(){
	return mode;
}
int Speedstuff::getSpeed(){
	return speed;
}
int Speedstuff::getPower(){
	return power;
}
int Speedstuff::getcommandSpeed(){
	return commandSpeed;
}
int Speedstuff::getKp(){
	return kp;
}
int Speedstuff::getKi(){
	return ki;
}

