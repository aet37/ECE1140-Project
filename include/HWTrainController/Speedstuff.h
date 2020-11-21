#ifndef Speedstuff_h
#define Speedstuff_h

#include <string>
class Speedstuff{
	private:
		int speed, power, commandSpeed, kp, ki;
		bool mode;
	public:
		Speedstuff();
		Speedstuff(int, int);
		void calculatePower();
		void calculatePower(int);
		void setMode(std::string);
		void setSpeed(int);
		void setPower(int);
		void setcommandSpeed(int);
		void setKp(int);
		void setKi(int);
		int getMode();	
		int getSpeed();
		int getPower();
		int getcommandSpeed();
		int getKp();
		int getKi();
};



#endif
