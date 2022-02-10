src = $(wildcard *.c ./client/*.c ./server/*.c)
obj = $(patsubst %.c, %.o, $(src))

all: 	server client
	@echo "getting start..."
	@echo $(src)
	@echo $(obj)
	

server: ./server/server.o wrap.o
	gcc ./server/server.o wrap.o -o ./server/server -Wall
client: ./client/client.o wrap.o
	gcc ./client/client.o wrap.o -o ./client/client -Wall

%.o: ./%c
	gcc -c $< -Wall
./client/%.o: ./client/%.c ./%c
	gcc -c $< -Wall
./server/%.o: ./server/%.c ./%c
	gcc -c $< -Wall


.PHONY: clean all
clean: 
	-rm ./server/server ./client/client $(obj)
