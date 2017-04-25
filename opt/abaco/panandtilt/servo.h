#ifdef WIN32
#include <windows.h> 
#else // Assume LINUX
#include <unistd.h>
#endif
#include <string>


class Servo 
{
public:
  void init_serial(char *port);
  int write_serial(void *data, int size);
  void close_serial(void);
private:
#ifdef WIN32
  HANDLE hComm;
#else
  int comport;
#endif
};
