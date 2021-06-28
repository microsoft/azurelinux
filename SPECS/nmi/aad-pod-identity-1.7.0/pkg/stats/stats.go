package stats

import (
	"sync"
	"time"

	"k8s.io/klog/v2"
)

type minMaxTime struct {
	min time.Time
	max time.Time
}

var (
	// globalStats is a map that stores the duration of each statistic.
	globalStats map[Type]time.Duration

	// minMaxTimeStats is a map that stores the earliest start time and
	// latest end time of statistics that are being collected concurrently.
	minMaxTimeStats map[Type]minMaxTime

	// countStats is a map that stores the count of each statistic.
	countStats map[Type]int

	mutex *sync.RWMutex
)

// Type represents differnet statistics that are being collected.
type Type string

const (
	// Total represents the total duration of a specific operation.
	Total Type = "Total"

	// System represents the duration it takes to list all aad-pod-identity CRDs.
	System Type = "System"

	// CacheSync represents the duration it takes to sync CRD client's cache.
	CacheSync Type = "CacheSync"

	// CurrentState represents the duration it takes to generate a list of desired AzureAssignedIdentities.
	CurrentState Type = "Gather current state"

	// PodList represents the duration it takes to list pods.
	PodList Type = "Pod listing"

	// AzureIdentityBindingList represents the duration it takes to list AzureIdentityBindings.
	AzureIdentityBindingList Type = "AzureIdentityBinding listing"

	// AzureIdentityList represents the duration it takes to list AzureIdentities.
	AzureIdentityList Type = "AzureIdentity listing"

	// AzurePodIdentityExceptionList represents the duration it takes to list AzurePodIdentityExceptions.
	AzurePodIdentityExceptionList Type = "AzurePodIdentityException listing"

	// AzureAssignedIdentityList represents the duration it takes to list AzureAssignedIdentities.
	AzureAssignedIdentityList Type = "AzureAssignedIdentity listing"

	// CloudGet represents the duration it takes to complete a GET request to ARM in a given sync cycle.
	CloudGet Type = "Cloud provider GET"

	// CloudPatch represents the duration it takes to complete a PATCH request to ARM in a given sync cycle.
	CloudPatch Type = "Cloud provider PATCH"

	// TotalPatchCalls represents the number of PATCH requests to ARM in a given sync cycle.
	TotalPatchCalls Type = "Number of cloud provider PATCH"

	// TotalGetCalls represents the number of GET requests to ARM in a given sync cycle.
	TotalGetCalls Type = "Number of cloud provider GET"

	// TotalAzureAssignedIdentitiesCreated represents the number of AzureAssignedIdentities created in a given sync cycle.
	TotalAzureAssignedIdentitiesCreated Type = "Number of AzureAssignedIdentities created in this sync cycle"

	// TotalAzureAssignedIdentitiesUpdated represents the number of AzureAssignedIdentities updated in a given sync cycle.
	TotalAzureAssignedIdentitiesUpdated Type = "Number of AzureAssignedIdentities updated in this sync cycle"

	// TotalAzureAssignedIdentitiesDeleted represents the number of AzureAssignedIdentities deleted in a given sync cycle.
	TotalAzureAssignedIdentitiesDeleted Type = "Number of AzureAssignedIdentities deleted in this sync cycle"

	// FindAzureAssignedIdentitiesToDelete represents the duration it takes to generate a list of AzureAssignedIdentities to be deleted.
	FindAzureAssignedIdentitiesToDelete Type = "Find AzureAssignedIdentities to delete"

	// FindAzureAssignedIdentitiesToCreate represents the duration it takes to generate a list of AzureAssignedIdentities to be created.
	FindAzureAssignedIdentitiesToCreate Type = "Find AzureAssignedIdentities to create"

	// DeleteAzureAssignedIdentity represents the duration it takes to delete an AzureAssignedIdentity.
	DeleteAzureAssignedIdentity Type = "AzureAssignedIdentity deletion"

	// CreateAzureAssignedIdentiy represents the duration it takes to create an AzureAssignedIdentity.
	CreateAzureAssignedIdentiy Type = "AzureAssignedIdentity creation"

	// UpdateAzureAssignedIdentity represents the duration it takes to update an AzureAssignedIdentity.
	UpdateAzureAssignedIdentity Type = "AzureAssignedIdentity update"

	// TotalAzureAssignedIdentitiesCreateOrUpdate represents the duration it takes to create or update a given list of AzureAssignedIdentities.
	TotalAzureAssignedIdentitiesCreateOrUpdate Type = "Total time to assign or update AzureAssignedIdentities"
)

