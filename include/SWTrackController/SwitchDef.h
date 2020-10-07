//
// Created by Nathan Swanson on 10.6.20
//

#ifndef SWITCH_DEF_H
#define SWITCH_DEF_H

// Structure that holds data about a single train
class Switch
{
    

    private:
        // Variables
	    bool switch_position;
        int switch_id;
          
        // Constructor to initialize elements
	    Switch(int id)
	    {
            switch_id =id;
	    	switch_position = 0;

	    }

    public:

    bool getSwitchPos()
    {
        return switch_position;

    }
    bool swapSwitchPos()
    {
        if(switch_position ==1)
        {
            switch_position = 0;
        }
        if(switch_position ==0)
        {
            switch_position = 1;
        }
        else();

        return switch_position;
    };

  
};







#endif //SWITCH_DEF_H
