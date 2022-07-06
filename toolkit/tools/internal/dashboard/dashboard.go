package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("Starting dashboard")
	path := "/home/james/repos/CBL-Mariner/toolkit/tools/internal/timestamp/results/create_worker_chroot.csv"
	currentStat, _ := os.Stat(path)
	for true {
		newStat, _ := os.Stat(path)
		if currentStat.Size() != newStat.Size() {
			currentStat = newStat
			fmt.Println(currentStat.Size())
		}
	}

}
