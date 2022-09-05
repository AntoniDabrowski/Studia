#include <iostream>

using namespace std;

void merge_arrays(int arr[], int l, int m, int r)
{
    int n1 = m - l + 1;
    int n2 = r - m;

    int L[n1], R[n2];

    for (int i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    int i = 0;

    int j = 0;

    int k = l;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        }
        else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

void mergeSort(int arr[],int l,int r){
    if(l>=r){
        return;//returns recursively
    }
    int m =l+ (r-l)/2;
    mergeSort(arr,l,m);
    mergeSort(arr,m+1,r);
    merge_arrays(arr,l,m,r);
}




int main()
{
    int n;
    int sum=0;
    cin >> n;
    int L[n];
    for(int i=0;i<n;i++){
        cin >> L[i];
        sum+=L[i];
    }
    mergeSort(L,0,n-1);
    int arr[2][sum+1];
    for(int j=0;j<=sum;j++){
        arr[0][j]=0;
        arr[1][j]=0;
    }

    int max_dist=0;
    int current = 0;
    int temp_dist = 0;
    int element;
    for(int j=0;j<n;j++){
        element = L[j];
        temp_dist = 0;
        for(int i=0;i<=min(max_dist+element,sum);i++){
            if(i==0 || (i + element <= sum && arr[abs(current-1)][i + element] != 0)){
               arr[current][i] = max(max(arr[current][i], arr[abs(current - 1)][i]), arr[abs(current - 1)][i + element]);
                temp_dist = max(temp_dist, i);
            }
            if(i-element==0 || (i - element > 0 && arr[abs(current-1)][i - element] != 0)){
                arr[current][i] = max(max(arr[current][i],arr[abs(current-1)][i]),arr[abs(current-1)][i - element]+element);
                temp_dist = max(temp_dist, i);
            }
            if(i - element < 0 && arr[abs(current-1)][abs(i-element)]!=0){
                arr[current][i] = max(max(arr[current][i],arr[abs(current-1)][i]),arr[abs(current-1)][abs(i-element)]-abs(i-element)+element);
                temp_dist = max(temp_dist, i);
            }
            arr[current][i] = max(arr[current][i],arr[abs(current-1)][i]);
        }
        max_dist = max(max_dist, temp_dist);
        current = abs(current - 1);
    }
    current = abs(current - 1);

    if(arr[current][0]!=0){
        cout << "TAK\n"<<arr[current][0];
        return 0;
    }


    for(int i=1;i<=sum;i++){
        if(arr[current][i]-i!=0 && arr[current][i]!=0){
            cout<<"NIE\n"<<i;
            return 0;
        }
    }
}
