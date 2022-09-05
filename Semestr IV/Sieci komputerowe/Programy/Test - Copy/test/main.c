#include "router.h"

/*#include <netinet/ip.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <netinet/ip_icmp.h>
#include <sys/select.h>*/




int main(){

    // Prepare socket
	int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockfd < 0) {
		fprintf(stderr, "socket error: %s\n", strerror(errno));
		return EXIT_FAILURE;
	}

    int broadcastEnable=1;
    if(setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcastEnable, sizeof(broadcastEnable)) < 0)
    {
        printf("Error in setting Broadcast option");
        return 0;
    }

	struct sockaddr_in server_address;
	bzero (&server_address, sizeof(server_address));
	server_address.sin_family      = AF_INET;
	server_address.sin_port        = htons(54321);
	server_address.sin_addr.s_addr = htonl(INADDR_ANY);


	if (bind (sockfd, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
		fprintf(stderr, "bind error: %s\n", strerror(errno));
		return EXIT_FAILURE;
	}


    int turn = 0;
    uint8_t packets[100][9];

    //initial configuration of distance vector
    int n = 0;
    node* HEAD = NULL;
    scanf("%d",&n);
    uint32_t ip_broadcast[n];
    int masks[n];
    HEAD = createLinkedList(n,ip_broadcast,masks);


	for (;;) {
        turn++;
        printf("\n\nTura %d",turn);

        recive_packet(sockfd,ip_broadcast,masks,n,HEAD,turn);
        //printf("\n");
        int number_of_packets = create_packets(packets,HEAD);
        for(int i=0;i<n;i++){
            char a[20];
            uint32_t b = ip_broadcast[i];
            inet_ntop(AF_INET, &b, a, 20);
            //printf("\nSend to: %s",a);
            for(int j=0;j<number_of_packets;j++){
                if(send_packet(ip_broadcast[i], packets[j], sockfd))
                    not_connected(HEAD,ip_broadcast[i],turn);
            }
        }
        //printf("\n\n");
        HEAD = vector_look_up(HEAD, turn);
        displayLinkedList(HEAD, turn);
	}
	close(sockfd);
	return EXIT_SUCCESS;
}
