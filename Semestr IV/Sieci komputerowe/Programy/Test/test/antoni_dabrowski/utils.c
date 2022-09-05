#include "router.h"

//Antoni Dabrowski
//Nr indeksu 317214


node* import_configs(){
    char icmp_addr[20],d[20],ip[20];
    uint32_t distance;

    char mask[3];
    scanf("%s",icmp_addr);
    scanf("%s",d);
    scanf("%u",&distance);

    // Converting IP
    bool still_ip = true;
    int last;
    for(long unsigned int i=0;i<strlen(icmp_addr);i++){
        if(icmp_addr[i]=='/'){
            still_ip = false;
            ip[i] = '\0';
            i++;
            last = i;
        }
        if(still_ip)
            ip[i]=icmp_addr[i];
        else
            mask[i-last]=icmp_addr[i];
    }
    struct dv_item new_item;

    inet_pton(AF_INET, ip, &(new_item.ip_int));

    strcpy(new_item.ip_str, ip);
    new_item.mask = atoi(mask);
    new_item.via_int = ntohl(new_item.ip_int)|(UINT_MAX>>new_item.mask);

    inet_ntop(AF_INET, &new_item.via_int, new_item.via_str, 20);

    new_item.via_int = htonl(new_item.via_int);

    new_item.turn = 0;
    new_item.distance = distance;
    new_item.default_distance = distance;
    new_item.directly_connected = true;
    node* new_node = NULL;
    new_node = (node*)malloc(sizeof(node));
    new_node->data = new_item;
    return new_node;
}


node* createLinkedList(int n,uint32_t ip_connected_networks[], int masks[]){
    node *head = NULL;
    node *temp = NULL;
    node *p = NULL;

    for(int i=0;i<n;i++){
        temp = (node*)malloc(sizeof(node));
        temp = import_configs();
        temp->next = NULL;

        ip_connected_networks[i] = temp->data.via_int;
        masks[i] = temp->data.mask;

        if(head == NULL){
            head = temp;
        }
        else{
            p = head;
            while(p->next != NULL)
                p = p->next;
            p->next = temp;
        }
    }
    return head;
}

void displayLinkedList(node* head){
    node* p = head;
    while(p!=NULL){
        printf("%s/%d ",p->data.ip_str,p->data.mask);
        if(p->data.distance==UINT_MAX){
            printf("unreachable");
            if(p->data.directly_connected){
                printf(" connected directly\n");
            }
            else{
                printf("\n");
            }
        }
        else{
            if(p->data.directly_connected){
                if((ntohl(p->data.ip_int)|(UINT_MAX>>p->data.mask))!=(ntohl(p->data.via_int)|(UINT_MAX>>p->data.mask)))
                    printf("distance %u via %s\n",p->data.distance,p->data.via_str);
                else{
                    printf("distance %u connected directly\n",p->data.distance);
                }
            }
            else{
                printf("distance %u via %s\n",p->data.distance,p->data.via_str);
            }
        }
        p = p->next;
    }
}

void push_back(node* new_element, node* head){
    node *p = NULL;
    p = head;
    while(p->next != NULL)
        p = p->next;
    p->next = new_element;
    new_element->next = NULL;
}

node* remove_element(node* head, uint32_t via, int mask){
    node *p = head;
    if((ntohl(p->data.via_int)|(UINT_MAX>>mask)) == (ntohl(via)|(UINT_MAX>>mask))){
        return head->next;
    }
    while(p->next != NULL){
        if((ntohl(p->data.via_int)|(UINT_MAX>>mask)) == (ntohl(via)|(UINT_MAX>>mask))){
            p->next = (p->next)->next;
        }
        else
            p = p->next;
    }
    return head;
}


void not_connected(node* head, uint32_t broadcast_ip, int turn){
    node* temp = head;
    uint8_t founded = 0;
    while(temp!=NULL)
    {
        if(!founded && (ntohl(temp->data.ip_int)|(UINT_MAX>>temp->data.mask))==broadcast_ip){
            if(temp->data.distance != UINT_MAX)
                temp->data.turn = turn;
            temp->data.distance = UINT_MAX;
        }
        else if(temp->data.via_int == broadcast_ip){
            if(temp->data.distance != UINT_MAX)
                temp->data.turn = turn;
            temp->data.distance = UINT_MAX;
        }
        temp = temp->next;
    }
}

void set_as_unreachable(node* head, uint32_t via, int mask,int current_turn){
    node* temp = head;
    while(temp!=NULL){
        if((temp->data.via_int==via) && (temp->data.mask==mask)){
            if(temp->data.distance != UINT_MAX)
                temp->data.turn = current_turn;
            temp->data.distance = UINT_MAX;
        }
        temp=temp->next;
    }
}

node* vector_look_up(node* head, int current_turn){
    node* temp = head;
    node* previous = head;
    if((temp->data.distance == UINT_MAX) && (current_turn - temp->data.turn >= 3)){
        if(!temp->data.directly_connected){
            return vector_look_up(temp->next, current_turn);
        }
        else{
            temp->data.via_int = ntohl(temp->data.ip_int)|(UINT_MAX>>temp->data.mask);
            temp->data.via_int = htonl(temp->data.via_int);
            set_as_unreachable(temp->next,temp->data.ip_int,temp->data.mask,current_turn);
        }
    }
    else if((current_turn - temp->data.turn) >= 3){
        temp->data.turn = current_turn;
        temp->data.distance = UINT_MAX;
    }
    if(temp->data.distance > 20){
        if(temp->data.distance != UINT_MAX)
                temp->data.turn = current_turn;
        temp->data.distance = UINT_MAX;
        if(temp->data.directly_connected)
            set_as_unreachable(temp->next,temp->data.ip_int,temp->data.mask,current_turn);
    }
    temp = temp->next;
    while(temp!=NULL){
        if(temp->data.distance > 20){
            if(temp->data.distance!= UINT_MAX)
                temp->data.turn = current_turn;
            temp->data.distance = UINT_MAX;
            if(temp->data.directly_connected)
                set_as_unreachable(temp->next,temp->data.ip_int,temp->data.mask,current_turn);
        }
        if((temp->data.distance != UINT_MAX) && ((current_turn - temp->data.turn) >= 3)){
            temp->data.distance = UINT_MAX;
            temp->data.turn = current_turn;
            if(temp->data.directly_connected)
                set_as_unreachable(temp->next,temp->data.ip_int,temp->data.mask,current_turn);

        }
        if((temp->data.distance == UINT_MAX) && ((current_turn - temp->data.turn) >= 3)){
            if(!temp->data.directly_connected){
                previous->next = temp->next;
            }
            else{
                if((ntohl(temp->data.via_int)|(UINT_MAX>>temp->data.mask))!=(ntohl(temp->data.ip_int)|(UINT_MAX>>temp->data.mask))){
                    temp->data.via_int = ntohl(temp->data.ip_int)|(UINT_MAX>>temp->data.mask);
                    temp->data.via_int = htonl(temp->data.via_int);
                }
                set_as_unreachable(temp->next,temp->data.ip_int,temp->data.mask,current_turn);
            }
        }
        temp = temp->next;
        previous = previous->next;
    }
    return head;
}
