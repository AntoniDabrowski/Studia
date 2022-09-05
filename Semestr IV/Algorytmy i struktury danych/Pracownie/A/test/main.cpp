#include <iostream>
#include <math.h>
#include <bits/stdc++.h>
#include <tuple>

using namespace std;


void merge(unsigned int arr_1[], unsigned long long int arr_2[], int l, int m, int r)
{
    int n1 = m - l + 1;
    int n2 = r - m;

    int L[n1], R[n2];
    unsigned long long int L_2[n1], R_2[n2];

    for (int i = 0; i < n1; i++)
    {
        L[i] = arr_1[l + i];
        L_2[i] = arr_2[l + i];
    }
    for (int j = 0; j < n2; j++)
    {
        R[j] = arr_1[m + 1 + j];
        R_2[j] = arr_2[m + 1 + j];
    }
    int i = 0;

    int j = 0;

    int k = l;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr_1[k] = L[i];
            arr_2[k] = L_2[i];
            i++;
        }
        else {
            arr_1[k] = R[j];
            arr_2[k] = R_2[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr_1[k] = L[i];
        arr_2[k] = L_2[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr_1[k] = R[j];
        arr_2[k] = R_2[j];
        j++;
        k++;
    }
}

void mergeSort(unsigned int arr_1[],unsigned long long int arr_2[],int l,int r){
    if(l>=r){
        return;
    }
    int m = l+ (r-l)/2;
    mergeSort(arr_1,arr_2,l,m);
    mergeSort(arr_1,arr_2,m+1,r);
    merge(arr_1,arr_2,l,m,r);
}

tuple<unsigned int, unsigned int> separete(unsigned int d)
{
    unsigned int prefix;
    unsigned int suffix = 0;
    string binary = bitset<64>(d).to_string();
    int len = binary.length();
    bool terminate = false;
    bool first_loop = true;
    bool was_one = false;
    while (!terminate)
    {
        len-=1;
        if (binary[len]=='0')
        {
            suffix++;
            binary.pop_back();
        }
        else
            terminate = true;

    }

    prefix = bitset<64>(binary).to_ulong();
    return {prefix, suffix};
}

unsigned int countBits(unsigned long long int n)
{
    unsigned int count = 0;
    while (n){
        count += n & 1;
        n >>= 1;
    }
    return count;
}

int main()
{
    unsigned int m=pow(10,6);
    unsigned long long int d,nd;

    //cin >> m;

    unsigned int D[m];
    unsigned long long int N_d[m];

    for(int i=0;i<m;i++)
    {
        d = 275604541-i-(i*i)%13;
        nd = pow(10,9);
        //cin >> d >> nd;
        auto [prefix, suffix] = separete(d);
//        cout<<endl<<bitset<64>(prefix).to_string()<<" "<<suffix<<endl;
        D[i] = prefix;
        N_d[i] = nd * int(pow(2,suffix));
//        cout<<endl<<bitset<64>(N_d[0]).to_string()<<endl;
    }

    mergeSort(D,N_d, 0, m - 1);

    unsigned int counter = 0;
    unsigned long long int coresponding_prefix_counter = N_d[0];
  //  cout << endl << bitset<64>(coresponding_prefix_counter).to_string() << endl;
    for(int i=1;i<m;i++)
    {
        if(D[i-1]==D[i])
        {
            coresponding_prefix_counter+=N_d[i];
        }
        else
        {
            counter += countBits(coresponding_prefix_counter);
            coresponding_prefix_counter = N_d[i];
        }
    }
    counter += countBits(coresponding_prefix_counter);
    cout << counter;
    return 0;
}
