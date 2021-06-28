package metrics

import (
	"fmt"
	"testing"

	"go.opencensus.io/stats"
	"go.opencensus.io/stats/view"
)

// TestBasicAndDurationReport test for basic count,duration metrics and related tags
func TestBasicAndDurationReport(t *testing.T) {
	reporter, err := initTest()
	if err != nil {
		t.Errorf("Failed to initialize Test:%v", err)
	}

	testCounterMetric(t, reporter, AssignedIdentityAdditionCountM)
	testCounterMetric(t, reporter, AssignedIdentityDeletionCountM)
	testCounterMetric(t, reporter, AssignedIdentityUpdateCountM)
	testCounterMetric(t, reporter, MICCycleCountM)
	testCounterMetric(t, reporter, MICNewLeaderElectionCountM)
	testCounterMetric(t, reporter, CloudProviderOperationsErrorsCountM)
	testCounterMetric(t, reporter, KubernetesAPIOperationsErrorsCountM)
	testOperationDurationMetric(t, reporter, CloudProviderOperationsDurationM)
	testOperationDurationMetric(t, reporter, NMIOperationsDurationM)
}

// testOperationDurationMetric tests the duration metric and related tags
func testOperationDurationMetric(t *testing.T, reporter *Reporter, m *stats.Float64Measure) {
	minimumDuration := float64(2)
	maximumDuration := float64(4)
	testOperationKey := "test"
	err := reporter.ReportOperation(testOperationKey, m.M(minimumDuration))
	if err != nil {
		t.Errorf("Error when reporting metrics: %v from %v", err, m.Name())
	}
	err = reporter.ReportOperation(testOperationKey, m.M(maximumDuration))
	if err != nil {
		t.Errorf("Error when reporting metrics: %v from %v", err, m.Name())
	}

	row, err := view.RetrieveData(m.Name())
	if err != nil {
		t.Errorf("Error when retrieving data: %v from %v", err, m.Name())
	}

	duration, ok := row[0].Data.(*view.DistributionData)
	if !ok {
		t.Error("DistributionData missing")
	}

	tag := row[0].Tags[0]
	if tag.Key.Name() != operationTypeKey.Name() && tag.Value != testOperationKey {
		t.Errorf("Tag does not match for %v", operationTypeKey.Name())
	}
	if duration.Min != minimumDuration {
		t.Errorf("Metric: %v - Expected %v, got %v. ", m.Name(), duration.Min, minimumDuration)
	}
	if duration.Max != maximumDuration {
		t.Errorf("Metric: %v - Expected %v, got %v. ", m.Name(), duration.Max, maximumDuration)
	}
}

// testCounterMetric test the given measure count
func testCounterMetric(t *testing.T, reporter *Reporter, m *stats.Int64Measure) {
	totalNumberOfOperations := 2
	reporter.Report(m.M(1))
	reporter.Report(m.M(1))
	row, err := view.RetrieveData(m.Name())
	if err != nil {
		t.Errorf("Error when retrieving data: %v from %v", err, m.Name())
	}

	count, ok := row[0].Data.(*view.CountData)
	if !ok {
		t.Error("ReportRequest should have aggregation Count()")
	}
	if count.Value != int64(totalNumberOfOperations) {
		t.Errorf("Metric: %v - Expected %v, got %v. ", m.Name(), count.Value, totalNumberOfOperations)
	}
}

// initTest initialize the view and reporter for the test
func initTest() (*Reporter, error) {
	// initilize the views
	err := registerViews()
	if err != nil {
		return nil, err
	}
	reporter, err := NewReporter()
	if err != nil {
		return nil, fmt.Errorf("failed to create reporter for metrics, error: %+v", err)
	}
	return reporter, nil
}
