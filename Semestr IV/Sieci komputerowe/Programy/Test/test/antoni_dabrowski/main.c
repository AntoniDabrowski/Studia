#include "router.h"

//Antoni Dabrowski
//Nr indeksu 317214




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

        recive_packet(sockfd,HEAD,turn);
        int number_of_packets = create_packets(packets,HEAD);
        for(int i=0;i<n;i++){
            for(int j=0;j<number_of_packets;j++){
                if(send_packet(ip_broadcast[i], packets[j], sockfd))
                    not_connected(HEAD,ip_broadcast[i],turn);
            }
        }
        printf("\n");
        HEAD = vector_look_up(HEAD, turn);
        displayLinkedList(HEAD);
	}
	close(sockfd);
	return EXIT_SUCCESS;
}
