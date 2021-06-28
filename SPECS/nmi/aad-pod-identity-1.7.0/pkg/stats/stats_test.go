package stats

import (
	"sync"
	"testing"
	"time"
)

func TestBasics(t *testing.T) {
	Init()
	Put(Total, time.Second*20)
	Aggregate(DeleteAzureAssignedIdentity, time.Second*40)
	Aggregate(DeleteAzureAssignedIdentity, time.Second*40)
	Increment(TotalPatchCalls, 100)
	Increment(TotalPatchCalls, 200)
	PrintSync()

	expectedDuration := time.Second * 20
	if globalStats[Total] != expectedDuration {
		t.Fatalf("Expected '%s' statistic to have a value of %s, but got %s", Total, expectedDuration, globalStats[Total])
	}

	expectedDuration = time.Second * 80
	if globalStats[DeleteAzureAssignedIdentity] != expectedDuration {
		t.Fatalf("Expected '%s' statistic to have a value of %s, but got %s", DeleteAzureAssignedIdentity, expectedDuration, globalStats[DeleteAzureAssignedIdentity])
	}

	expectedCount := 300
	if countStats[TotalPatchCalls] != expectedCount {
		t.Fatalf("Expected '%s' statistic to have a value of %d, but got %d", TotalPatchCalls, expectedCount, globalStats[TotalPatchCalls])
	}
}

func TestAggregateConcurrent(t *testing.T) {
	Init()

	begin := time.Now()
	count := 100

	var wg sync.WaitGroup
	wg.Add(count)

	for i := 0; i < count; i++ {
		go func() {
			defer wg.Done()
			begin := time.Now()
			time.Sleep(time.Millisecond * 10)
			AggregateConcurrent(CreateAzureAssignedIdentiy, begin, time.Now())
		}()
	}
	wg.Wait()
	PrintSync()

	totalDuration := time.Since(begin)
	if totalDuration < globalStats[CreateAzureAssignedIdentiy] {
		t.Fatalf("Expected the total duration to be shorter than %s, but got %s", totalDuration, globalStats[CreateAzureAssignedIdentiy])
	}
}
