package metrics

import (
	"context"
	"fmt"
	"sync"
	"time"

	"go.opencensus.io/stats"
	"go.opencensus.io/stats/view"
	"go.opencensus.io/tag"
	"k8s.io/klog/v2"
)

// This const block defines the metric names.
const (
	assignedIdentityAdditionDurationName   = "assigned_identity_addition_duration_seconds"
	assignedIdentityAdditionCountName      = "assigned_identity_addition_count"
	assignedIdentityDeletionDurationName   = "assigned_identity_deletion_duration_seconds"
	assignedIdentityDeletionCountName      = "assigned_identity_deletion_count"
	assignedIdentityUpdateDurationName     = "assigned_identity_update_duration_seconds"
	assignedIdentityUpdateCountName        = "assigned_identity_update_count"
	nmiOperationsDurationName              = "nmi_operations_duration_seconds"
	micCycleDurationName                   = "mic_cycle_duration_seconds"
	micCycleCountName                      = "mic_cycle_count"
	micNewLeaderElectionCountName          = "mic_new_leader_election_count"
	cloudProviderOperationsErrorsCountName = "cloud_provider_operations_errors_count"
	cloudProviderOperationsDurationName    = "cloud_provider_operations_duration_seconds"
	kubernetesAPIOperationsErrorsCountName = "kubernetes_api_operations_errors_count"
	imdsOperationsErrorsCountName          = "imds_operations_errors_count"
	imdsOperationsDurationName             = "imds_operations_duration_seconds"

	// AdalTokenFromMSIOperationName represents the duration of obtaining a token with MSI.
	AdalTokenFromMSIOperationName = "adal_token_msi" // #nosec

	// AdalTokenFromMSIWithUserAssignedIDOperationName represents the duration of obtaining a token with a user-assigned identity.
	AdalTokenFromMSIWithUserAssignedIDOperationName = "adal_token_msi_userassignedid" // #nosec

	// AdalTokenOperationName represents the duration of obtaining a token.
	AdalTokenOperationName = "adal_token"

	// GetVmssOperationName represents the duration of a GET request to a VMSS instance.
	GetVmssOperationName = "vmss_get"

	// UpdateVMSSOperationName represents the duration of a PATCH request to a VMSS instance.
	UpdateVMSSOperationName = "vmss_update"

	// GetVMOperationName represents the duration of a GET request to a VM instance.
	GetVMOperationName = "vm_get"

	// UpdateVMOperationName represents the duration of a PATCH request to a VM instance.
	UpdateVMOperationName = "vm_update"

	// AssignedIdentityDeletionOperationName represents the duration of an AzureAssignedIdentity deletion.
	AssignedIdentityDeletionOperationName = "assigned_identity_deletion"

	// AssignedIdentityAdditionOperationName represents the duration of an AzureAssignedIdentity addition.
	AssignedIdentityAdditionOperationName = "assigned_identity_addition"

	// AssignedIdentityUpdateOperationName represents the duration of an AzureAssignedIdentity update.
	AssignedIdentityUpdateOperationName = "assigned_identity_update"

	// UpdateAzureAssignedIdentityStatusOperationName represents the status of an AzureAssignedIdentity update operation.
	UpdateAzureAssignedIdentityStatusOperationName = "update_azure_assigned_identity_status"

	// GetPodListOperationName represents the status of a pod list operation.
	GetPodListOperationName = "get_pod_list"

	// GetSecretOperationName represents the status of a secret get operation.
	GetSecretOperationName = "get_secret"
)

