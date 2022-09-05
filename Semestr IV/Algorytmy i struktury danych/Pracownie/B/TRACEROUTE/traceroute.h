#ifndef traceroute_h
#define traceroute_h
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

//Pobieranie pid procesu
pid_t getpid(void);
bool is_valid(int argc);

int send_packets(int sockfd, int ttl, int pid, struct sockaddr_in addr);

//Odbieranie
int get_one_respond(int sockfd, int ttl, int id, struct in_addr addr);
int listen(int sockfd, int ttl, int id, int *number_of_response, int *timer, struct in_addr *responses);

//Funkcja z wykładu - suma kontrolna
u_int16_t compute_icmp_checksum (const void *buff, int length);

#endif
