#include "traceroute.h"


int send_packets(int sockfd, int ttl, int pid, struct sockaddr_in addr){
	struct icmp packet;
	packet.icmp_type = ICMP_ECHO;
	packet.icmp_code = 0;
	packet.icmp_id = pid;
	packet.icmp_seq = ttl;
	packet.icmp_cksum = 0;
	packet.icmp_cksum = compute_icmp_checksum((u_int16_t*)&packet, sizeof(packet));

	setsockopt(sockfd, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl));

    for(int i=0; i<3; i++){
        if (sendto(sockfd, &packet, sizeof(packet), 0, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            fprintf(stderr, "sendto error: %s\n", strerror(errno));
            return -1;
        }
    }
	return 0;
}
