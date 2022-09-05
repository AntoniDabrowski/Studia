#ifndef common_functions_h
#define common_functions_h
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

pid_t getpid(void);
bool is_valid(int argc);
int get_one_respond(int sockfd, int ttl, int id, struct in_addr *addr);
u_int16_t compute_icmp_checksum (const void *buff, int length);

#endif

