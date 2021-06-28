package server

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"os/signal"
	"regexp"
	"runtime"
	"runtime/debug"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/Azure/go-autorest/autorest/adal"
	"k8s.io/klog/v2"

	"github.com/Azure/aad-pod-identity/pkg/auth"
	"github.com/Azure/aad-pod-identity/pkg/k8s"
	"github.com/Azure/aad-pod-identity/pkg/metrics"
	"github.com/Azure/aad-pod-identity/pkg/nmi"
	"github.com/Azure/aad-pod-identity/pkg/nmi/iptables"
	"github.com/Azure/aad-pod-identity/pkg/pod"
)

const (
	localhost = "127.0.0.1"
)

// Server encapsulates all of the parameters necessary for starting up
// the server. These can be set via command line.
type Server struct {
	KubeClient                         k8s.Client
	NMIPort                            string
	MetadataIP                         string
	MetadataPort                       string
	NodeName                           string
	IPTableUpdateTimeIntervalInSeconds int
	MICNamespace                       string
	Initialized                        bool
	BlockInstanceMetadata              bool
	MetadataHeaderRequired             bool
	// TokenClient is client that fetches identities and tokens
	TokenClient nmi.TokenClient
	Reporter    *metrics.Reporter
}

// NMIResponse is the response returned to caller
type NMIResponse struct {
	Token    msiResponse `json:"token"`
	ClientID string      `json:"clientid"`
}

// MetadataResponse represents the error returned
// to caller when metadata header is not specified.
type MetadataResponse struct {
	Error            string `json:"error"`
	ErrorDescription string `json:"error_description"`
}

// NewServer will create a new Server with default values.
func NewServer(micNamespace string, blockInstanceMetadata bool, metadataHeaderRequired bool) *Server {
	reporter, err := metrics.NewReporter()
	if err != nil {
		klog.Errorf("failed to create reporter for metrics, error: %+v", err)
	} else {
		// keeping this reference to be used in ServeHTTP, as server is not accessible in ServeHTTP
		appHandlerReporter = reporter
		auth.InitReporter(reporter)
	}
	return &Server{
		MICNamespace:           micNamespace,
		BlockInstanceMetadata:  blockInstanceMetadata,
		MetadataHeaderRequired: metadataHeaderRequired,
		Reporter:               reporter,
	}
}

// Run runs the specified Server.
func (s *Server) Run() error {
	go s.updateIPTableRules()

	mux := http.NewServeMux()
	mux.Handle("/metadata/identity/oauth2/token", appHandler(s.msiHandler))
	mux.Handle("/metadata/identity/oauth2/token/", appHandler(s.msiHandler))
	mux.Handle("/host/token", appHandler(s.hostHandler))
	mux.Handle("/host/token/", appHandler(s.hostHandler))
	if s.BlockInstanceMetadata {
		mux.Handle("/metadata/instance", http.HandlerFunc(forbiddenHandler))
	}
	mux.Handle("/", appHandler(s.defaultPathHandler))

	klog.Infof("listening on port %s", s.NMIPort)
	if err := http.ListenAndServe("localhost:"+s.NMIPort, mux); err != nil {
		klog.Fatalf("error creating http server: %+v", err)
	}
	return nil
}

func (s *Server) updateIPTableRulesInternal() {
	klog.V(5).Infof("node(%s) ip(%s) metadata address(%s:%s) nmi port(%s)", s.NodeName, localhost, s.MetadataIP, s.MetadataPort, s.NMIPort)

	if err := iptables.AddCustomChain(s.MetadataIP, s.MetadataPort, localhost, s.NMIPort); err != nil {
		klog.Fatalf("%s", err)
	}
	if err := iptables.LogCustomChain(); err != nil {
		klog.Fatalf("%s", err)
	}
}

// updateIPTableRules ensures the correct iptable rules are set
// such that metadata requests are received by nmi assigned port
// NOT originating from HostIP destined to metadata endpoint are
// routed to NMI endpoint
func (s *Server) updateIPTableRules() {
	signalChan := make(chan os.Signal, 1)
	signal.Notify(signalChan, syscall.SIGTERM, syscall.SIGINT)

	ticker := time.NewTicker(time.Second * time.Duration(s.IPTableUpdateTimeIntervalInSeconds))
	defer ticker.Stop()

	// Run once before the waiting on ticker for the rules to take effect
	// immediately.
	s.updateIPTableRulesInternal()
	s.Initialized = true

loop:
	for {
		select {
		case <-signalChan:
			handleTermination()
			break loop

		case <-ticker.C:
			s.updateIPTableRulesInternal()
		}
	}
}

type appHandler func(http.ResponseWriter, *http.Request) string

