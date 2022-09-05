#include "traceroute.h"

int main(int argc, char *argv[])
{

    if(!is_valid(argc))
        return 0;


	int sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);


	if (sockfd < 0) {
		fprintf(stderr, "socket error: %s\n", strerror(errno));
		return 0;
	}

	struct sockaddr_in sender;

	sender.sin_port = htons(0);
  	sender.sin_family = AF_INET;
  	if(inet_pton(AF_INET, argv[1], &(sender.sin_addr))==0){
		printf("Blad\n");
		return 0;
	}

	int id = getpid();
    int max_ttl = 50;

	for(int i=1; i<max_ttl; i++){
		struct in_addr responses[3];
		int timer = 0;
		int number_of_response = 0;
		if(send_packets(sockfd, i, id, sender)<0){
            return 0;
		}
		int end = listening(sockfd, i, id, &number_of_response, &timer, responses);
		if(end<0){
            return 0;
		}

        if(i<10) printf(" ");

        printf(" %d.\t", i);

        char first[16], second[16], third[16];
        inet_ntop(AF_INET, &(responses[0]),first,sizeof(first));
        inet_ntop(AF_INET, &(responses[1]),second,sizeof(second));
        inet_ntop(AF_INET, &(responses[2]),third,sizeof(third));

        if(number_of_response == 0) printf("*");
        else{
            printf("%s", first);
            if(strcmp(first,second)!=0 && number_of_response>1){
                printf(" %s", second);
            }
            if(strcmp(first,third)!=0 && strcmp(second,third)!=0 && number_of_response>2) {
                printf(" %s", third);
            }

            if(timer<0) printf("\t???");
            else printf("\t%dms", timer);
        }

		if(end) break;
		printf("\n");
	}
	return 0;
}
