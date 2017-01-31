/*
** apt-get install libsdl2-dev
** sudo adduser ubuntu dialout
*/

#include "servo.h"
#include <SDL2/SDL.h>
#include <iostream>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <ctype.h>
#if WIN32
#include <thread>
#include <time.h>
#define SLEEP(x) Sleep(x)
#else
#include <pthread.h>
#define SLEEP(x) usleep(x)
#endif

Servo *control;
int vflag = 0;
using namespace std;

#define debug(fmt, ...) printf("%s:%d: " fmt, __FILE__, __LINE__, __VA_ARGS__);
#define vprintf(...) if (vflag) { printf(__VA_ARGS__); }
#if 0 /* Less movement */
#define PAN_JITTER 10
#define TILT_JITTER 10
#define UPDATE_JITTER 2000
#else /* More movement */
#define PAN_JITTER 20
#define TILT_JITTER 20
#define UPDATE_JITTER 1000
#endif

enum modes
{
  MODE_USER = 0,
  MODE_SCAN,
  MODE_JIGGLE,
  MODE_LAST
};

void help()
{
	cout << "usage: joystick -d serialport [-sijhv]\n";
	cout << "  -d port      Serial port i.e. /dev/ttyS0\n";
	cout << "  -s           Scaning mode, pan left to right automatically\n";
	cout << "  -i           Inverse y axes\n";
	cout << "  -j           Jiggle the camera simulating vibration\n";
	cout << "  -h           Print help\n";
	cout << "  -v           Verbose output\n\n";
	cout << "Tested Controllers:\n";
	cout << "  Sony Computer Entertainment Wireless Controller\n";
	cout << "  Xbox 360 Wireless Receiver\n";
}

void my_handler(int s){
  control->close_serial();
  SDL_Quit();
	printf("Done...\n");
	exit(1); 
}

class Joystick
{
public:
  Joystick(int, int);
  void scan(void);
  void jiggle(void);
  void user(int);
  int check(int);
private:
	char data[6];
	int x_axis; 
	int y_axis;
  // scan
  int x_dir;
  int y_dir;
  int pan;
  int tilt;
  // jitter
  int r1, r2, delay;
  // user
  bool button_state[5];
  bool last_button_state;
  bool last_button_a;
  int lock_servos;
  SDL_Joystick *joystick;
  int pan_speed;
  int tilt_speed;
	//Event handler 
  SDL_Event e; 
  SDL_GameController *ControllerHandle;
};

Joystick::Joystick(int x, int y)
{
  x_dir = -2;
  y_dir = -50;
  pan = 128;
  tilt = 128;
	data[0]=255;
	data[1]=8;
	data[2]=128;
	data[3]=255;
	data[4]=1;
  data[5]=128;
  last_button_state = 0;
  last_button_a = 0;
  lock_servos = 0;
  x_axis = x; 
  y_axis = y;
  pan_speed = 2;
  tilt_speed = 2;

  ControllerHandle = SDL_GameControllerOpen(0); // Assume only one joystick

  joystick = SDL_JoystickOpen(0);
  vprintf("%i joystick/s found.\n", SDL_NumJoysticks() );
  vprintf("The names of the joysticks are:\n");
	
  for(int i=0; i < SDL_NumJoysticks(); i++ ) 
  {
    SDL_Joystick *joystick = SDL_JoystickOpen(i);
	  printf("%s ", SDL_JoystickName(joystick));
    printf("(%d Buttons, ",SDL_JoystickNumButtons(joystick));
    printf("%d Axis)\n",SDL_JoystickNumAxes(joystick));
  }
}

void Joystick::scan(void)
{
    if (pan == 10)
      x_dir = 2;
    if (pan == 246)
      x_dir = -2;
    pan = pan + x_dir;
		data[2]=pan;
#if 1
    if (pan == 10)
    {
      y_dir = 50;
      tilt = tilt + y_dir;
	  	data[5]=tilt;
    }
    if (pan == 246)
    {
      y_dir = -50;
      tilt = tilt + y_dir;
		  data[5]=tilt;
    }
#endif
		control->write_serial(data, 6);
	  SLEEP (40000);
}

void Joystick::jiggle(void)
{
		r1 = ( (double)rand() / (RAND_MAX / TILT_JITTER) ) - TILT_JITTER / 2;
		r2 = ( (double)rand() / (RAND_MAX / PAN_JITTER) ) - PAN_JITTER / 2;
		data[2] = pan + r1;
		data[5] = tilt + r2;
		control->write_serial(data, 6);
		delay = ( (double)rand() / (RAND_MAX / UPDATE_JITTER) + 40000 );
	  SLEEP(delay);
}

