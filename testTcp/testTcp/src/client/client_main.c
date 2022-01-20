#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "../wrap.h"

#define MAXLINE 80
#define SERV_PORT 6666
//#define TEST_STR "zzcc88b"
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

	sockfd = socket(AF_INET, SOCK_STREAM, 0);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	inet_pton(AF_INET, "127.0.0.1", &servaddr.sin_addr);
	servaddr.sin_port = htons(SERV_PORT);

	connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));


	while (fgets(buf, MAXLINE, stdin) != NULL)
	{
		if (strncmp(buf, "end", 3) == 0)
		{
			// test for lost connection after data sending
			printf("ending script");
			Write(sockfd, "end", 3);
			close(sockfd);
			printf("socket of client is closed");
			exit(1);
		}
		else
		{
			Write(sockfd, buf, strlen(buf));
			n = Read(sockfd, buf, MAXLINE);
			if (n == 0)
			{
				printf("the other side has been closed.\n");
			}
			else
			{
				Write(STDOUT_FILENO, buf, n);
				printf("\n");
			}
		}
	}

	close(sockfd);

	return 0;
}

