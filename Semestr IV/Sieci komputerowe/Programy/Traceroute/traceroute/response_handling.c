//Antoni Dąbrowski
//nr. indeksu 317214

#include "common_functions.h"

int listening(int sockfd, int ttl, int id, int *number_of_response, int *timer, struct in_addr *responses){

        int is_ok;
        int time=0;
        struct timespec t,st;
        clock_gettime(CLOCK_MONOTONIC, &t);
        int passed_time = 0;

        while(*number_of_response < 3 && passed_time<1000){
                is_ok=get_one_respond(sockfd, ttl, id, responses+*number_of_response);

                if(is_ok<0) return -1;
                if(is_ok!=2) {
                        (*number_of_response)++;
                        time+=passed_time;
                                        }
                clock_gettime(CLOCK_MONOTONIC, &st);
                passed_time = (st.tv_sec - t.tv_sec)*1000 + (st.tv_nsec - t.tv_nsec)/1000000;
        }
        if(*number_of_response<3) *timer = -1;
        else *timer=time/3;

        if(is_ok==1) return true;

        return false;
}
