/*
*@file TrackModelData.hpp
*/

#ifndef TRACKMODELDATA_HPP
#define TRACKMODELDATA_HPP

namespace TrackModel
{
    int distance = 0;
    int speed_limit;
    int block = 1;
    void setSpeedLimit(int speed){
        speed_limit = speed;
    }

    int getSpeedLimit()
    {
        return speed_limit;
    }

    int getBlockNumber()
    {
        distance++;
        if (distance % 4 == 0)
        {
            block++;
            distance = (distance - 4);
        }
        return block;
    }

}

#endif