#ifndef Trainfunctions_h
#define Trainfunctions_h



class Trainfunctions{
	private:
		bool trackSignal, emergencyBrake;
		int serviceBrake;
	public:
		Trainfunctions();
		//void setMode(int);
		void setTrackSignal(int);
		void setServiceBrake(int);
		void setEmergencyBrake(int);
		//int getMode();
		int getTrackSignal();
		int getServiceBrake();
		int getEmergencyBrake();	
};

#endif
