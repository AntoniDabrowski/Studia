#include <iostream>
#include <math.h>
#include <bits/stdc++.h>
#include <tuple>

using namespace std;

void swap(uint32_t* a, uint32_t* b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

void swap(uint64_t* a, uint64_t* b)
{
    int t = *a;
    *a = *b;
    *b = t;
}
/* This function is same in both iterative and recursive*/
int partition(uint64_t arr_1[], uint64_t arr_2[], uint32_t l, uint32_t h)
{
    int x = arr_1[h];
    int i = (l - 1);

    for (int j = l; j <= h - 1; j++) {
        if (arr_1[j] <= x) {
            i++;
            swap(&arr_1[i], &arr_1[j]);
            swap(&arr_2[i], &arr_2[j]);
        }
    }
    swap(&arr_1[i + 1], &arr_1[h]);
    swap(&arr_2[i + 1], &arr_2[h]);
    return (i + 1);
}

/* A[] --> Array to be sorted,
l --> Starting index,
h --> Ending index */
void quickSortIterative(uint64_t arr_1[], uint64_t arr_2[], uint32_t l, uint32_t h)
{
    // Create an auxiliary stack
    int stack[h - l + 1];

    // initialize top of stack
    int top = -1;

    // push initial values of l and h to stack
    stack[++top] = l;
    stack[++top] = h;

    // Keep popping from stack while is not empty
    while (top >= 0) {
        // Pop h and l
        h = stack[top--];
        l = stack[top--];

        // Set pivot element at its correct position
        // in sorted array
        int p = partition(arr_1, arr_2, l, h);

        // If there are elements on left side of pivot,
        // then push left side to stack
        if (p - 1 > l) {
            stack[++top] = l;
            stack[++top] = p - 1;
        }

        // If there are elements on right side of pivot,
        // then push right side to stack
        if (p + 1 < h) {
            stack[++top] = p + 1;
            stack[++top] = h;
        }
    }
}

//--------------------------------------------


void merge(unsigned long long int arr_1[], unsigned long long int arr_2[], int l, int m, int r)
{
    int n1 = m - l + 1;
    int n2 = r - m;

    unsigned long long int L[n1], R[n2];
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

void mergeSort(unsigned long long int arr_1[],unsigned long long int arr_2[],int l,int r,  int depth){
    if(l>=r){
        return;
    }
    int m = l+ (r-l)/2;
//    cout << depth << endl;
    mergeSort(arr_1,arr_2,l,m,depth+1);
    mergeSort(arr_1,arr_2,m+1,r,depth+1);
    merge(arr_1,arr_2,l,m,r);
}

tuple<unsigned int, unsigned int> separete(unsigned int d)
{
    uint32_t prefix;
    uint32_t suffix = 0;
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
    uint32_t m = pow(10,5);
    uint64_t d,nd;
    //cout << sizeof(m);
    //cin >> m;
    uint64_t D[m];
    uint64_t N_d[m];

    for(int i=0;i<m;i++)
    {
        //cin >> d >> nd;
        d = pow(10,9)-i;
        nd = pow(10,9);

        auto [prefix, suffix] = separete(d);
//        cout<<endl<<bitset<64>(prefix).to_string()<<" "<<suffix<<endl;
        D[i] = prefix;
        N_d[i] = nd * int(pow(2,suffix));
//        cout<<endl<<bitset<64>(N_d[0]).to_string()<<endl;
    }

//    mergeSort2(D,N_d, 0, m - 1);
    quickSortIterative(D,N_d, 0, m - 1);
    cout << endl << "Posortowalem" << endl;

    unsigned int counter = 0;
    unsigned long long int coresponding_prefix_counter_first = N_d[0];

//    cout << endl << bitset<64>(coresponding_prefix_counter).to_string() << endl;
    for(int i=1;i<m;i++)
    {
        if(D[i-1]==D[i])
        {
            coresponding_prefix_counter_first+=N_d[i];
        }
        else
        {
            counter += countBits(coresponding_prefix_counter_first);
            coresponding_prefix_counter_first = N_d[i];
        }
//        cout << endl << "Second: " << coresponding_prefix_counter_second << endl;
    }
    counter += countBits(coresponding_prefix_counter_first);
    cout << counter;
    return 0;
}
