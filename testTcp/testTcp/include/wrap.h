
#ifndef __WRAP_H_
#define __WRAP_H_
#include <stdio.h>
#include <unistd.h>
#include <sys/select.h>

void perr_exit(const char* s);
int Accept(int fd, struct sockaddr* sa, socklen_t* salenptr);
int Bind(int fd, const struct sockaddr* sa, socklen_t salen);
int Connect(int fd, const struct sockaddr* sa, socklen_t salen);
int Listen(int fd, int backlog);
int Socket(int family, int type, int protocol);
ssize_t Read(int fd, void* ptr, size_t nbytes);
ssize_t Write(int fd, const void* ptr, size_t nbytes);
int Close(int fd);
ssize_t Readn(int fd, void* vptr, size_t n);
ssize_t Writen(int fd, const void* vptr, size_t n);
ssize_t my_read(int fd, char* ptr);
ssize_t Readline(int fd, void* vptr, size_t maxlen);
void showAddr(char* str, struct sockaddr_in* a);
void showDebug(void);
int Select(int __nfds, fd_set* __restrict __readfds,
	fd_set* __restrict __writefds,
	fd_set* __restrict __exceptfds,
	struct timeval* __restrict __timeout);
#endif