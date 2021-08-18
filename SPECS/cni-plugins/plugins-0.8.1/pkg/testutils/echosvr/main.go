// Echosvr is a simple TCP echo server
//
// It prints its listen address on stdout
//    127.0.0.1:xxxxx
//  A test should wait for this line, parse it
//  and may then attempt to connect.
package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"os"
	"strings"
	"time"
)

func main() {
	listener, err := net.Listen("tcp", ":")
	if err != nil {
		panic(err)
	}
	_, port, err := net.SplitHostPort(listener.Addr().String())
	if err != nil {
		panic(err)
	}
	fmt.Printf("127.0.0.1:%s\n", port)
	for {
		conn, err := listener.Accept()
		if err != nil {
			panic(err)
		}
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	conn.SetReadDeadline(time.Now().Add(1 * time.Minute))
	content, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil && err != io.EOF {
		fmt.Fprint(os.Stderr, err.Error())
		return
	}

	conn.SetWriteDeadline(time.Now().Add(1 * time.Minute))
	if _, err = conn.Write([]byte(strings.TrimSuffix(content, "\n"))); err != nil {
		fmt.Fprint(os.Stderr, err.Error())
		return
	}

	if err = conn.Close(); err != nil {
		fmt.Fprint(os.Stderr, err.Error())
		return
	}

}
