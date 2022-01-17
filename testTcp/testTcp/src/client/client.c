#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


#define MAXLINE 80
#define SERV_PORT 6666
#define TEST_STR "zzcc88b"
#define CROSS_COMPILE_DEBUG 1

#if CROSS_COMPILE_DEBUG == 1
int main(void)
#else
int main(int argc, char* argv[])
#endif
{
	struct sockaddr_in servaddr;
	char buf[MAXLINE];
	int sockfd, n;
	char *str;
#if CROSS_COMPILE_DEBUG ==1
	if (0) 
#else
	if (argc != 2)
#endif
	{
		fputs("usage: ./client message\n", stderr);
		exit(1);
	}
#if CROSS_COMPILE_DEBUG ==1
	str = TEST_STR;
#else
	str = argv[1];
#endif
	sockfd = socket(AF_INET, SOCK_STREAM, 0);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	inet_pton(AF_INET, "127.0.0.1", &servaddr.sin_addr);
	servaddr.sin_port = htons(SERV_PORT);

	connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));

	write(sockfd, str, strlen(str));

	n = read(sockfd, buf, MAXLINE);	
	printf("Response from server:\n");
	write(STDOUT_FILENO, buf, n);
	printf("\n");
	close(sockfd);

	return 0;
}

