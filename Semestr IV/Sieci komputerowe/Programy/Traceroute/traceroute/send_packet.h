#ifndef send_packet_h
#define send_packet_h
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <netinet/ip_icmp.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdbool.h>
#include <time.h>
#define assert(expr)
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>

int send_packets(int sockfd, int ttl, int pid, struct sockaddr_in addr);

#endif
