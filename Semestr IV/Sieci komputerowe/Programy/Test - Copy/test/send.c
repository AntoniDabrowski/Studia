#include "router.h"

int send_packet(uint32_t destination, uint8_t reply[], int sockfd){
    struct sockaddr_in 	sender;
    socklen_t 			sender_len = sizeof(sender);
    sender.sin_family      = AF_INET;
    sender.sin_port=htons(54321);
    sender.sin_addr.s_addr = destination;
    //sender->sin_addr.s_addr = ntohl(sender->sin_addr.s_addr);
    //sender->sin_addr.s_addr = 16885952;
    if (sendto(sockfd, reply, 9, 0, (struct sockaddr*)&sender, sender_len) == -1) {
        return 1;
    }
    fflush(stdout);
    return 0;
}

int create_packets(uint8_t packets[][9], node* head){
    int i = 0;
    node* temp = head;
    while(temp!=NULL){
        uint32_t a = ntohl(temp->data.ip_int)|(UINT_MAX>>temp->data.mask);
        char b[20];
        a = htonl(a);
        inet_ntop(AF_INET, &a, b, 20);
        //printf("\nPacket: %s/%d distance %u",b,temp->data.mask,temp->data.distance);
        packets[i][3] = (temp->data.ip_int)>>24;
        packets[i][2] = ((temp->data.ip_int)<<8)>>24;
        packets[i][1] = ((temp->data.ip_int)<<16)>>24;
        packets[i][0] = ((temp->data.ip_int)<<24)>>24;
        packets[i][4] = temp->data.mask;
        //printf("\nSENDING DISTANCE  %u",head->data.distance);
        packets[i][5] = (temp->data.distance)>>24;
        packets[i][6] = ((temp->data.distance)<<8)>>24;
        packets[i][7] = ((temp->data.distance)<<16)>>24;
        packets[i][8] = ((temp->data.distance)<<24)>>24;
        i++;
        temp = temp->next;
    }
    return i;
}
