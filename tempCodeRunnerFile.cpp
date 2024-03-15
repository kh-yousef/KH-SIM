#include <iostream>
#include <random>
#include <queue>
#include <functional>
#include <cstdlib>
#include <ctime>

using namespace std;



int main()
{
    std::priority_queue<int>diceroll;
    srand(time(0));
    for(int i = 1; i <=10; ++i)
    {
        int n = rand() % 6 + 1;
        cout << "roll " << (i) <<": " << n <<  endl;
        
        diceroll.push(n);
    }
    
    cout <<"######################################" << endl;
    for(int i = 0; i < 5; i ++)
    {
        if(!diceroll.empty())
        {
            cout << "removed " << diceroll.top(); 
            cout << endl;
            diceroll.pop();

        }
    }

    while(!diceroll.empty())
    {
        int p = diceroll.top();
        cout << p;
        diceroll.pop();
    }
}




