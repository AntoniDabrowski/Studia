#include "router.h"

//Antoni Dabrowski
//Nr indeksu 317214


void recive_packet(int sockfd, node* head, int turn){
    struct sockaddr_in 	sender;
    sender.sin_port=htons(54321);
    socklen_t 			sender_len = sizeof(sender);
    u_int8_t 			buffer[9];
    int ready;
    fd_set rfds;
    FD_ZERO(&rfds);
    FD_SET(sockfd, &rfds);
    struct timeval time;
    time.tv_sec = 5;
    time.tv_usec = 0;
    uint32_t recived_from;
    do{
        ready = select(sockfd+1, &rfds, NULL, NULL, &time);
        if (ready < 0) {
            fprintf(stderr, "select() error: %s\n", strerror(errno));
            exit(EXIT_FAILURE);
        }
        else if(ready){
            ssize_t datagram_len = recvfrom (sockfd, buffer, 9, 0, (struct sockaddr*)&sender, &sender_len);
            if (datagram_len < 0) {
                fprintf(stderr, "recvfrom error: %s\n", strerror(errno));
                exit(EXIT_FAILURE);
            }
            recived_from = sender.sin_addr.s_addr;
            //buffer[datagram_len] = 0;
            node* temp = head;
            uint8_t founded = 0;
            while(!founded && temp!=NULL){
                if(temp->data.directly_connected && ((ntohl(temp->data.ip_int)|(UINT_MAX>>temp->data.mask))==(ntohl(recived_from)|(UINT_MAX>>temp->data.mask)))){
                    founded = 1;
                    uint32_t a = recived_from;
                    uint32_t c = ntohl(recived_from)|(UINT_MAX>>temp->data.mask);
                    uint32_t e = ntohl(temp->data.ip_int)|(UINT_MAX>>temp->data.mask);
                    c = htonl(c);
                    char b[20];
                    char d[20];
                    char f[20];
                    inet_ntop(AF_INET, &a, b, 20);
                    inet_ntop(AF_INET, &c, d, 20);
                    inet_ntop(AF_INET, &e, f, 20);
                    handle_recived_packet(buffer,recived_from,temp->data.distance,head,turn);
                }
                temp = temp->next;
            }

        }
    }while(ready!=0);
}


void handle_recived_packet(uint8_t packet[9], uint32_t packet_via_int, int additional_distance, node* head,
    int current_turn){
    node* temp = head;
    uint32_t packet_ip;
    packet_ip = packet[0];
    packet_ip = packet_ip<<8;
    packet_ip += packet[1];
    packet_ip = packet_ip<<8;
    packet_ip += packet[2];
    packet_ip = packet_ip<<8;
    packet_ip += packet[3];
    packet_ip = htonl(packet_ip);
    int packet_mask = packet[4];

    uint32_t t = packet_ip;
    char ip_s[20];
    inet_ntop(AF_INET, &t, ip_s, 20);

    uint32_t packet_distance;
    packet_distance = packet[5];
    packet_distance = packet_distance<<8;
    packet_distance += packet[6];
    packet_distance = packet_distance<<8;
    packet_distance += packet[7];
    packet_distance = packet_distance<<8;
    packet_distance += packet[8];
    if((packet_distance<20)||(packet_distance==UINT_MAX)){
        bool founded = false;
        while(temp!=NULL && !founded){
            if((ntohl(temp->data.ip_int)|(UINT_MAX>>temp->data.mask))==(ntohl(packet_ip)|(UINT_MAX>>temp->data.mask)) && (temp->data.mask == packet_mask)){
                founded = true;
                if(packet_distance==UINT_MAX){
                    set_as_unreachable(head,temp->data.ip_int,temp->data.mask,current_turn);
                }
                if((packet_distance!=UINT_MAX) && (temp->data.distance>packet_distance+additional_distance) && (temp->data.distance!=UINT_MAX)){
                    if(temp->data.directly_connected){
                        remove_element(temp,packet_via_int,temp->data.mask);
                    }
                    temp->data.via_int = packet_via_int;
                    inet_ntop(AF_INET, &packet_via_int, temp->data.via_str, 20);
                    temp->data.turn = current_turn;
                    temp->data.distance = packet_distance + additional_distance;

                }
                else if((temp->data.via_int == packet_via_int) && (temp->data.distance!=UINT_MAX))
                {
                    temp->data.turn = current_turn;
                }
                else if(temp->data.directly_connected && (ntohl(temp->data.via_int)|(UINT_MAX>>temp->data.mask))==(ntohl(packet_via_int)|(UINT_MAX>>temp->data.mask))
                        && (temp->data.distance!=UINT_MAX)){
                    temp->data.via_int = packet_via_int;
                    inet_ntop(AF_INET, &packet_via_int, temp->data.via_str, 20);
                    temp->data.turn = current_turn;
                    temp->data.distance = temp->data.default_distance;
                }
                else if((temp->data.distance==UINT_MAX) && temp->data.directly_connected && (packet_distance!=UINT_MAX)){
                    temp->data.via_int = packet_via_int;
                    inet_ntop(AF_INET, &packet_via_int, temp->data.via_str, 20);
                    temp->data.turn = current_turn;
                    temp->data.distance = packet_distance + additional_distance;
                }
            }
            temp = temp->next;
        }
        if(!founded && (packet_distance!=UINT_MAX)){
            node* new_node = NULL;
            new_node = (node*)malloc(sizeof(node));
            new_node->data.ip_int = packet_ip;
            inet_ntop(AF_INET, &(new_node->data.ip_int), new_node->data.ip_str, 20);
            new_node->data.mask = packet_mask;
            new_node->data.via_int = packet_via_int;
            inet_ntop(AF_INET, &(new_node->data.via_int), new_node->data.via_str, 20);
            new_node->data.turn = current_turn;
            new_node->data.distance = packet_distance + additional_distance;
            new_node->data.default_distance = packet_distance + additional_distance;
            new_node->data.directly_connected = 0;
            push_back(new_node, head);
        }
    }
}