// The following variables are measures
var (
	// AssignedIdentityAdditionDurationM is a measure that tracks the duration in seconds of assigned_identity_addition operations.
	AssignedIdentityAdditionDurationM = stats.Float64(
		assignedIdentityAdditionDurationName,
		"Duration in seconds of assigned identity addition operations",
		stats.UnitMilliseconds)

	// AssignedIdentityAdditionCountM is a measure that tracks the cumulative number of assigned identity addition operations.
	AssignedIdentityAdditionCountM = stats.Int64(
		assignedIdentityAdditionCountName,
		"Total number of assigned identity addition operations",
		stats.UnitDimensionless)

	// AssignedIdentityDeletionDurationM is a measure that tracks the duration in seconds of assigned_identity_deletion operations.
	AssignedIdentityDeletionDurationM = stats.Float64(
		assignedIdentityDeletionDurationName,
		"Duration in seconds of assigned identity deletion operations",
		stats.UnitMilliseconds)

	// AssignedIdentityDeletionCountM is a measure that tracks the cumulative number of assigned identity deletion operations.
	AssignedIdentityDeletionCountM = stats.Int64(assignedIdentityDeletionCountName,
		"Total number of assigned identity deletion operations",
		stats.UnitDimensionless)

	// NMIOperationsDurationM is a measure that tracks the duration in seconds of nmi operations.
	NMIOperationsDurationM = stats.Float64(
		nmiOperationsDurationName,
		"Duration in seconds for nmi operations",
		stats.UnitMilliseconds)

	// MICCycleDurationM is a measure that tracks the duration in seconds for single mic sync cycle.
	MICCycleDurationM = stats.Float64(
		micCycleDurationName,
		"Duration in seconds for single mic sync cycle",
		stats.UnitMilliseconds)

	// MICCycleCountM is a measure that tracks the cumulative number of cycles executed in mic.
	MICCycleCountM = stats.Int64(
		micCycleCountName,
		"Total number of cycles executed in mic",
		stats.UnitDimensionless)

	// MICNewLeaderElectionCountM is a measure that tracks the cumulative number of new leader election in mic.
	MICNewLeaderElectionCountM = stats.Int64(
		micNewLeaderElectionCountName,
		"Total number of new leader election in mic",
		stats.UnitDimensionless)

	// CloudProviderOperationsErrorsCountM is a measure that tracks the cumulative number of errors in cloud provider operations.
	CloudProviderOperationsErrorsCountM = stats.Int64(
		cloudProviderOperationsErrorsCountName,
		"Total number of errors in cloud provider operations",
		stats.UnitDimensionless)

	// CloudProviderOperationsDurationM is a measure that tracks the duration in seconds of CloudProviderOperations operations.
	CloudProviderOperationsDurationM = stats.Float64(
		cloudProviderOperationsDurationName,
		"Duration in seconds of cloudprovider operations",
		stats.UnitMilliseconds)

	// KubernetesAPIOperationsErrorsCountM is a measure that tracks the cumulative number of errors in cloud provider operations.
	KubernetesAPIOperationsErrorsCountM = stats.Int64(
		kubernetesAPIOperationsErrorsCountName,
		"Total number of errors in kubernetes api operations",
		stats.UnitDimensionless)

	// ImdsOperationsErrorsCountM is a measure that tracks the cumulative number of errors in imds operations.
	ImdsOperationsErrorsCountM = stats.Int64(
		imdsOperationsErrorsCountName,
		"Total number of errors in imds token operations",
		stats.UnitDimensionless)

	// ImdsOperationsDurationM is a measure that tracks the duration in seconds of imds operations.
	ImdsOperationsDurationM = stats.Float64(
		imdsOperationsDurationName,
		"Duration in seconds of imds token operations",
		stats.UnitMilliseconds)

	// AssignedIdentityUpdateDurationM is a measure that tracks the duration in seconds of assigned_identity_update operations.
	AssignedIdentityUpdateDurationM = stats.Float64(
		assignedIdentityUpdateDurationName,
		"Duration in seconds of assigned identity update operations",
		stats.UnitMilliseconds)

	// AssignedIdentityUpdateCountM is a measure that tracks the cumulative number of assigned identity update operations.
	AssignedIdentityUpdateCountM = stats.Int64(
		assignedIdentityUpdateCountName,
		"Total number of assigned identity update operations",
		stats.UnitDimensionless)
)

var (
	operationTypeKey = tag.MustNewKey("operation_type")
	statusCodeKey    = tag.MustNewKey("status_code")
	namespaceKey     = tag.MustNewKey("namespace")
	resourceKey      = tag.MustNewKey("resource")
)

const componentNamespace = "aadpodidentity"

// SinceInSeconds gets the time since the specified start in seconds.
func SinceInSeconds(start time.Time) float64 {
	return time.Since(start).Seconds()
}

// registerViews register views to be collected by exporter
func registerViews() error {
	views := []*view.View{
		{
			Description: AssignedIdentityAdditionDurationM.Description(),
			Measure:     AssignedIdentityAdditionDurationM,
			Aggregation: view.Distribution(0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 10),
		},
		{
			Description: AssignedIdentityAdditionCountM.Description(),
			Measure:     AssignedIdentityAdditionCountM,
			Aggregation: view.Count(),
		},
		{
			Description: AssignedIdentityDeletionDurationM.Description(),
			Measure:     AssignedIdentityDeletionDurationM,
			Aggregation: view.Distribution(0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 10),
		},
		{
			Description: AssignedIdentityDeletionCountM.Description(),
			Measure:     AssignedIdentityDeletionCountM,
			Aggregation: view.Count(),
		},
		{
			Description: NMIOperationsDurationM.Description(),
			Measure:     NMIOperationsDurationM,
			Aggregation: view.Distribution(0.5, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100),
			TagKeys:     []tag.Key{operationTypeKey, statusCodeKey, namespaceKey, resourceKey},
		},
		{
			Description: MICCycleDurationM.Description(),
			Measure:     MICCycleDurationM,
			Aggregation: view.Distribution(0.5, 1, 5, 10, 30, 60, 120, 300, 600, 900, 1200),
		},
		{
			Description: MICCycleCountM.Description(),
			Measure:     MICCycleCountM,
			Aggregation: view.Count(),
		},
		{
			Description: MICNewLeaderElectionCountM.Description(),
			Measure:     MICNewLeaderElectionCountM,
			Aggregation: view.Count(),
		},
		{
			Description: CloudProviderOperationsErrorsCountM.Description(),
			Measure:     CloudProviderOperationsErrorsCountM,
			Aggregation: view.Count(),
			TagKeys:     []tag.Key{operationTypeKey},
		},
		{
			Description: CloudProviderOperationsDurationM.Description(),
			Measure:     CloudProviderOperationsDurationM,
			Aggregation: view.Distribution(0.5, 1, 5, 10, 30, 60, 120, 300, 600, 900, 1200),
			TagKeys:     []tag.Key{operationTypeKey},
		},
		{
			Description: KubernetesAPIOperationsErrorsCountM.Description(),
			Measure:     KubernetesAPIOperationsErrorsCountM,
			Aggregation: view.Count(),
			TagKeys:     []tag.Key{operationTypeKey},
		},
		{
			Description: ImdsOperationsErrorsCountM.Description(),
			Measure:     ImdsOperationsErrorsCountM,
			Aggregation: view.Count(),
			TagKeys:     []tag.Key{operationTypeKey},
		},
		{
			Description: ImdsOperationsDurationM.Description(),
			Measure:     ImdsOperationsDurationM,
			Aggregation: view.Distribution(0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 10),
			TagKeys:     []tag.Key{operationTypeKey},
		},
		{
			Description: AssignedIdentityUpdateDurationM.Description(),
			Measure:     AssignedIdentityUpdateDurationM,
			Aggregation: view.Distribution(0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 10),
		},
		{
			Description: AssignedIdentityUpdateCountM.Description(),
			Measure:     AssignedIdentityUpdateCountM,
			Aggregation: view.Count(),
		},
	}
	err := view.Register(views...)
	return err
}

