#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <ctype.h>
#include <sys/select.h>
#include <strings.h>
#include <sys/wait.h>
#include <signal.h>

#define MAXLINE 80
#define SERV_PORT 6666
#define SERV_TIMEOUT_DEFAULT 60 // [s] seconds for the select function time out
#define FD_SETSIZE_USR		32
#define IP_ADDRESS_SERVER "172.27.132.88"
static void sigchldHandler(int);
static void sigpipeHandler(int);
int main(void)
{
	/* define var */
	int listenfd, connfd;
	int maxQueue = FD_SETSIZE_USR;
	char str[INET_ADDRSTRLEN]; 			/* #define INET_ADDRSTRLEN 16 */
	socklen_t cliaddr_len;
	struct sockaddr_in cliaddr, servaddr;	// client & server addr
	pid_t childPid;


	listenfd = Socket(AF_INET, SOCK_STREAM, 0);
	printf("socket number: %d\n", listenfd);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);//htonl(IP_ADDRESS_SERVER);
	servaddr.sin_port = htons(SERV_PORT);

	Bind(listenfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
	showAddr("Binding to address:", &servaddr);
	printf("\n");
	/* listening to connection requests */
	printf("Listening at socket: %d with max queue: %d\t\t", listenfd, maxQueue);
	Listen(listenfd, 128); 		/* 默认最大128 */

	signal(SIGCHLD, sigchldHandler);//initializing signal handler to avoid zombie process
	signal(SIGPIPE, sigpipeHandler);//initializing signal handler to handle broken pipe

	for (; ; )
	{
		cliaddr_len = sizeof(cliaddr);
		connfd = Accept(listenfd, (struct sockaddr*)&cliaddr, &cliaddr_len);
		childPid = fork();
		if (childPid == 0)
		{
			//printf("child process:");
			//child process
			Close(listenfd);
			signal(SIGPIPE, sigpipeHandler);	//initializing signal handler to handle broken pipe
			printf("child process:");
			printf("\n");
			printf("\n");
			printf("Assigning server tasks to process\n\n");
			serviceFunc(connfd, cliaddr);
			exit(0);	// exit child process
		}
		else if (childPid > 0)
		{
			printf("pararent now:");
			close(connfd);	// pararent to close connection
		}
		else
		{
			perr_exit("fork error, program closing...");
		}

	}

	return 0;
}


void serviceFunc(int socketNumber, struct sockaddr_in clientAddr)
{
	int i, maxi, maxfd, sockfd;
	int setsReady, client[FD_SETSIZE]; 	/* FD_SETSIZE默认为 1024 */
	struct sockaddr_in cliaddr;
	ssize_t n;
	fd_set rset, allset;
	char buf[MAXLINE], bufRecv[MAXLINE];	// 读写 buf
	char str[INET_ADDRSTRLEN]; 			// INET_ADDRSTRLEN 16 

	sockfd = socketNumber;
	cliaddr = clientAddr;
	FD_ZERO(&allset);
	FD_SET(sockfd, &allset);

	for (; ; )
	{	
		printf("received from %s at PORT %d\n", \
			inet_ntop(AF_INET, &cliaddr.sin_addr, str, sizeof(str)), ntohs(cliaddr.sin_port));	// 地址和端口号才正真换成正确的
		n = Read(socketNumber, buf, MAXLINE);
		if (n == 0)
		{
			printf("the other side has been closed.\n");
			break;
		}
		for (i = 0; i < n; i++)
			buf[i] = toupper(buf[i]);
		Write(socketNumber, buf, n);
	}
}

//signal handler for SIGCHLD signal
static void sigchldHandler(int signo) {
	pid_t pid;
	int stat;

	//option WNOHANG: if the child is running the caller does not block it
	while ((pid = waitpid(0, &stat, WNOHANG)) > 0) {
		printf("\n");
		printf("-> Server process %d terminated\n\n", pid);
	}
	return;
}


//signal handler for SIGPIPE signal
static void sigpipeHandler(int signo) {
	printf("-> Broken pipe!\n");
	return;
}
