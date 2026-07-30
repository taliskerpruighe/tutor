//go:build darwin

// The only OS-specific code in the programme. BSD spells the terminal ioctls
// TIOCGETA/TIOCSETA where Linux says TCGETS/TCSETS, and the Termios struct
// differs in field widths — so both come from Go's own per-GOOS syscall
// package rather than being hardcoded here, which makes them right by
// construction on a machine that cannot run the result.
package main

import (
	"syscall"
	"unsafe"
)

type termios = syscall.Termios

const (
	setNow   = syscall.TIOCSETA  // TCSANOW
	setDrain = 0x80487415        // TIOCSETAW  (TCSADRAIN)
	setFlush = syscall.TIOCSETAF // TCSAFLUSH
)

func getTermios(fd int) (*termios, error) {
	var t termios
	if err := ioctlPtr(fd, syscall.TIOCGETA, unsafe.Pointer(&t)); err != nil {
		return nil, err
	}
	return &t, nil
}

func setTermios(fd int, req uintptr, t *termios) error {
	return ioctlPtr(fd, req, unsafe.Pointer(t))
}

func getWinsize(fd int) (cols, rows int, err error) {
	var ws struct{ Row, Col, Xpixel, Ypixel uint16 }
	if err := ioctlPtr(fd, syscall.TIOCGWINSZ, unsafe.Pointer(&ws)); err != nil {
		return 0, 0, err
	}
	return int(ws.Col), int(ws.Row), nil
}

func ioctlPtr(fd int, req uintptr, arg unsafe.Pointer) error {
	_, _, errno := syscall.Syscall(syscall.SYS_IOCTL, uintptr(fd), req, uintptr(arg))
	if errno != 0 {
		return errno
	}
	return nil
}
