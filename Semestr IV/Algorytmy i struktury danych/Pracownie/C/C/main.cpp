#include <iostream>
#include <cmath>
#include <vector>
#include <bits/stdc++.h>

using namespace std;

vector<uint16_t> convert_to_num(int p){
    string s1,s2,s3;
    uint16_t current_num;
    vector<uint16_t> tab(p,0);
    for(int i=0;i<p;i++){
        cin >> s1 >> s2 >> s3;
        current_num=(s1[0]=='x')*4+(s2[0]=='x')*2+(s3[0]=='x');
        current_num=current_num<<5;
        current_num+=(s1[1]=='x')*4+(s2[1]=='x')*2+(s3[1]=='x');
        current_num=current_num<<5;
        current_num+=(s1[2]=='x')*4+(s2[2]=='x')*2+(s3[2]=='x');
        current_num=current_num<<2;
        tab[i]=current_num;
    }
    sort(tab.begin(), tab.end());
    if(p>1){
        vector<uint16_t> unique_tab;
        unique_tab.push_back(tab[0]);
        for(int i=1;i<p;i++){
            if(tab[i]!=tab[i-1]){
                unique_tab.push_back(tab[i]);
            }
        }
        return unique_tab;
    }
    else
        return tab;
}

bool is_good(int num, vector<uint16_t> tab){
    for(auto x:tab)
        if((num&0b0111001110011100)==x || (num&0b0011100111001110)<<1==x || (num&0b0001110011100111)<<2==x)
            return false;
    return true;
}

pair<vector<uint32_t>, vector<bool>> initalization(vector<uint16_t> restirctions){
    vector<uint32_t> num(1024,0);
    vector<bool> adjencity(pow(2,15),0);
    for(uint16_t i=0;i<pow(2,15);i++){
        if(is_good(i,restirctions)){
            num[i&0b0000001111111111]++;
            adjencity[i]=true;
        }
    }
    return make_pair(num,adjencity);
}

vector<uint32_t> add_columns(vector<uint32_t> num, vector<bool> adjencity, int n, int m){
    vector<uint32_t> new_num(1024,0);
    for(int i=0;i<n-3;i++){
        for(uint16_t y=0;y<pow(2,15);y++){
            if(adjencity[y])
                new_num[y&0b0000001111111111]+=num[y>>5];
        }
        for(int y=0; y<1024; y++){
            if(new_num[y]>=m)
                num[y]=new_num[y]%m;
            else
                num[y]=new_num[y];
            new_num[y]=0;
        }
    }
    return num;
}

int final_sum(vector<uint32_t> num, int m){
    uint32_t sum=0;
    for(int i=0;i<1024;i++){
        sum+=num[i];
        if(sum>=m)
            sum=sum%m;
    }
    return sum;
}

int alg(vector<uint16_t> restirctions,int n,int m){
    auto [num, adjencity] = initalization(restirctions);
    num = add_columns(num, adjencity, n, m);
    return final_sum(num,m);
}

int main()
{
    int n, p, m;
    cin >> n;
    cin >> p;
    cin >> m;
    vector<uint16_t> restirctions;
    restirctions = convert_to_num(p);
    cout << alg(restirctions,n,m);


    return 0;
}
