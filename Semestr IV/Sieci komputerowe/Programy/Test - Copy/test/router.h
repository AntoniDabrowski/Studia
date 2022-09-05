#ifndef router_h
#define router_h

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <arpa/inet.h>
#include <limits.h>
#include <unistd.h>
#include <errno.h>
#include <assert.h>
#include <sys/select.h>

struct dv_item{
    uint32_t ip_int;
    char ip_str[20];
    int mask;
    uint32_t via_int;
    char via_str[20];
    int turn;
    uint32_t distance;
    uint32_t default_distance;
    bool directly_connected;
};


typedef struct node{
    struct dv_item data;
    struct node *next;
}node;


//utils
node* import_configs();

node* createLinkedList(int n,uint32_t ip_connected_networks[], int masks[]);

void displayLinkedList(node* head, int current_turn);

void push_back(node* new_element, node* head);

node* remove_element(node* head, uint32_t via, int mask);

void not_connected(node* head, uint32_t ip_connected_network, int turn);

node* vector_look_up(node* head, int current_turn);

//send
int send_packet(uint32_t sender_ip_str, uint8_t reply[], int sockfd);

int create_packets(uint8_t packets[][9], node* head);

//recive
void recive_packet(int sockfd, uint32_t ip_broadcast[], int masks[],int n, node* head,int turn);

void handle_recived_packet(uint8_t packet[9], uint32_t packet_via_int, int additional_distance, node* head,
    int current_turn);

#endif // router_h