// Init initializes the maps uesd to store the
func Init() {
	globalStats = make(map[Type]time.Duration)
	minMaxTimeStats = make(map[Type]minMaxTime)
	countStats = make(map[Type]int)
	mutex = &sync.RWMutex{}
}

// Put puts a value to a specific statistic.
func Put(key Type, val time.Duration) {
	if globalStats != nil {
		mutex.Lock()
		defer mutex.Unlock()
		globalStats[key] = val
	}
}

// Aggregate aggregates the value of a specific statistic.
func Aggregate(key Type, val time.Duration) {
	if globalStats != nil {
		mutex.Lock()
		defer mutex.Unlock()

		globalStats[key] = globalStats[key] + val
	}
}

// AggregateConcurrent aggregates the value of a specific statistic that is being collected concurrently.
func AggregateConcurrent(key Type, begin, end time.Time) {
	if globalStats != nil && minMaxTimeStats != nil {
		mutex.Lock()
		defer mutex.Unlock()

		// we only need the earliest begin time and the latest end
		// time to calculate the total duration of a statistic
		var min, max time.Time
		if _, ok := minMaxTimeStats[key]; !ok {
			min, max = begin, end
		} else {
			min, max = minMaxTimeStats[key].min, minMaxTimeStats[key].max
		}

		if begin.Before(min) {
			min = begin
		}
		if end.After(max) {
			max = end
		}

		minMaxTimeStats[key] = minMaxTime{
			min: min,
			max: max,
		}
		globalStats[key] = minMaxTimeStats[key].max.Sub(minMaxTimeStats[key].min)
	}
}

// Print prints the value of a specific statistic.
func Print(key Type) {
	mutex.RLock()
	defer mutex.RUnlock()

	klog.Infof("%s: %s", key, globalStats[key])
}

// PrintCount prints the count of a specific statistic.
func PrintCount(key Type) {
	mutex.RLock()
	defer mutex.RUnlock()

	klog.Infof("%s: %d", key, countStats[key])
}

// Increment Increments the count of a specific statistic.
func Increment(key Type, count int) {
	mutex.Lock()
	defer mutex.Unlock()

	countStats[key] = countStats[key] + count
}

// PrintSync prints all relevant statistics in a sync cycle.
func PrintSync() {
	klog.Infof("** stats collected **")
	if globalStats != nil {
		Print(PodList)
		Print(AzureIdentityList)
		Print(AzureIdentityBindingList)
		Print(AzureAssignedIdentityList)
		Print(System)
		Print(CacheSync)

		Print(CloudGet)
		Print(CloudPatch)
		Print(CreateAzureAssignedIdentiy)
		Print(UpdateAzureAssignedIdentity)
		Print(DeleteAzureAssignedIdentity)

		PrintCount(TotalPatchCalls)
		PrintCount(TotalGetCalls)

		PrintCount(TotalAzureAssignedIdentitiesCreated)
		PrintCount(TotalAzureAssignedIdentitiesUpdated)
		PrintCount(TotalAzureAssignedIdentitiesDeleted)

		Print(FindAzureAssignedIdentitiesToCreate)
		Print(FindAzureAssignedIdentitiesToDelete)

		Print(TotalAzureAssignedIdentitiesCreateOrUpdate)

		Print(Total)
	}
	klog.Infof("*********************")
}
