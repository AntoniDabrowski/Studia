#include <netinet/ip.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

int main()
{
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

	for (;;) {
        char sender_ip_str[20];
        int sender_ip_str_len = sizeof(sender_ip_str);
        struct sockaddr_in 	sender;
        sender.sin_port=htons(54321);
        socklen_t 			sender_len = sizeof(sender);
        u_int8_t 			buffer[IP_MAXPACKET+1];
        int ready;
        fd_set rfds;
        FD_ZERO(&rfds);
        FD_SET(sockfd, &rfds);
        struct timeval time;
        time.tv_sec = 5;
        time.tv_usec = 0;
        do{
            ready = select(sockfd+1, &rfds, NULL, NULL, &time);
            if (ready < 0) {
                fprintf(stderr, "select() error: %s\n", strerror(errno));
                exit(EXIT_FAILURE);
            }
            else if(ready){
                printf("STH");
                ssize_t datagram_len = recvfrom (sockfd, buffer, IP_MAXPACKET, 0, (struct sockaddr*)&sender, &sender_len);
                if (datagram_len < 0) {
                    fprintf(stderr, "recvfrom error: %s\n", strerror(errno));
                    exit(EXIT_FAILURE);
                }
                inet_ntop(AF_INET, &(sender.sin_addr), sender_ip_str, sender_ip_str_len);
                printf ("Received UDP packet from IP address: %s, port: %d\n", sender_ip_str, ntohs(sender.sin_port));

                buffer[datagram_len] = 0;
                printf ("%ld-byte message: +%s+\n", datagram_len, buffer);
            }
        }while(ready!=0);




		char* reply = "Thank you!";
		ssize_t reply_len = strlen(reply);
		sender.sin_addr.s_addr = 4278298816;//33663168
		printf("%u",sender.sin_addr);
		if (sendto(sockfd, reply, reply_len, 0, (struct sockaddr*)&sender, sender_len) != reply_len) {
			fprintf(stderr, "sendto error: %s\n", strerror(errno));
			return EXIT_FAILURE;
		}

		fflush(stdout);
	}

	close (sockfd);
	return EXIT_SUCCESS;
}
