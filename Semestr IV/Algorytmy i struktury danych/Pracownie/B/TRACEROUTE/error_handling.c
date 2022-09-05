#include "traceroute.h"


bool is_valid(int argc)
{
    bool is_good = true;
	if(argc != 2){
        is_good = false;
		printf("Zla liczba argumentow" );
    }
    return is_good;
}

u_int16_t compute_icmp_checksum (const void *buff, int length){

	u_int32_t sum;
	const u_int16_t* ptr = buff;
	assert (length % 2 == 0);
	for (sum = 0; length > 0; length -= 2)
		sum += *ptr++;

	sum = (sum >> 16) + (sum & 0xffff);
	return (u_int16_t)(~(sum + (sum >> 16)));
}

int get_one_respond(int sockfd, int ttl, int id, struct in_addr *addr)
{
	u_int8_t buffer[IP_MAXPACKET+1];
    int check = recv(sockfd, buffer, IP_MAXPACKET, MSG_DONTWAIT)<0 && (errno != EAGAIN || errno !=  EWOULDBLOCK);
	if(check){
		fprintf(stderr, "Error: %s\n", strerror(errno));
		return -1;
	}

	struct ip *set_ip = (struct ip *)buffer;
	struct icmp *set_icmp = (struct icmp *)((uint8_t *)set_ip + (*set_ip).ip_hl * 4);

	if(set_icmp->icmp_type == ICMP_TIME_EXCEEDED){
		struct ip *temp_ip = (struct ip *)((uint8_t *)set_icmp + 8);
		struct icmp *temp_icmp = (struct icmp *)((uint8_t *)temp_ip + (*temp_ip).ip_hl * 4);
		if(temp_icmp->icmp_seq==ttl && temp_icmp->icmp_id==id){
			*addr=set_ip->ip_src;
			return 0;
		}
	}else if(set_icmp->icmp_type == ICMP_ECHOREPLY && set_icmp->icmp_seq==ttl && set_icmp->icmp_id==id){
		*addr=set_ip->ip_src;
		return 1;
	}

	return 2;
}
