//
// Created by Nathan Swanson on on 10.6.20.
// System which will run the SW Track Controller module
//
#ifndef SW_TRACK_SYSTEM_HPP
#define SW_TRACK_SYSTEM_HPP

#include <vector>
#include "TrackController.hpp"


class TrackSystem
{
	private:
		/**
		 * @brief constructor for singleton object TrackSystem
		 */
		

		// Tracks
		std::vector<TrackController> p_Controllers;
		std::vector<std::vector<int>> blocks_Controlled;
		std::vector<bool> switchpositions;
		std::vector<bool> prevswitchpositions;


	

	public:
		/**
		 * @brief	gets singleton instance
		 * @return 	reference to this singleton TrackSystem Object
		 */
		TrackSystem()
		{
			std::vector<int> temp;
			blocks_Controlled.push_back({0, 62,61,60,59});
			blocks_Controlled.push_back({62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76});
			blocks_Controlled.push_back({63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 101});
			blocks_Controlled.push_back({77, 78, 79, 80, 81, 82, 83, 84});
			blocks_Controlled.push_back({85, 78, 79, 80, 81, 82, 83, 84});
			blocks_Controlled.push_back({85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100});
			blocks_Controlled.push_back({101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58});
			blocks_Controlled.push_back({29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14});
			blocks_Controlled.push_back({28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13});
			blocks_Controlled.push_back({13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1});
			blocks_Controlled.push_back({30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59});
			blocks_Controlled.push_back({58, 59, 60, 61});


			blocks_Controlled.push_back({1, 2, 3, 4, 5, 6, 7, 8, 9});
			blocks_Controlled.push_back({0, 9, 10, 11, 12, 13, 14, 15});
			blocks_Controlled.push_back({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16});
			blocks_Controlled.push_back({16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26});
			blocks_Controlled.push_back({17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27});
			blocks_Controlled.push_back({72, 73, 74, 75, 76, 27, 28, 29, 30, 31, 32});
			blocks_Controlled.push_back({72, 73, 74, 75, 76, 28, 29, 30, 31, 32, 33});
			blocks_Controlled.push_back({33, 34, 35, 36, 37});
			blocks_Controlled.push_back({34, 35, 36, 37, 38});
			blocks_Controlled.push_back({38, 39, 40, 41, 42, 43, 71, 70, 69, 68, 67});
			blocks_Controlled.push_back({39, 40, 41, 42, 43, 44, 71, 70, 69, 68, 67});
			blocks_Controlled.push_back({44, 45, 46, 47, 48, 49, 50, 51});
			blocks_Controlled.push_back({45, 46, 47, 48, 49, 50, 51, 52});
			blocks_Controlled.push_back({52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66});

			TrackController a;

			for(int i=1;i<26;i++)
			{
				p_Controllers.push_back(a);
			}
		}

