// Antoni Dąbrowski
// 317214
// KLO


#include <iostream>
#include<math.h>

using namespace std;

int main()
{
    unsigned int a, b;
    cin >> a >> b;
    for(int i=ceil(a/2021.0)*2021;i<=b;i+=2021){
        cout << i << " ";
    }
    return 0;
}
