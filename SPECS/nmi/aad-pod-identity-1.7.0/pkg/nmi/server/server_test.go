package server

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"
)

var (
	mux       *http.ServeMux
	server    *httptest.Server
	tokenPath = "/metadata/identity/oauth2/token"
)

func setup() {
	mux = http.NewServeMux()
	server = httptest.NewServer(mux)
}

func teardown() {
	server.Close()
}

func TestMsiHandler_NoMetadataHeader(t *testing.T) {
	setup()
	defer teardown()

	s := &Server{
		MetadataHeaderRequired: true,
	}
	mux.Handle(tokenPath, appHandler(s.msiHandler))

	req, err := http.NewRequest(http.MethodGet, tokenPath, nil)
	if err != nil {
		t.Fatal(err)
	}

	recorder := httptest.NewRecorder()
	mux.ServeHTTP(recorder, req)

	if recorder.Code != http.StatusBadRequest {
		t.Errorf("Unexpected status code %d", recorder.Code)
	}

	resp := &MetadataResponse{
		Error:            "invalid_request",
		ErrorDescription: "Required metadata header not specified",
	}
	expected, err := json.Marshal(resp)
	if err != nil {
		t.Fatal(err)
	}

	if string(expected) != strings.TrimSpace(recorder.Body.String()) {
		t.Errorf("Unexpected response body %s", recorder.Body.String())
	}
}

func TestMsiHandler_NoRemoteAddress(t *testing.T) {
	setup()
	defer teardown()

	s := &Server{
		MetadataHeaderRequired: false,
	}
	mux.Handle(tokenPath, appHandler(s.msiHandler))

	req, err := http.NewRequest(http.MethodGet, tokenPath, nil)
	if err != nil {
		t.Fatal(err)
	}

	recorder := httptest.NewRecorder()
	mux.ServeHTTP(recorder, req)

	if recorder.Code != http.StatusInternalServerError {
		t.Errorf("Unexpected status code %d", recorder.Code)
	}

	expected := "request remote address is empty"
	if expected != strings.TrimSpace(recorder.Body.String()) {
		t.Errorf("Unexpected response body %s", recorder.Body.String())
	}
}

func TestParseTokenRequest(t *testing.T) {
	const endpoint = "http://127.0.0.1/metadata/identity/oauth2/token"

	t.Run("query present", func(t *testing.T) {
		const resource = "https://vault.azure.net"
		const clientID = "77788899-f67e-42e1-9a78-89985f6bff3e"
		const resourceID = "/subscriptions/9f2be85c-f8ae-4569-9353-38e5e8b459ef/resourcegroups/test/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test"

		var r http.Request
		r.URL, _ = url.Parse(fmt.Sprintf("%s?client_id=%s&msi_res_id=%s&resource=%s", endpoint, clientID, resourceID, resource))

		result := parseTokenRequest(&r)

		if result.ClientID != clientID {
			t.Errorf("invalid ClientID - expected: %q, actual: %q", clientID, result.ClientID)
		}

		if result.ResourceID != resourceID {
			t.Errorf("invalid ResourceID - expected: %q, actual: %q", resourceID, result.ResourceID)
		}

		if result.Resource != resource {
			t.Errorf("invalid Resource - expected: %q, actual: %q", resource, result.Resource)
		}
	})

	t.Run("bare endpoint", func(t *testing.T) {
		var r http.Request
		r.URL, _ = url.Parse(endpoint)

		result := parseTokenRequest(&r)

		if result.ClientID != "" {
			t.Errorf("invalid ClientID - expected: %q, actual: %q", "", result.ClientID)
		}

		if result.ResourceID != "" {
			t.Errorf("invalid ResourceID - expected: %q, actual: %q", "", result.ResourceID)
		}

		if result.Resource != "" {
			t.Errorf("invalid Resource - expected: %q, actual: %q", "", result.Resource)
		}
	})
}

func TestTokenRequest_ValidateResourceParamExists(t *testing.T) {
	tr := TokenRequest{
		Resource: "https://vault.azure.net",
	}

	if !tr.ValidateResourceParamExists() {
		t.Error("ValidateResourceParamExists should have returned true when the resource is set")
	}

	tr.Resource = ""
	if tr.ValidateResourceParamExists() {
		t.Error("ValidateResourceParamExists should have returned false when the resource is unset")
	}
}
