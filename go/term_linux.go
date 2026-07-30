//go:build linux

// The Linux counterpart of term_darwin.go. This is the build the test harness
// exercises; the darwin file above is its mirror image.
package main

import (
	"syscall"
	"unsafe"
)

type termios = syscall.Termios

const (
	tcgets   = 0x5401
	setNow   = 0x5402 // TCSETS   (TCSANOW)
	setDrain = 0x5403 // TCSETSW  (TCSADRAIN)
	setFlush = 0x5404 // TCSETSF  (TCSAFLUSH)
)

func getTermios(fd int) (*termios, error) {
	var t termios
	if err := ioctlPtr(fd, tcgets, unsafe.Pointer(&t)); err != nil {
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

// The pixel fields this ioctl also returns are read by cellPixels in
// image.go, which does its own TIOCGWINSZ rather than calling through here.
// That duplication is deliberate: image.go is self-contained by design, and
// a second accessor in this file would be a copy of the same three lines
// with nothing to keep the two honest if one of them changed.

func ioctlPtr(fd int, req uintptr, arg unsafe.Pointer) error {
	_, _, errno := syscall.Syscall(syscall.SYS_IOCTL, uintptr(fd), req, uintptr(arg))
	if errno != 0 {
		return errno
	}
	return nil
}
