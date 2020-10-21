#ifndef Distance_h
#define Distance_h

class Distance{
	private:
		int authority, transponder;
	public:
		void setAuthority(int);
		void setTransponder(int);
		int getAuthority();
		int getTransponder();		
};

#endif
