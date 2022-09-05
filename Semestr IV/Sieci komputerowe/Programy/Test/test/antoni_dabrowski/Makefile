CFLAGS = -std=gnu99 -Wall -W

all: router

router : utils.o recive.o send.o main.o
	gcc -o router utils.o recive.o send.o main.o

main.o: main.c router.h

recive.o : recive.c router.h

send.o : send.c router.h

utils.o : utils.c router.h

clean :
	rm -f utils.o router.o recive.o send.o main.o
distclean :
	rm -f router recive send main utils utils.o router.o recive.o send.o main.o
