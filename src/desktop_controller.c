#include <linux/uinput.h>

#include <fcntl.h>
#include <string.h>
#include <unistd.h>

#include <stdlib.h>

void emit(int fd, int type, int code, int val) {
  struct input_event ie;

  ie.type = type;
  ie.code = code;
  ie.value = val;
  /* timestamp values below are ignored */
  ie.time.tv_sec = 0;
  ie.time.tv_usec = 0;

  write(fd, &ie, sizeof(ie));
}

struct desktop_controller {
  int fd;
};

void *desktop_controller_init() {
  struct desktop_controller *desktop_controller_ptr =
      malloc(sizeof(struct desktop_controller));
  int fd = open("/dev/uinput", O_WRONLY | O_NONBLOCK);
  desktop_controller_ptr->fd = fd;
  struct uinput_setup usetup;

  /*
   * The ioctls below will enable the device that is about to be
   * created, to pass key events
   */
  ioctl(fd, UI_SET_EVBIT, EV_KEY);
  ioctl(fd, UI_SET_KEYBIT, KEY_SPACE);
  ioctl(fd, UI_SET_KEYBIT, KEY_W);
  ioctl(fd, UI_SET_KEYBIT, KEY_A);
  ioctl(fd, UI_SET_KEYBIT, KEY_S);
  ioctl(fd, UI_SET_KEYBIT, KEY_D);

  memset(&usetup, 0, sizeof(usetup));
  usetup.id.bustype = BUS_USB;
  usetup.id.vendor = 0x1234;  /* sample vendor */
  usetup.id.product = 0x5678; /* sample product */
  strcpy(usetup.name, "Argos Desktop Controller");

  ioctl(fd, UI_DEV_SETUP, &usetup);
  ioctl(fd, UI_DEV_CREATE);

  return (void *)desktop_controller_ptr;
}

void desktop_controller_free(void *self) {
  struct desktop_controller *desktop_controller_ptr =
      (struct desktop_controller *)self;
  ioctl(desktop_controller_ptr->fd, UI_DEV_DESTROY);
  close(desktop_controller_ptr->fd);
  free(self);
}

void input_event(void *self, int eventCode) {
  struct desktop_controller *desktop_controller_ptr =
      (struct desktop_controller *)self;

  int fd = desktop_controller_ptr->fd;

  /* Key press, report the event, send key release, and report again */
  emit(fd, EV_KEY, eventCode, 1);
  emit(fd, EV_SYN, SYN_REPORT, 0);
  sleep(1);
  emit(fd, EV_KEY, eventCode, 0);
  emit(fd, EV_SYN, SYN_REPORT, 0);
}

