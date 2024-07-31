# Compiler
CC := g++
# Compiler flags
CFLAGS := -std=c++11 -Wall
# Libraries required by OpenCV
LIBS := `pkg-config --libs opencv4`
# Include path for OpenCV
INC_PATH1 := -I/System/Volumes/Data/opt/homebrew/var/homebrew/linked/opencv/include/opencv4
INC_PATH2 := `pkg-config --cflags opencv4` #-I/usr/include/opencv4

# Default target
all: gstTransTest.cpp

# Target for building the executable
gstTransTest: test.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

# Target for compiling main.cpp into an object file
test.o: gstTransTest.cpp
	$(CC) $(CFLAGS) $(INC_PATH1) $(LIBS) -c -o $@ $<

# Target for cleaning up object files and the executable
clean:
	rm -f *.o gstTransTest