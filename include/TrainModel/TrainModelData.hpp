
/**
 * @file TrainModelData.hpp
*/
#ifndef TRAINMODELDATA_HPP
#define TRAINMODELDATA_HPP

// SYSTEM INCLUDES
// (none)

namespace TrainModel
{
int trainlength;
int speedLimit;
int power;
void setTrainLength(int len)
{
    trainlength = len;
}
int getTrainLength()
{
    return trainlength;
}
void setPower(int pow)
{
    power = pow;
}
int getPower()
{
    return power;
}

int tm_train_id, tm_authority, tm_command_speed, tm_current_speed, tm_speed_limit;
/**
 * @brief	Buffer function to send info about new train from CTC to Track Controller
 *
 * @param[in]	train_id
 * @param[in]	authority
 * @param[in]	command_speed
 * @param[in]   current_speed
 * @param[in]   speed_limit
 *
 * @return	None
 */
void TrainInfoBuffer_TrainModel(int train_id, int authority, int command_speed, int current_speed, int speed_limit)
{
	tm_train_id = train_id;
	tm_authority = authority;
	tm_command_speed = command_speed;
	tm_current_speed = current_speed;
	tm_speed_limit = speed_limit;
}

int getID()
{
    return tm_train_id;
}
int getAuthority()
{
    return tm_authority;
}
int getCommandSpeed()
{
    return tm_command_speed;
}
int getCurrentSpeed()
{
    return tm_current_speed;
}
int getSpeedLimit()
{
    return tm_speed_limit;
}


} // namespace TrainModel

#endif // TRAINMODELDATA_HPP