		void updateOccupied(bool a, int b)
		{
			int count1;
			int count2;
			if(a==0)
			{

				for(int i=0;i<blocks_Controlled.size()-1;i++)
				{
					count1=i;
					
					for(int j=0;j<blocks_Controlled[i].size();j++)
					{
						count2=j;
						if(blocks_Controlled[i].at(j)==b)
						{
							break;
						}

					}
				}
			}
			else if(a==1)
			{

			}

			p_Controllers[count1].setOccupied(count2);

			for(int i=0;i<27;i+2)
		{
			if(i==i+1)
			{
				switchpositions.push_back(p_Controllers[i].getSwitchPos());
			}


		}
		}
		


		
		string makeOccupancies()
		{
			//green line
			 
			
			string out = "";

			std::vector<bool> temp;

			//green
			temp = p_Controllers[9].getOccupancy();

			//blocks 1-13
			for(int i =12;i>=0;i--)
			{
				out+=temp[i];
				}
			temp= p_Controllers[7].getOccupancy();

			//blocks 14-29
			for(int i=15;i>=0;i--)
			{
				out+=temp[i];
			}
			temp=p_Controllers[10].getOccupancy();

			//blocks 30-59
			for(int i=0;i<29;i++)
			{
				out+=temp[i];
			}
			temp=p_Controllers[11].getOccupancy();

			//blocks 60-61
			for(int i=2;i<4;i++)
			{
				out+=temp[i];
			}
			temp = p_Controllers[1].getOccupancy();

			//blocks 62-76
			for(int i=0;i<15;i++)
			{
				out += temp[i];
			}

			temp = p_Controllers[3].getOccupancy();

			//blocks 77-84
			for(int i=0;i<8;i++)
			{
				out += temp[i];
			}

			temp = p_Controllers[5].getOccupancy();

			//blocks 85-100
			for(int i=0;i<16;i++)
			{
				out +=temp[i];
			}

			temp = p_Controllers[6].getOccupancy();
			//blocks 101-151
			for(int i=0;i<51;i++)
			{
				out += temp[i];
			}

			out+=" ";
		
			//red
			//blocks 1-16
			for(int i=0;i<17;i++)
			{
				out+=temp[i];
			}

			temp = p_Controllers[16].getOccupancy();
				
			//blocks 17-27
			for(int i=0;i<11;i++)
			{
				out+=temp[i];
			}

			temp = p_Controllers[17].getOccupancy();

			//blocks 28-32
			for(int i=6;i<11;i++)
			{
				out+=temp[i];
			}
				
			temp = p_Controllers[19].getOccupancy();

			//blocks 33-37
			for(int i=0;i<5;i++)
			{
				out+=temp[i];
			}

			temp = p_Controllers[21].getOccupancy();

			//blocks 38-43
			for(int i=0;i<6;i++)
			{
				out+=temp[i];
			}

			temp = p_Controllers[23].getOccupancy();

			//blocks 44-51
			for(int i=0;i<8;i++)
			{
				out+=temp[i];
			}

			temp = p_Controllers[25].getOccupancy();
			//blocks 52-66
			for(int i=0;i<15;i++)
			{
				out+=temp[i];
			}

			temp = p_Controllers[21].getOccupancy();

			//blocks 67-71
			for(int i=10;i>5;i--)
			{
				out+=temp[i];
			}

			temp = p_Controllers[17].getOccupancy();

			//blocks 72-76
			for(int i=0;i<5;i++)
			{
				out+=temp[i];
			}

			return out;
		}

	string makePositions()
	{
		string out="";

		for(int i=0;i<27;i+2)
		{
			if(i==i+1)
			{
				out += p_Controllers[i].getSwitchPos();
			}
			else
			{
				break;
			}
		}

		return out;

	}

	bool getSinglePosition(int a)
	{
		return switchpositions[a];
	}

	int didSwitchMove()
	{
		for(int i=0;i<switchpositions.size();i++)
		{
			if(switchpositions.at(i)!=prevswitchpositions.at(i))
			{
				return i;
			}
			else
			{
				{
					return 14;
				}
			}
			
		}



	}

	void inputPositions(std::vector<bool> input, bool a)
	{
			if(a==0)
			{
				p_Controllers[6].addToQueue(input[0]);
				p_Controllers[7].addToQueue(input[0]);

				p_Controllers[8].addToQueue(input[1]);
				p_Controllers[9].addToQueue(input[1]);

				p_Controllers[8].addToQueue(input[4]);
				p_Controllers[9].addToQueue(input[4]);

				p_Controllers[10].addToQueue(input[2]);
				p_Controllers[11].addToQueue(input[2]);

				p_Controllers[10].addToQueue(input[3]);
				p_Controllers[11].addToQueue(input[3]);

				p_Controllers[4].addToQueue(input[5]);
				p_Controllers[5].addToQueue(input[5]);
				
				p_Controllers[4].addToQueue(input[8]);
				p_Controllers[5].addToQueue(input[8]);

				p_Controllers[1].addToQueue(input[6]);

				p_Controllers[1].addToQueue(input[7]);

				p_Controllers[6].addToQueue(input[9]);
				p_Controllers[7].addToQueue(input[9]);
			}
			else if (a==1)
			{


			}

	}

};

#endif // SW_TRACK_SYSTEM_HPP
