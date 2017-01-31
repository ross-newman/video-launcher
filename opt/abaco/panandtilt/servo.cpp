#include "servo.h"
// Standard includes
#include <iostream>
#include <unistd.h>
// Do nothing
#if WIN32
#else
#include <fcntl.h> //File control
#include <errno.h> //Error number def
#include <termios.h> //POSIX terminal control
#include <termio.h>
#endif

using namespace std;

/*
 * init_serial - Initalize serial data RS232
 */
void Servo::init_serial(char *port)
{
#if WIN32
	string comport = "COM2";
	hComm = CreateFile("COM2",  
			GENERIC_READ | GENERIC_WRITE, 
			0, 
			0, 
			OPEN_EXISTING,
			0,
			0);
	if (hComm == INVALID_HANDLE_VALUE)
	{
		cout << "Error opening COM2!\n";
	}

	//Port Settings
	DCB dcbSerialParams = {0};
	dcbSerialParams.DCBlength=sizeof(dcbSerialParams);
	dcbSerialParams.BaudRate=CBR_9600;
	dcbSerialParams.ByteSize=8;
	dcbSerialParams.StopBits=ONESTOPBIT;
	dcbSerialParams.Parity=NOPARITY;

	SetCommState(hComm,&dcbSerialParams);//Apply Settings to Handle
#else
    struct termios options;

    comport = open(port, O_RDWR);

    if(comport == -1){
      cout << "open_port: Unable to open " << port << "\n";
    }else fcntl(comport, F_SETFL, 0);

    tcgetattr(comport, &options);

    cfsetispeed(&options, B9600); //Typical way of setting baud rate. Actual baud rate are contained in the c_ispeed and c_ospeed members
    cfsetospeed(&options, B9600);

    tcsetattr (comport, TCSANOW, &options);
#endif
}

/*
 * write_serial - Write data to thge serial port
 */
int Servo::write_serial(void *data, int len)
{
#if WIN32
	DWORD written;
    WriteFile(hComm, data, (DWORD)len, &written, NULL);
#else
    return write(comport, data, len);
#endif
}

void Servo::close_serial(void)
{
#if WIN32
	// Close the port again
	CloseHandle(hComm);
#else
    ::close(comport);
#endif
}
