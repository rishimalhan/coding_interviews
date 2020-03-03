// Given a string simulate a robot and show if it forms a circle
#include <iostream>
#include <cmath>

// Create a struct to define robot position
struct pose
{
	int x;
	int y;
	int dir[2]; // Direction vector of the robot
};

void apply_transform(pose& curr_pose, int angle)
{
	int temp;
	temp = round(cos(angle*3.14/180)*curr_pose.dir[0] - sin(angle*3.14/180)*curr_pose.dir[0]);
	curr_pose.dir[1] = round(sin(angle*3.14/180)*curr_pose.dir[1] + cos(angle*3.14/180)*curr_pose.dir[1]);
	curr_pose.dir[0] = temp;
};

bool forms_circle(std::string cmd)
{
	// Simulate the robot
	pose init_pose;
	// Define start point and orientation
	init_pose.x = 0;
	init_pose.y = 0;
	init_pose.dir[0] = 0;
	init_pose.dir[1] = 1;

	pose curr_pose;
	curr_pose = init_pose;
	int i=0;
	while(cmd[i])
	{
		char curr_cmd = cmd[i];
		if (curr_cmd=='R') // Rotation of 90 degrees
		{
			apply_transform(curr_pose,-90);
		}
		if (curr_cmd=='L') // Rotation of -90 degrees
		{
			apply_transform(curr_pose,90);
		}
		if (curr_cmd=='M') // Progress the robot
		{
			curr_pose.x += curr_pose.dir[0];
			curr_pose.y += curr_pose.dir[1];
			std::cout<< curr_pose.x << "," << curr_pose.y << std::endl;
		}
		++i;
	}
	if (curr_pose.x==init_pose.x && curr_pose.y==init_pose.y)
		return true;
	else
		return false;
};

int main(int argc, char** argv)
{
	std::string cmd = "RRRR";
	if (forms_circle(cmd))
		std::cout<< "Circle detected" << std::endl;
	else
		std::cout<< "Circle not detected" << std::endl;
	return 0;
}