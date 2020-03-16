#include <cmath>

class Solution {
private:
    struct pose{
        int x;
        int y;
        int dir[2]; // Direction vector
    };
    void apply_transform(int *dir, int angle)
    {
        int temp = round(cos(angle*3.141592653589793/180)*dir[0] - sin(angle*3.141592653589793/180)*dir[1]);
        dir[1] = round(sin(angle*3.141592653589793/180)*dir[0] + cos(angle*3.141592653589793/180)*dir[1]);
        dir[0] = temp;
    };
    // void print_obs_grid(std::unordered_map<int, std::unordered_set<int>> grid){
    //     for (int i=-100; i<100; ++i){
    //         if (grid.count(i)>0){
    //             std::cout<< i << ": ";
    //             auto temp = grid.find(i)->second;
    //             for (int j=-100; j<100; ++j){
    //                 if (temp.count(j)>0)
    //                     std::cout<< j << ",";
    //             }
    //             std::cout<< std::endl;
    //         }
    //     }
    // };
public:
    int robotSim(vector<int>& commands, vector<vector<int>>& obstacles) {
        // Generate a multi dimensional obstacle grid where x and y values are stored for an obstacle
        std::unordered_map<int, std::unordered_set<int>> obs_grid;
        std::unordered_set<int> temp;
        for (size_t i=0; i<obstacles.size(); ++i){
            if (obs_grid.count(obstacles[i][0])>0){ // If the x element is already present
                temp = obs_grid.find(obstacles[i][0])->second; // The set which stores y values
                temp.insert(obstacles[i][1]);
                obs_grid.erase(obstacles[i][0]);
                obs_grid.emplace(obstacles[i][0],temp);
            }
            else{
                temp.clear();
                temp.insert(obstacles[i][1]);
                obs_grid.emplace(obstacles[i][0],temp);
            }
        }
        // print_obs_grid(obs_grid);
        
        
        pose rob_pose;
        rob_pose.x = 0;
        rob_pose.y = 0;
        rob_pose.dir[0] = 0;
        rob_pose.dir[1] = 1; // Facing north +Y axis
        // Execute all commands
        for (size_t i=0; i<commands.size(); ++i){
            // If direction change
            if(commands[i]==-2){
                // std::cout<< "Turn left\n";
                apply_transform(rob_pose.dir,90);
                continue;
            }
            if (commands[i]==-1){
                // std::cout<< "Turn right\n";
                apply_transform(rob_pose.dir,-90);
                continue;
            }
            
            // If no direction change then position change
            if (obs_grid.size()>0){
                // std::cout<< "Checking if path has obstacles\n";
                for (size_t j=1; j<=commands[i]; ++j){
                    rob_pose.x += rob_pose.dir[0];
                    rob_pose.y += rob_pose.dir[1];
                    // std::cout<< "Moving to: " << rob_pose.x << " " << rob_pose.y << "\n";
                    if (obs_grid.count(rob_pose.x)>0){ // If x coordinate is present in the map
                        temp = obs_grid.find(rob_pose.x)->second;
                        if (temp.count(rob_pose.y)>0){
                            // std::cout<< "Obstacle detected!\n";
                            rob_pose.x -= rob_pose.dir[0];
                            rob_pose.y -= rob_pose.dir[1];
                            break;
                        }
                    }
                }
            }
            else{
                rob_pose.x += rob_pose.dir[0]*commands[i];
                rob_pose.y += rob_pose.dir[1]*commands[i];
            }
        }
        return (pow( rob_pose.x,2 )+pow( rob_pose.y,2 ));
    }
};