#include <iostream>
#include "Failures.h"

void Failures::setEngineFailure(int x)
{
	engineFailure = x;
}
void Failures::setSignalFailure(int x)
{
	signalFailure = x;
}
void Failures::setBrakeFailure(int x)
{
	brakeFailure = x;
}
int Failures::getEngineFailure()
{
	return engineFailure;
}
int Failures::getSignalFailure()
{
	return signalFailure;
}
int Failures::getBrakeFailure()
{
	return brakeFailure;
}
