/*
*@file TrackModelData.hpp
*/

#ifndef TRACKMODELDATA_HPP
#define TRACKMODELDATA_HPP

namespace TrackModel
{
    int speed_limit;
    void setSpeedLimit(int speed){
        speed_limit = speed;
    }

    int getSpeedLimit()
    {
        return speed_limit;
    }
}

#endif