package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Println("Starting dashboard")
	wd, _ := os.Getwd()
	idx := strings.Index(wd, "CBL-Mariner/toolkit")
	wd = wd[0 : idx+19]
	wd += "/tools/internal/timestamp/results/create_worker_chroot.csv"
	path := wd
	currentStat, _ := os.Stat(path)
	for true {
		newStat, _ := os.Stat(path)
		if currentStat.Size() != newStat.Size() {
			currentStat = newStat
			fmt.Println(currentStat.Size())
		}
	}

}
