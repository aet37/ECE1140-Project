#include "Distance.h"

// void Distance::setAuthority(int x){
// 	authority = x; // Use joystick to set authority up or down
// }
// void Distance::setTransponder(int x){
// 	transponder = x; //Use button to get transponder 
// }
Distance::Distance(int auth){
	authority = auth;
}
int Distance::getAuthority(){
	return authority;
}
int Distance::getTransponder(){
	return transponder;
}