void Joystick::user(int iflag)
{
  SDL_PollEvent( &e );
  
#if 0 // Old Method not as portable
  int xpos = SDL_JoystickGetAxis(joystick, x_axis);
  int ypos = SDL_JoystickGetAxis(joystick, y_axis);
#else
  int xpos = SDL_GameControllerGetAxis(ControllerHandle, SDL_CONTROLLER_AXIS_LEFTX);
  int ypos = SDL_GameControllerGetAxis(ControllerHandle, SDL_CONTROLLER_AXIS_RIGHTY);
#endif
  button_state[0] = SDL_GameControllerGetButton(ControllerHandle, SDL_CONTROLLER_BUTTON_RIGHTSHOULDER);
  SLEEP (40000);
  if (button_state[0])
  {
     if (last_button_state != button_state[0])
     {
       lock_servos ? lock_servos = 0 : lock_servos = 1;
       if (lock_servos)
       {
         vprintf("Locked\n");
       }
       else
       {
         vprintf("Unlocked\n");
       }
     }
  }
  last_button_state = button_state[0];

  
  if (!lock_servos)
  {
    button_state[1] = SDL_GameControllerGetButton(ControllerHandle, SDL_CONTROLLER_BUTTON_DPAD_RIGHT);
    button_state[2] = SDL_GameControllerGetButton(ControllerHandle, SDL_CONTROLLER_BUTTON_DPAD_LEFT);
    button_state[3] = SDL_GameControllerGetButton(ControllerHandle, SDL_CONTROLLER_BUTTON_DPAD_UP);
    button_state[4] = SDL_GameControllerGetButton(ControllerHandle, SDL_CONTROLLER_BUTTON_DPAD_DOWN);
    if (button_state[1] || 
        button_state[2] ||
        button_state[3] ||
        button_state[4] )
    {
      if (button_state[1]) pan += pan_speed;
      if (button_state[2]) pan -= pan_speed;
      if (iflag)
      {
        if (button_state[3]) tilt += tilt_speed;
        if (button_state[4]) tilt -= tilt_speed;
      }
      else
      {
        if (button_state[3]) tilt -= tilt_speed;
        if (button_state[4]) tilt += tilt_speed;
      }
		  data[5]=((ypos + 32768) / 256) - 128 + tilt;
		  data[2]=((xpos + 32768) / 256) - 128 + pan;
		  control->write_serial(data, 6);
    }
    else
    {
      int tmp=0;
		  tmp=((xpos + 32768) / 256) + (pan - 128);
		  if (tmp<0) tmp=0;
		  if (tmp>255) tmp=255;
		  data[2]=tmp;
      if (iflag)
      {
        // Invert y axes
    	  tmp = ((65535 - (ypos + 32768)) / 256) + (tilt - 128);
    		if (tmp<0) tmp=0;
    		if (tmp>255) tmp=255;
    		data[5]=tmp;
    	}
    	else
    	{
    	  tmp = ((ypos + 32768) / 256) + (tilt - 128);
    		if (tmp<0) tmp=0;
    		if (tmp>255) tmp=255;
	    	data[5]=tmp;
	    }
		  control->write_serial(data, 6);
    }
  }
}

int Joystick::check(int mode)
{
  bool b = 0;
  SDL_PollEvent( &e );
  b = SDL_GameControllerGetButton(ControllerHandle, SDL_CONTROLLER_BUTTON_A);
  if (b)
  {
    if (b != last_button_a)
    {
      mode=mode+1;
      if (mode==MODE_LAST) mode=0;
      vprintf("Mode Change %d\n", mode);
      pan=128;
      tilt=128;
    } 
  }
  last_button_a = b;
  return mode;
}

int main(int argc, char **argv)
{
	struct sigaction sigIntHandler;
  Joystick *joystick_control;
	//Main loop flag 
  bool quit = false; 
	//Normalized direction 
  int button = 4;
  // Parser variables
  opterr = 0;
  int mode = MODE_USER;
  int iflag = 0;
  char *comport = NULL;
  int index;
  int c;

//  cout << argc << "args\n";
  if (argc == 1)
  {
    help();
    return -1;
  }

  control = new Servo();

	sigIntHandler.sa_handler = my_handler;
	sigemptyset(&sigIntHandler.sa_mask);
	sigIntHandler.sa_flags = 0;

  // Handle CTRL+C properly
  sigaction(SIGINT, &sigIntHandler, NULL);

  while ((c = getopt (argc, argv, "d:shijv")) != -1)
    switch (c)
      {
      case 'd':
        comport = optarg;
        break;
      case 's':
        mode = MODE_SCAN;
        break;
      case 'i':
        iflag = 1;
        break;
      case 'j':
        mode = MODE_JIGGLE;
        break;
      case 'v':
        vflag = 1;
        break;
      case 'h':
        help();
        return -1;
      case '?':
        if (optopt == 'd')
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);
        else if (isprint (optopt))
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr,
                   "Unknown option character `\\x%x'.\n",
                   optopt);
        return 1;
      default:
        abort ();
      }

  if (comport==NULL) 
  {
    printf("Error: No serial port specified -d comport\n");
    help();
    return -1;
  }

  for (index = optind; index < argc; index++)
  {
    printf ("Non-option argument %s\n", argv[index]);
    return -1;
  }

  if (SDL_Init( SDL_INIT_GAMECONTROLLER | SDL_INIT_JOYSTICK ) < 0)
  {
    fprintf(stderr, "Couldn't initialize SDL: %s\n", SDL_GetError());
    exit(1);
  }

  printf("Abaco Systems - Joystick 'Pan & Tilt' Camera mount controller.\n");

//  if (strncmp("Sony Computer Entertainment Wireless Controller", joystick_name, 4) == 0)
  if (1)
  {
    joystick_control = new Joystick(0,4);
  }
  else
  {
    printf("Unrecognised joystick\n");
    control->close_serial();
    return -1;
  }

  control->init_serial(comport);
  while (1)
  {
    mode = joystick_control->check(mode);

    switch (mode)
    {
    case MODE_SCAN :
      joystick_control->scan();
      break;
    case MODE_JIGGLE : 
      joystick_control->jiggle();
      break;
    case MODE_USER : 
      joystick_control->user(iflag);
      break;
    }
  }

  std::cout << "Finished\n";

  control->close_serial();
  return 0;
}

