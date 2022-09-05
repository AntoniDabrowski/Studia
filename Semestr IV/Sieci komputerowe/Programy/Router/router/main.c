#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>



void importDataFromUser(long unsigned int routingTable[][12],int numOfAdjacentNetwork){
    char icmp[18],d[20];
    int distance;
    int currentPosition, currentByte, positionInByte;

    for(int i=0;i<numOfAdjacentNetwork;i++){
        char mask[2] = "  ";
        scanf("%s",icmp);
        scanf("%s",d);
        scanf("%d",&distance);

        currentPosition = 0;
        currentByte = 0;
        // Converting IP
        while(currentByte!=4){
            char oneByte[3] = "   ";
            positionInByte = 0;
            while(icmp[currentPosition]!='.'&&icmp[currentPosition]!='/'){
                oneByte[positionInByte]=icmp[currentPosition];
                positionInByte++;
                currentPosition++;
            }
            routingTable[i][currentByte] = atoi(oneByte);
            currentPosition++;
            currentByte++;
        }
        for(int j=currentPosition;j<strlen(icmp);j++){
            mask[j%currentPosition]=icmp[j];
        }
        routingTable[i][4]=atoi(mask);
        routingTable[i][5]=distance;
        routingTable[i][6]=-1; // directly connected
        routingTable[i][7]=-1; // directly connected
        routingTable[i][8]=-1; // directly connected
        routingTable[i][9]=-1; // directly connected
        routingTable[i][10]=0; // current round
        routingTable[i][11]=distance; // default distance
    }
}

void printTable(long unsigned int routingTable[][12],int numOfRecords,int currentRound, int roundLimit){
    for(int i=0;i<numOfRecords;i++){
        if(i!=0)
            printf("\n");
        if(currentRound-routingTable[i][10]<roundLimit){
            if(routingTable[i][5]!=UINT_MAX || routingTable[i][11]!=0){
                printf("%lu.%lu.%lu.%lu/%lu", routingTable[i][0], routingTable[i][1], routingTable[i][2], routingTable[i][3],routingTable[i][4]);
                if(routingTable[i][5]!=UINT_MAX){
                    printf(" distance %lu",routingTable[i][5]);
                }
                else{
                    printf(" unreachable");
                }
                if(routingTable[i][6]==-1){
                    printf(" connected directly");
                }
                else{
                    printf(" via %lu.%lu.%lu.%lu", routingTable[i][6], routingTable[i][7], routingTable[i][8], routingTable[i][9]);
                }
            }
            else{
                printf("%lu.%lu.%lu.%lu/%lu", routingTable[i][0], routingTable[i][1], routingTable[i][2], routingTable[i][3],routingTable[i][4]);
                printf(" unreachable");
            }
        }
    }
}

