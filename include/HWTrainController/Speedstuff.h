#ifndef Speedstuff_h
#define Speedstuff_h


class Speedstuff{
	private:
		int speed, power, commandSetpoint, kp, ki;
	public:
		void setSpeed(int);
		void setPower(int);
		void setCommandSetpoint(int);
		void setKp(int);
		void setKi(int);	
		int getSpeed();
		int getPower();
		int getCommandSetpoint();
		int getKp();
		int getKi();
};



#endif
