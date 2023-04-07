# Image Config Schema

## Structs

Each newly added component of the imageconfig schema should be defined in its own file as its own Go type.

From [kernelcommandline.go](../../tools/imagegen/configuration/kernelcommandline.go):

```go
// KernelCommandLine holds extra command line parameters which can be
// added to the grub config file.
//   - ImaPolicy: A list of IMA policies which will be used together
//   - ExtraCommandLine: Arbitrary parameters which will be appended to the
//     end of the kernel command line
type KernelCommandLine struct {
    CGroup           CGroup      `json:"CGroup"`
    ImaPolicy        []ImaPolicy `json:"ImaPolicy"`
    SELinux          SELinux     `json:"SELinux"`
    ExtraCommandLine string      `json:"ExtraCommandLine"`
}
```

## JSON Parsing

Each type should have its own copy of `UnmarshalJSON()` defined, which calls the type's `IsValid()` function.

```go
// UnmarshalJSON Unmarshals a KernelCommandLine entry
func (k *KernelCommandLine) UnmarshalJSON(b []byte) (err error) {
    // Use an intermediate type which will use the default JSON unmarshal implementation
    type IntermediateTypeKernelCommandLine KernelCommandLine
    err = json.Unmarshal(b, (*IntermediateTypeKernelCommandLine)(k))
    if err != nil {
        return fmt.Errorf("failed to parse [KernelCommandLine]: %w", err)
    }

    // Now validate the resulting unmarshaled object
    err = k.IsValid()
    if err != nil {
        return fmt.Errorf("failed to parse [KernelCommandLine]: %w", err)
    }
    return
}

```

## Validation

Each type should also implement `IsValid()`, which validates the current types configuration as well as recursively calls each child component's `IsValid()`. This function is used in two places, the JSON unmarshal flow, as well as the image [config validator tool](../how_it_works/1_initial_prep.md#imageconfigvalidator) which calls the root configuration structure's `IsValid()`.

```go
// GetSedDelimeter returns the delimeter which should be used with sed
// to find/replace the command line strings.
func (k *KernelCommandLine) GetSedDelimeter() (delimeter string) {
    return "`"
}

// IsValid returns an error if the KernelCommandLine is not valid
func (k *KernelCommandLine) IsValid() (err error) {
    err = k.CGroup.IsValid()
    if err != nil {
        return err
    }

    for _, ima := range k.ImaPolicy {
        if err = ima.IsValid(); err != nil {
            return
        }
    }

    err = k.SELinux.IsValid()
    if err != nil {
        return err
    }

    // A character needs to be set aside for use as the sed delimiter, make sure it isn't included in the provided string
    if strings.Contains(k.ExtraCommandLine, k.GetSedDelimeter()) {
        return fmt.Errorf("ExtraCommandLine contains character %s which is reserved for use by sed", k.GetSedDelimeter())
    }

    return
}
```

## Unit Tests

Where possible, all components should have an associated test file (for example [kernelcommandline_test.go](../../tools/imagegen/configuration/kernelcommandline_test.go)). These tests are invoked when building the go tools.

```bash
# Run the tests and build the tools
sudo make go-tools REBUILD_TOOLS=y

# Generate a coverage report at ../toolkit/out/tools/test_coverage_report.html
sudo make go-test-coverage
```

### Unit Test Implementations

#### Common Variables

Each test will generally have something along the lines of:

* A valid structure with parameters filled in with dummy data
* Some invalid inputs
* A valid JSON input (often simplified)
* An invalid JSON input
* A config with one sub component that is invalid

From [kernelcommandline_test.go](../../tools/imagegen/configuration/kernelcommandline_test.go):

```go
var (
    validCommandLine KernelCommandLine = KernelCommandLine{
        ImaPolicy: []ImaPolicy{
            ImaPolicyTcb,
        },
        ExtraCommandLine: "param1=value param2=\"value2 value3\"",
        SELinux:          "permissive",
        CGroup:           "version_two",
    }
    invalidExtraCommandLine     = "invalid=`delim`"
    validExtraComandLineJSON    = `{"ImaPolicy": ["tcb"], "ExtraCommandLine": "param1=value param2=\"value2 value3\"", "SELinux": "permissive", "CGroup": "version_two"}`
    invalidExtraComandLineJSON1 = `{"ImaPolicy": [ "not-an-ima-policy" ]}`
    invalidExtraComandLineJSON2 = `{"ExtraCommandLine": "` + invalidExtraCommandLine + `"}`
)
```

Types that are similar to enums will generally also have the following tests:

From [imapolicy_test.go](../../tools/imagegen/configuration/imapolicy_test.go)

```go
var (
    validImaPolicies = []ImaPolicy{
        ImaPolicy("tcb"),
        ImaPolicy("appraise_tcb"),
        ImaPolicy("secure_boot"),
        ImaPolicy(""),
    }
)

func TestShouldSucceedValidImaPoliciesMatch_ImaPolicy(t *testing.T) {
    var ima ImaPolicy
    assert.Equal(t, len(validImaPolicies), len(ima.GetValidImaPolicies()))

    for _, imaPolicy := range validImaPolicies {
        found := false
        for _, validImaPolicy := range ima.GetValidImaPolicies() {
            if imaPolicy == validImaPolicy {
                found = true
            }
        }
        assert.True(t, found)
    }
}
```

Many of these test files will define a `valid<TYPE> <TYPE> = <TYPE>{ ... }` variable at the top of the file. This variable should be handled carefully because modifying it in a test can pollute the variable for other tests. You will often see something along the lines of:

```go
    testConfig := validConfig
    // Copy the current elements, then mangle one by adding a bad flag
    badElements := append([]Element{}, testConfig.Elements...)
    testConfig.Elements = badElements
    testConfig.Elements[0].flags = badFlag
```

This creates a new instance of the list which won't propagate back to the source var.
