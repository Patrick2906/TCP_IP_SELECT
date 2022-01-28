#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/select.h>
#include <fcntl.h>

#define MAXLINE 512
#define SERV_PORT 6666
#define IP_ADDRESS_CLIENT "127.0.0.1"
#define CROSS_COMPILE_DEBUG 0
#define CLIENT_TIMEOUT_DEFAULT 10 // £¨s)seconds for the select function time out

clientFunc(int socketNumber, struct sockaddr_in servaddr);
int appGet(char *buffer);

#if CROSS_COMPILE_DEBUG == 1
int main(void)
#else
int main(int argc, char* argv[])
#endif
{
	struct sockaddr_in servaddr;
	int sockfd;
	sockfd = socket(AF_INET, SOCK_STREAM, 0);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	inet_pton(AF_INET, IP_ADDRESS_CLIENT, &servaddr.sin_addr);
	servaddr.sin_port = htons(SERV_PORT);

	char straddr[INET_ADDRSTRLEN];
	
	inet_ntop(AF_INET, &servaddr.sin_addr, straddr, sizeof(straddr));
	printf("Connecting to server address:%s \n", straddr);
	Connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
	printf("server connectted.\n");

	clientFunc(sockfd, servaddr);

	close(sockfd);

	return 0;
}

clientFunc(int socketNumber, struct sockaddr_in servaddr)
{
	char buf[MAXLINE];
	int sockfd, n;
	int setReady;
	fd_set rset;
	struct timeval tval;
	sockfd = socketNumber;

	// select settings
	tval.tv_sec = CLIENT_TIMEOUT_DEFAULT;
	tval.tv_usec = 0;
	FD_ZERO(&rset);
	FD_SET(sockfd, &rset);

	while (appGet(buf) == 0)
	{
		Write(sockfd, buf, strlen(buf));// send out the message

#if CLIENT_TIMEOUT_DEFAULT > 0
		tval.tv_sec = CLIENT_TIMEOUT_DEFAULT;
		tval.tv_usec = 0;
		setReady = Select(sockfd + 1, &rset, NULL, NULL, &tval);
#else
		setReady = Select(sockfd + 1, &rset, NULL, NULL, NULL);
#endif
		if (setReady > 0)
		{
			if (FD_ISSET(sockfd, &rset))
			{
				n = Read(sockfd, buf, MAXLINE);
				if (n == 0)
				{
					printf("The other side has been closed.\n");
					printf("Closing connection...\n");
					break;
				}
				else
				{// print to console
					printf("Read form buffer: \n");
					Write(STDOUT_FILENO, buf, n);
					printf("\n");
				}
			}
		}
		else
		{
			printf("No response received, timeout. Closing connection...\n");
			break;
		}
	}

}

int appGet(char* buffer)
{
	// could be changed from developer
	if (fgets(buffer, MAXLINE, stdin) != NULL)
	{
		return 0;
	}
	else
	{
		return -1;
	}
}