#ifndef Insidetrain_h
#define Insidetrain_h



class Insidetrain{
	private:
		bool lights, doors, emergencyPassengerBrake, advertisements, announcements;
		int temperature;
	public:
		Insidetrain();
		void setLights();
		void setDoors(int);
		void setEmergencyPassengerBrake(int);
		void setTemperature(int);
		void setAdvertisements(int);
		void setAnnouncements(int);
		int getLights();
		int getDoors();
		int getEmergencyPassengerBrake();
		int getTemperature();
		int getAdvertisements();
		int getAnnouncements();
};
#endif