int update_table(long unsigned int routingTable[][12],int numOfRecords, int destinationNetwork[5],int reciveFromNetwork[5],
                  int senderIP[5], int dist, int currentRound){
    int newRecord = 1;

    for(int i=0;i<numOfRecords;i++){
        if(reciveFromNetwork[0]==routingTable[i][0] && reciveFromNetwork[1]==routingTable[i][1] && reciveFromNetwork[2]==routingTable[i][2]
            && reciveFromNetwork[3]==routingTable[i][3] && reciveFromNetwork[4]==routingTable[i][4]){
            if(routingTable[i][5]!=UINT_MAX){
                if(dist!=UINT_MAX){
                    dist = dist + routingTable[i][5];
                }
                routingTable[i][10] = currentRound;
                routingTable[i][5] = routingTable[i][11];
                i = numOfRecords;
            }
        }
    }


    for(int i=0;i<numOfRecords;i++){
        if(destinationNetwork[0]==routingTable[i][0] && destinationNetwork[1]==routingTable[i][1] && destinationNetwork[2]==routingTable[i][2]
            && destinationNetwork[3]==routingTable[i][3] && destinationNetwork[4]==routingTable[i][4]){
            newRecord = 0;
            if(dist==UINT_MAX){
                if(senderIP[0]==routingTable[i][6] && senderIP[1]==routingTable[i][7] && senderIP[2]==routingTable[i][8]
                    && senderIP[3]==routingTable[i][9]){
                    routingTable[i][5] = UINT_MAX;
                    routingTable[i][6] = UINT_MAX;
                    routingTable[i][7] = UINT_MAX;
                    routingTable[i][8] = UINT_MAX;
                    routingTable[i][9] = UINT_MAX;
                    routingTable[i][10] = currentRound;
                }
            }
            else{
                if(routingTable[i][5]>dist){
                    routingTable[i][5] = dist;
                    routingTable[i][6] = senderIP[0];
                    routingTable[i][7] = senderIP[1];
                    routingTable[i][8] = senderIP[2];
                    routingTable[i][9] = senderIP[3];
                    routingTable[i][10] = currentRound;
                }
            }
        }
        if(routingTable[i][5]>30 && routingTable[i][5]!=UINT_MAX){
            routingTable[i][5] = UINT_MAX;
            routingTable[i][6] = UINT_MAX;
            routingTable[i][7] = UINT_MAX;
            routingTable[i][8] = UINT_MAX;
            routingTable[i][9] = UINT_MAX;
            routingTable[i][10] = currentRound;
        }
    }
    if(newRecord){
        routingTable[numOfRecords][0]=destinationNetwork[0];
        routingTable[numOfRecords][1]=destinationNetwork[1];
        routingTable[numOfRecords][2]=destinationNetwork[2];
        routingTable[numOfRecords][3]=destinationNetwork[3];
        routingTable[numOfRecords][4]=destinationNetwork[4];
        routingTable[numOfRecords][5]=dist;
        routingTable[numOfRecords][6]=senderIP[0];
        routingTable[numOfRecords][7]=senderIP[1];
        routingTable[numOfRecords][8]=senderIP[2];
        routingTable[numOfRecords][9]=senderIP[3];
        routingTable[numOfRecords][10]=currentRound;
        routingTable[numOfRecords][11]=0;
        numOfRecords++;
    }
    return numOfRecords;
}

int create_packets(long unsigned int routingTable[][12],unsigned char toSend[][9],int numOfRecords,int currentRound, int roundLimit){
    int counter = 0;
    for(int i=0;i<numOfRecords;i++){
        if(currentRound-routingTable[i][10]<roundLimit){
            toSend[counter][0]=routingTable[i][0];
            toSend[counter][1]=routingTable[i][1];
            toSend[counter][2]=routingTable[i][2];
            toSend[counter][3]=routingTable[i][3];
            toSend[counter][4]=routingTable[i][4];
            toSend[counter][5]=routingTable[i][5]&0b00000000000000000000000011111111;
            toSend[counter][6]=(routingTable[i][5]&0b00000000000000001111111100000000)>>8;
            toSend[counter][7]=(routingTable[i][5]&0b00000000111111110000000000000000)>>16;
            toSend[counter][8]=(routingTable[i][5]&0b11111111000000000000000000000000)>>24;
            printf("\nTest: %hhu",toSend[counter][5]);
            printf("\nTest: %hhu",toSend[counter][6]);
            printf("\nTest: %hhu",toSend[counter][7]);
            printf("\nTest: %hhu\n",toSend[counter][8]);
            counter++;
        }
    }
    return counter;
}