// record records the given measure
func record(ctx context.Context, ms ...stats.Measurement) {
	stats.Record(ctx, ms...)
}

// Reporter is stats reporter in the context
type Reporter struct {
	// adding mutex lock to ensure thread safety
	// TODO (aramase) remove this lock after confirming opencensus report
	// call is thread-safe
	mu  sync.Mutex
	ctx context.Context
}

// NewReporter creates a reporter with new context
func NewReporter() (*Reporter, error) {
	ctx, err := tag.New(
		context.Background(),
	)
	if err != nil {
		return nil, err
	}
	return &Reporter{ctx: ctx, mu: sync.Mutex{}}, nil
}

// Report records the given measure
func (r *Reporter) Report(ms ...stats.Measurement) {
	r.mu.Lock()
	record(r.ctx, ms...)
	r.mu.Unlock()
}

// ReportOperationAndStatus records given measurements by operation type, status code for the given namespace and resource.
func (r *Reporter) ReportOperationAndStatus(operationType, statusCode, namespace, resource string, ms ...stats.Measurement) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	ctx, err := tag.New(
		r.ctx,
		tag.Insert(operationTypeKey, operationType),
		tag.Insert(statusCodeKey, statusCode),
		tag.Insert(namespaceKey, namespace),
		tag.Insert(resourceKey, resource),
	)
	if err != nil {
		return err
	}
	record(ctx, ms...)
	return nil
}

// ReportOperation records given measurement by operation type.
func (r *Reporter) ReportOperation(operationType string, measurement stats.Measurement) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	ctx, err := tag.New(
		r.ctx,
		tag.Insert(operationTypeKey, operationType),
	)
	if err != nil {
		return err
	}
	record(ctx, measurement)
	return nil
}

// RegisterAndExport register the views for the measures and expose via prometheus exporter
func RegisterAndExport(port string) error {
	err := registerViews()
	if err != nil {
		return fmt.Errorf("failed to register views for metrics, error:%v", err)
	}
	klog.Infof("registered views for metric")
	exporter, err := newPrometheusExporter(componentNamespace, port)
	if err != nil {
		return fmt.Errorf("failed to create Prometheus exporter, error: %+v", err)
	}
	view.RegisterExporter(exporter)
	klog.Infof("registered and exported metrics on port %s", port)
	return nil
}

// ReportIMDSOperationError reports IMDS error count
func (r *Reporter) ReportIMDSOperationError(operation string) error {
	return r.ReportOperation(operation, ImdsOperationsErrorsCountM.M(1))
}

// ReportIMDSOperationDuration reports IMDS operation duration
func (r *Reporter) ReportIMDSOperationDuration(operation string, duration time.Duration) error {
	return r.ReportOperation(operation, ImdsOperationsDurationM.M(duration.Seconds()))
}

// ReportCloudProviderOperationError reports cloud provider operation error count
func (r *Reporter) ReportCloudProviderOperationError(operation string) error {
	return r.ReportOperation(operation, CloudProviderOperationsErrorsCountM.M(1))
}

// ReportCloudProviderOperationDuration reports cloud provider operation duration
func (r *Reporter) ReportCloudProviderOperationDuration(operation string, duration time.Duration) error {
	return r.ReportOperation(operation, CloudProviderOperationsDurationM.M(duration.Seconds()))
}

// ReportKubernetesAPIOperationError reports kubernetes operation error count
func (r *Reporter) ReportKubernetesAPIOperationError(operation string) error {
	return r.ReportOperation(operation, KubernetesAPIOperationsErrorsCountM.M(1))
}
