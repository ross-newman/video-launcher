OBJS = joystick.o servo.o
CC = g++
DEBUG = -g
CFLAGS = -Wall -c $(DEBUG)  -lSDL2main -lSDL2
LFLAGS = -Wall $(DEBUG) 

all : $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -lSDL2main -lSDL2 -o joystick

clean:
	rm *.o