int main()
{
    int numOfAdjacentNetwork;
    scanf("%d",&numOfAdjacentNetwork);

    const int maxSize = 100;
    long unsigned int routingTable[maxSize][12];
    unsigned char toSend[maxSize][9];
    importDataFromUser(routingTable,numOfAdjacentNetwork);
    int numOfRecords = numOfAdjacentNetwork;

    int roundLimit = 3;
    int numOfPackets;
    int dist;
    int senderIP[4];
    int reciveFromNetwork[5];
    int destinationNetwork[5];
    int currentRound = 0;



    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockfd < 0) {
		fprintf(stderr, "socket error: %s\n", strerror(errno));
		return EXIT_FAILURE;
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


	for (;;) {
        // printing routing table
        printTable(routingTable,numOfAdjacentNetwork,currentRound,roundLimit)

        // recive
        struct timeval time;
        time.tv_sec = 30;
        time.tv_usec = 0;
        do{
            struct sockaddr_in 	sender;
            socklen_t 			sender_len = sizeof(sender);
            u_int8_t 			buffer[IP_MAXPACKET+1];

            fd_set descriptors;
            FD_ZERO(&descriptors);
            FD_SET(socket_fd, &descriptors);
            int ready = select(socket_fd+1, &descriptors, NULL, NULL, &time);
            if (ready < 0) {
                fprintf(stderr, "select() error: %s\n", strerror(errno));
                exit(EXIT_FAILURE);
            }
            ssize_t datagram_len = recvfrom (sockfd, buffer, IP_MAXPACKET, 0, (struct sockaddr*)&sender, &sender_len);
            if (datagram_len < 0) {
                fprintf(stderr, "recvfrom error: %s\n", strerror(errno));
                return EXIT_FAILURE;
            }

            char sender_ip_str[20];
            inet_ntop(AF_INET, &(sender.sin_addr), sender_ip_str, sizeof(sender_ip_str));
            printf ("Received UDP packet from IP address: %s, port: %d\n", sender_ip_str, ntohs(sender.sin_port));

            buffer[datagram_len] = 0;
            printf ("%ld-byte message: +%s+\n", datagram_len, buffer);
        }while(ready!=TIMEOUT)

        // send
        numOfPackets = create_packets(routingTable,toSend,numOfRecords,currentRound,roundLimit);
        for(int i=0;i<numOfPackets;i++){
            char reply[9] = toSend[i];
            ssize_t reply_len = strlen(&reply);
            if (sendto(sockfd, &reply, reply_len, 0, (struct sockaddr*)&sender, sender_len) != reply_len) {
                fprintf(stderr, "sendto error: %s\n", strerror(errno));
                return EXIT_FAILURE;
            }
        }
		fflush(stdout);
	}
	close (sockfd);

























    //printTable(routingTable,numOfAdjacentNetwork);
    int i = 0;
    int roundLimit = 3;
    int numOfPackets;
    int dist;
    int senderIP[4];
    int reciveFromNetwork[5];
    int destinationNetwork[5];
    int currentRound = 0;
    while(1){
        currentRound = i;
        printf("\n");
        // Handeling przychodzących pakietów
        int destinationNetwork[5];
        scanf("%d",&destinationNetwork[0]);
        scanf("%d",&destinationNetwork[1]);
        scanf("%d",&destinationNetwork[2]);
        scanf("%d",&destinationNetwork[3]);
        scanf("%d",&destinationNetwork[4]);

        scanf("%d",&reciveFromNetwork[0]);
        scanf("%d",&reciveFromNetwork[1]);
        scanf("%d",&reciveFromNetwork[2]);
        scanf("%d",&reciveFromNetwork[3]);
        scanf("%d",&reciveFromNetwork[4]);

        scanf("%d",&senderIP[0]);
        scanf("%d",&senderIP[1]);
        scanf("%d",&senderIP[2]);
        scanf("%d",&senderIP[3]);

        scanf("%d",&dist);
        int numOfRecords = numOfAdjacentNetwork;

        numOfAdjacentNetwork = update_table(routingTable,numOfRecords,destinationNetwork,reciveFromNetwork,senderIP,dist,currentRound);

        if(i%3==0){
            numOfPackets = create_packets(routingTable,toSend,numOfRecords,currentRound,roundLimit);
            printf("\nPackets:\n");
            for(int j=0;j<numOfPackets;j++){
//                printf("%hhu.%hhu.%hhu.%hhu/%hhu dist ",toSend[j][0],toSend[j][1],toSend[j][2],toSend[j][3],toSend[j][4]);
//                printf("%hhu %hhu %hhu %hhu\n",toSend[j][5],toSend[j][6],toSend[j][7],toSend[j][8]);
                printf("%s\n",toSend[j]);
            }
        }
        i++;
        printTable(routingTable,numOfAdjacentNetwork,currentRound,roundLimit);
        printf("\nRound %d \n",i);
    }


    printf("\nHello world!\n");
    return 0;
}
