// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package hostnameview

import (
	"fmt"
	"strings"

	"github.com/gdamore/tcell"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/navigationbar"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uiutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/randomization"
)

// Input validation constants.
const (
	defaultHostNamePrefix = "cbl-mariner"
	maxHostNameLength     = 63
)

// UI constants.
const (
	// default to <Next>
	defaultNavButton = 1

	formProportion = 0

	navBarHeight     = 0
	navBarProportion = 1
)

// HostNameView contains the hostname UI
type HostNameView struct {
	form         *tview.Form
	nameField    *tview.InputField
	navBar       *navigationbar.NavigationBar
	flex         *tview.Flex
	centeredFlex *tview.Flex
	defaultName  string
}

// New creates and returns a new HostNameView.
func New() *HostNameView {
	return &HostNameView{}
}

// Initialize initializes the view.
func (hv *HostNameView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	hostname, err := randomHostname(defaultHostNamePrefix)
	if err != nil {
		return
	}
	hv.defaultName = hostname

	hv.nameField = tview.NewInputField().
		SetLabel(uitext.HostNameInputLabel).
		SetFieldWidth(maxHostNameLength).
		SetAcceptanceFunc(
			func(textToCheck string, lastChar rune) bool {

				if len(textToCheck) > maxHostNameLength {
					return false
				}

				if !validFQDNCharacter(lastChar, len(textToCheck) == 1) {
					return false
				}

				hv.navBar.ClearUserFeedback()
				return true
			})

	hv.form = tview.NewForm().
		SetButtonsAlign(tview.AlignCenter).
		AddFormItem(hv.nameField)

	hv.navBar = navigationbar.NewNavigationBar().
		AddButton(backButtonText, previousPage).
		AddButton(uitext.ButtonNext, func() {
			enteredHostname := hv.nameField.GetText()

			err := validateFQDN(enteredHostname)
			if err == nil {
				sysConfig.Hostname = enteredHostname
				nextPage()
			} else {
				hv.navBar.SetUserFeedback(uiutils.ErrorToUserFeedback(err), tview.Styles.TertiaryTextColor)
			}
		}).
		SetAlign(tview.AlignCenter)

	formWidth, formHeight := uiutils.MinFormSize(hv.form)
	centeredForm := uiutils.CenterHorizontally(formWidth, hv.form)
	centeredNav := uiutils.CenterHorizontally(formWidth, hv.navBar)

	hv.flex = tview.NewFlex().
		SetDirection(tview.FlexRow).
		AddItem(centeredForm, formHeight, formProportion, true).
		AddItem(centeredNav, navBarHeight, navBarProportion, false)

	hv.centeredFlex = uiutils.CenterVerticallyDynamically(hv.flex)

	// Box styling
	hv.centeredFlex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)

	err = hv.Reset()
	return
}

// HandleInput handles custom input.
func (hv *HostNameView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	if hv.navBar.UnfocusedInputHandler(event) {
		return nil
	}

	return event
}

// Reset resets the page, undoing any user input.
func (hv *HostNameView) Reset() (err error) {
	hv.navBar.ClearUserFeedback()
	hv.navBar.SetSelectedButton(defaultNavButton)
	hv.nameField.SetText(hv.defaultName)

	return
}

// Name returns the friendly name of the view.
func (hv *HostNameView) Name() string {
	return "HOSTNAME"
}

// Title returns the title of the view.
func (hv *HostNameView) Title() string {
	return uitext.HostNameTitle
}

// Primitive returns the primary primitive to be rendered for the view.
func (hv *HostNameView) Primitive() tview.Primitive {
	return hv.centeredFlex
}

// OnShow gets called when the view is shown to the user
func (hv *HostNameView) OnShow() {
}

func validFQDNCharacter(r rune, isFirstRune bool) bool {
	if (r >= 'a' && r <= 'z') || (r >= 'A' && r <= 'Z') {
		return true
	}

	if !isFirstRune {
		if (r >= '0' && r <= '9') || (r == '.') || (r == '-') {
			return true
		}
	}

	return false
}

func validateFQDN(fqdn string) (err error) {
	var (
		hostname      string
		domainName    string
		hasDomainName bool
	)

	if len(fqdn) > maxHostNameLength {
		err = fmt.Errorf(uitext.FQDNInvalidLengthErrorFmt, maxHostNameLength)
		return
	}

	if strings.Contains(fqdn, ".") {
		hostAndDomainName := strings.SplitN(fqdn, ".", 2)
		hostname = hostAndDomainName[0]
		domainName = hostAndDomainName[1]
		hasDomainName = true
	} else {
		hostname = fqdn
	}

	namesToCheck := []string{hostname}

	if hasDomainName {
		namesToCheck = append(namesToCheck, domainName)
	}

	for i, name := range namesToCheck {
		var segmentName string
		if i == 0 {
			segmentName = uitext.HostNameSegment
		} else {
			segmentName = uitext.DomainNameSegment
		}

		// May not have empty segments in the FQDN
		if name == "" {
			return fmt.Errorf(uitext.FQDNEmptyErrorFmt, segmentName)
		}

		firstLetter := name[0]
		lastLetter := name[len(name)-1]

		// First letter must be one of [A-Za-z]
		if !validFQDNCharacter(rune(firstLetter), true) {
			return fmt.Errorf(uitext.FQDNInvalidStartErrorFmt, segmentName)
		}

		if lastLetter == '-' {
			return fmt.Errorf(uitext.FQDNEndsInDashErrorFmt, segmentName)
		}

		for _, r := range name {
			if !validFQDNCharacter(r, false) {
				return fmt.Errorf(uitext.FQDNInvalidRuneErrorFmt, segmentName)
			}
		}
	}

	return
}

// randomHostname generates a random hostname that starts with prefix.
func randomHostname(prefix string) (hostname string, err error) {
	const postfixLength = 12

	postfix, err := randomization.RandomString(postfixLength, randomization.LegalCharactersAlphaNum)
	if err != nil {
		return
	}

	hostname = fmt.Sprintf("%s-%s", prefix, postfix)

	return
}
