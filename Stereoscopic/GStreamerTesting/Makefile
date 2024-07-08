# Compiler
CC := g++
# Compiler flags
CFLAGS := -std=c++11 -Wall
# Libraries required by OpenCV
LIBS := `pkg-config --libs opencv4`
# Include path for OpenCV
INC_PATH1 := -I/System/Volumes/Data/opt/homebrew/var/homebrew/linked/opencv/include/opencv4
INC_PATH2 := -I/home/pi/opencv/include

# Default target
all: 2StreamDisplay.cpp 2StreamSender.cpp

# Target for building the executable
2StreamDisplay: display.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)
2StreamSender: sender.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

# Target for compiling main.cpp into an object file
display.o: 2StreamDisplay.cpp
	$(CC) $(CFLAGS) $(INC_PATH1) $(LIBS) -c -o $@ $<
sender.o: 2StreamSender.cpp
	$(CC) $(CFLAGS) $(INC_PATH2) $(LIBS) -c -o $@ $<

# Target for cleaning up object files and the executable
clean:
	rm -f *.o Single_Pipeline_Test