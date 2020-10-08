#include "Distance.h"

void Distance::setAuthority(int x){
	authority = x;
}
void Distance::setTransponder(int x){
	transponder = x;
}
int Distance::getAuthority(){
	return authority;
}
int Distance::getTransponder(){
	return transponder;
}