type responseWriter struct {
	http.ResponseWriter
	statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}

func newResponseWriter(w http.ResponseWriter) *responseWriter {
	return &responseWriter{w, http.StatusOK}
}

var appHandlerReporter *metrics.Reporter

// ServeHTTP implements the net/http server handler interface
// and recovers from panics.
func (fn appHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	tracker := fmt.Sprintf("req.method=%s reg.path=%s req.remote=%s", r.Method, r.URL.Path, parseRemoteAddr(r.RemoteAddr))

	// Set the header in advance so that both success as well
	// as error paths have it set as application/json content type.
	w.Header().Set("Content-Type", "application/json")
	start := time.Now()
	defer func() {
		var err error
		if rec := recover(); rec != nil {
			_, file, line, _ := runtime.Caller(3)
			stack := string(debug.Stack())
			switch t := rec.(type) {
			case string:
				err = errors.New(t)
			case error:
				err = t
			default:
				err = errors.New("unknown error")
			}
			klog.Errorf("panic processing request: %+v, file: %s, line: %d, stacktrace: '%s' %s res.status=%d", r, file, line, stack, tracker, http.StatusInternalServerError)
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}
	}()
	rw := newResponseWriter(w)
	ns := fn(rw, r)
	latency := time.Since(start)
	klog.Infof("status (%d) took %d ns for %s", rw.statusCode, latency.Nanoseconds(), tracker)

	tokenRequest := parseTokenRequest(r)

	if appHandlerReporter != nil {
		err := appHandlerReporter.ReportOperationAndStatus(
			r.URL.Path,
			strconv.Itoa(rw.statusCode),
			ns,
			tokenRequest.Resource,
			metrics.NMIOperationsDurationM.M(metrics.SinceInSeconds(start)))
		if err != nil {
			klog.Warningf("failed to report metrics, error: %+v", err)
		}
	}
}

