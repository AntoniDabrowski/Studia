#ifndef response_handling_h
#define response_handling_h
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

int listening(int sockfd, int ttl, int id, int *number_of_response, int *timer, struct in_addr *responses);

#endif

