CC = gcc
CFLAGS = -Wall -Wextra -O3 -fPIC
TARGET_LIB = libtree_engine.so
TARGET_WIN = tree_engine.dll

all: $(TARGET_LIB) $(TARGET_WIN)

$(TARGET_LIB): tree_engine.c tree_engine.h
	$(CC) $(CFLAGS) -shared -o $@ tree_engine.c

$(TARGET_WIN): tree_engine.c tree_engine.h
	$(CC) $(CFLAGS) -shared -o $@ tree_engine.c

clean:
	rm -f *.o *.so *.dll
