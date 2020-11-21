#ifndef Failures_h
#define Failures_h

class Failures{
	private:
		bool engineFailure, signalFailure, brakeFailure;
	public:	
		Failures();
		void setEngineFailure(int);
		void setSignalFailure(int);
		void setBrakeFailure(int);
		int getEngineFailure();
		int getSignalFailure();
		int getBrakeFailure();
};

#endif