func (s *Server) hostHandler(w http.ResponseWriter, r *http.Request) (ns string) {
	hostIP := parseRemoteAddr(r.RemoteAddr)
	tokenRequest := parseTokenRequest(r)

	podns, podname := parsePodInfo(r)
	if podns == "" || podname == "" {
		klog.Error("missing podname and podns from request")
		http.Error(w, "missing 'podname' and 'podns' from request header", http.StatusBadRequest)
		return
	}
	// set the ns so it can be used for metrics
	ns = podns
	if hostIP != localhost {
		klog.Errorf("request remote address is not from a host")
		http.Error(w, "request remote address is not from a host", http.StatusInternalServerError)
		return
	}
	if !tokenRequest.ValidateResourceParamExists() {
		klog.Warning("parameter resource cannot be empty")
		http.Error(w, "parameter resource cannot be empty", http.StatusBadRequest)
		return
	}

	podID, err := s.TokenClient.GetIdentities(r.Context(), podns, podname, tokenRequest.ClientID, tokenRequest.ResourceID)
	if err != nil {
		klog.Errorf("failed to get identities, error: %+v", err)
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}
	tokens, err := s.TokenClient.GetTokens(r.Context(), tokenRequest.ClientID, tokenRequest.Resource, *podID)
	if err != nil {
		klog.Errorf("failed to get service principal token for pod:%s/%s, error: %+v", podns, podname, err)
		http.Error(w, err.Error(), http.StatusForbidden)
		return
	}
	nmiResp := NMIResponse{
		Token:    newMSIResponse(*tokens[0]),
		ClientID: podID.Spec.ClientID,
	}
	response, err := json.Marshal(nmiResp)
	if err != nil {
		klog.Errorf("failed to marshal service principal token and clientid for pod:%s/%s, error: %+v", podns, podname, err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	_, _ = w.Write(response)
	return
}

// msiResponse marshals in a format that matches the underlying
// metadata endpoint more closely. This increases compatibility
// with callers built on older versions of adal client libraries.
type msiResponse struct {
	AccessToken  string `json:"access_token"`
	RefreshToken string `json:"refresh_token"`

	ExpiresIn string `json:"expires_in"`
	ExpiresOn string `json:"expires_on"`
	NotBefore string `json:"not_before"`

	Resource string `json:"resource"`
	Type     string `json:"token_type"`
}

func newMSIResponse(token adal.Token) msiResponse {
	return msiResponse{
		AccessToken:  token.AccessToken,
		RefreshToken: token.RefreshToken,
		ExpiresIn:    token.ExpiresIn.String(),
		ExpiresOn:    token.ExpiresOn.String(),
		NotBefore:    token.NotBefore.String(),
		Resource:     token.Resource,
		Type:         token.Type,
	}
}

func (s *Server) isMIC(podNS, rsName string) bool {
	micRegEx := regexp.MustCompile(`^mic-*`)
	if strings.EqualFold(podNS, s.MICNamespace) && micRegEx.MatchString(rsName) {
		return true
	}
	return false
}

func (s *Server) getTokenForExceptedPod(rqClientID, rqResource string) ([]byte, int, error) {
	var token *adal.Token
	var err error
	// ClientID is empty, so we are going to use System assigned MSI
	if rqClientID == "" {
		klog.Infof("fetching token for system assigned MSI")
		token, err = auth.GetServicePrincipalTokenFromMSI(rqResource)
	} else { // User assigned identity usage.
		klog.Infof("fetching token for user assigned MSI for resource: %s", rqResource)
		token, err = auth.GetServicePrincipalTokenFromMSIWithUserAssignedID(rqClientID, rqResource)
	}
	if err != nil {
		// TODO: return the right status code based on the error we got from adal.
		return nil, http.StatusForbidden, fmt.Errorf("failed to get service principal token, error: %+v", err)
	}
	response, err := json.Marshal(newMSIResponse(*token))
	if err != nil {
		return nil, http.StatusInternalServerError, fmt.Errorf("failed to marshal service principal token, error: %+v", err)
	}
	return response, http.StatusOK, nil
}

// msiHandler uses the remote address to identify the pod ip and uses it
// to find a matching client id, and then returns the token sourced through
// AAD using adal
// if the requests contains client id it validates it against the admin
// configured id.
func (s *Server) msiHandler(w http.ResponseWriter, r *http.Request) (ns string) {
	if s.MetadataHeaderRequired && parseMetadata(r) != "true" {
		klog.Errorf("metadata header is not specified, req.method=%s reg.path=%s req.remote=%s", r.Method, r.URL.Path, parseRemoteAddr(r.RemoteAddr))
		metadataNotSpecifiedError(w)
		return
	}

	podIP := parseRemoteAddr(r.RemoteAddr)
	tokenRequest := parseTokenRequest(r)

	if podIP == "" {
		klog.Error("request remote address is empty")
		http.Error(w, "request remote address is empty", http.StatusInternalServerError)
		return
	}
	if !tokenRequest.ValidateResourceParamExists() {
		klog.Warning("parameter resource cannot be empty")
		http.Error(w, "parameter resource cannot be empty", http.StatusBadRequest)
		return
	}

	podns, podname, rsName, selectors, err := s.KubeClient.GetPodInfo(podIP)
	if err != nil {
		klog.Errorf("failed to get pod info from pod IP: %s, error: %+v", podIP, err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	// set ns for using in metrics
	ns = podns
	exceptionList, err := s.KubeClient.ListPodIdentityExceptions(podns)
	if err != nil {
		klog.Errorf("getting list of AzurePodIdentityException in %s namespace failed with error: %+v", podns, err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// If its mic, then just directly get the token and pass back.
	if pod.IsPodExcepted(selectors.MatchLabels, *exceptionList) || s.isMIC(podns, rsName) {
		klog.Infof("exception pod %s/%s token handling", podns, podname)
		response, errorCode, err := s.getTokenForExceptedPod(tokenRequest.ClientID, tokenRequest.Resource)
		if err != nil {
			klog.Errorf("failed to get service principal token for pod:%s/%s with error code %d, error: %+v", podns, podname, errorCode, err)
			http.Error(w, err.Error(), errorCode)
			return
		}
		_, _ = w.Write(response)
		return
	}

	podID, err := s.TokenClient.GetIdentities(r.Context(), podns, podname, tokenRequest.ClientID, tokenRequest.ResourceID)
	if err != nil {
		klog.Errorf("failed to get matching identities for pod: %s/%s, error: %+v", podns, podname, err)
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}

	tokens, err := s.TokenClient.GetTokens(r.Context(), tokenRequest.ClientID, tokenRequest.Resource, *podID)
	if err != nil {
		klog.Errorf("failed to get service principal token for pod: %s/%s, error: %+v", podns, podname, err)
		http.Error(w, err.Error(), http.StatusForbidden)
		return
	}

	var v interface{}
	if len(tokens) == 1 {
		v = newMSIResponse(*tokens[0])
	} else {
		var msiResp []msiResponse
		for _, token := range tokens {
			msiResp = append(msiResp, newMSIResponse(*token))
		}
		v = msiResp
	}

	response, err := json.Marshal(v)
	if err != nil {
		klog.Errorf("failed to marshal service principal token for pod: %s/%s, error: %+v", podns, podname, err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	_, _ = w.Write(response)
	return
}

// Error replies to the request without the specified metadata header.
// It does not otherwise end the request; the caller should ensure no further
// writes are done to w.
func metadataNotSpecifiedError(w http.ResponseWriter) {
	metadataResp := MetadataResponse{
		Error:            "invalid_request",
		ErrorDescription: "Required metadata header not specified",
	}
	response, err := json.Marshal(metadataResp)
	if err != nil {
		klog.Errorf("failed to marshal metadata response, %+v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(http.StatusBadRequest)
	fmt.Fprintln(w, string(response))
}

func parseMetadata(r *http.Request) (metadata string) {
	return r.Header.Get("metadata")
}

func parsePodInfo(r *http.Request) (podns string, podname string) {
	podns = r.Header.Get("podns")
	podname = r.Header.Get("podname")

	return podns, podname
}

func parseRemoteAddr(addr string) string {
	n := strings.IndexByte(addr, ':')
	if n <= 1 {
		return ""
	}
	hostname := addr[0:n]
	if net.ParseIP(hostname) == nil {
		return ""
	}
	return hostname
}

// TokenRequest contains the client and resource ID token, as well as what resource the client is trying to access.
type TokenRequest struct {
	// ClientID identifies, by Azure AD client ID, a specific identity to use
	// when authenticating to Azure AD. It is mutually exclusive with
	// MsiResourceID.
	// Example: 77788899-f67e-42e1-9a78-89985f6bff3e
	ClientID string

	// MsiResourceID identifies, by urlencoded ARM resource ID, a specific
	// identity to use when authenticating to Azure AD. It is mutually exclusive
	// with ClientID.
	// Example: /subscriptions/<subid>/resourcegroups/<resourcegroup>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>
	ResourceID string

	// Resource is the urlencoded URI of the resource for the requested AD token.
	// Example: https://vault.azure.net.
	Resource string
}

// ValidateResourceParamExists returns true if there exists a resource parameter from the request.
func (r TokenRequest) ValidateResourceParamExists() bool {
	// check if resource exists in the request
	// if resource doesn't exist in the request, then adal libraries will return the same error
	// IMDS also returns an error with 400 response code if resource parameter is empty
	// this is done to emulate same behavior observed while requesting token from IMDS
	return len(r.Resource) != 0
}

func parseTokenRequest(r *http.Request) (request TokenRequest) {
	vals := r.URL.Query()
	if vals != nil {
		// These are mutually exclusive values (client_id, msi_resource_id)
		request.ClientID = vals.Get("client_id")
		request.ResourceID = vals.Get("msi_res_id")

		request.Resource = vals.Get("resource")
	}
	return request
}

// defaultPathHandler creates a new request and returns the response body and code
func (s *Server) defaultPathHandler(w http.ResponseWriter, r *http.Request) (ns string) {
	if s.MetadataHeaderRequired && parseMetadata(r) != "true" {
		klog.Errorf("metadata header is not specified, req.method=%s reg.path=%s req.remote=%s", r.Method, r.URL.Path, parseRemoteAddr(r.RemoteAddr))
		metadataNotSpecifiedError(w)
		return
	}

	client := &http.Client{}
	req, err := http.NewRequest(r.Method, r.URL.String(), r.Body)
	if err != nil || req == nil {
		klog.Errorf("failed creating a new request for %s, error: %+v", r.URL.String(), err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	host := fmt.Sprintf("%s:%s", s.MetadataIP, s.MetadataPort)
	req.Host = host
	req.URL.Host = host
	req.URL.Scheme = "http"
	if r.Header != nil {
		copyHeader(req.Header, r.Header)
	}
	resp, err := client.Do(req)
	if err != nil {
		klog.Errorf("failed executing request for %s, error: %+v", req.URL.String(), err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		klog.Errorf("failed to read response body for %s, error: %+v", req.URL.String(), err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
	_, _ = w.Write(body)
	return
}

// forbiddenHandler responds to any request with HTTP 403 Forbidden
func forbiddenHandler(w http.ResponseWriter, r *http.Request) {
	http.Error(w, "Request blocked by AAD Pod Identity NMI", http.StatusForbidden)
}

func copyHeader(dst, src http.Header) {
	for k, vv := range src {
		for _, v := range vv {
			dst.Add(k, v)
		}
	}
}

func handleTermination() {
	klog.Info("received SIGTERM, shutting down")

	exitCode := 0
	// clean up iptables
	if err := iptables.DeleteCustomChain(); err != nil {
		klog.Errorf("failed to clean up during shutdown, error: %+v", err)
		exitCode = 1
	}

	// wait for pod to delete
	klog.Info("handled termination, awaiting pod deletion")
	time.Sleep(10 * time.Second)

	klog.Infof("exiting with %v", exitCode)
	os.Exit(exitCode)
}
