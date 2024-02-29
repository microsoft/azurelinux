// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package userview

import (
	"fmt"

	"github.com/gdamore/tcell"
	"github.com/muesli/crunchy"
	"github.com/rivo/tview"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/primitives/navigationbar"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uitext"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/attendedinstaller/uiutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
)

// UI constants.
const (
	navButtonNext = 1
	noSelection   = -1

	formProportion = 0

	navBarHeight     = 0
	navBarProportion = 1

	passwordFieldWidth = 64

	maxUserNameLength = 32
)

// UserView contains the password UI
type UserView struct {
	form                 *tview.Form
	userNameField        *tview.InputField
	passwordField        *tview.InputField
	confirmPasswordField *tview.InputField
	navBar               *navigationbar.NavigationBar
	flex                 *tview.Flex
	centeredFlex         *tview.Flex
	passwordValidator    *crunchy.Validator

	user *configuration.User
}

// New creates and returns a new UserView.
func New() *UserView {
	return &UserView{
		passwordValidator: crunchy.NewValidator(),
	}
}

// Initialize initializes the view.
func (uv *UserView) Initialize(backButtonText string, sysConfig *configuration.SystemConfig, cfg *configuration.Config, app *tview.Application, nextPage, previousPage, quit, refreshTitle func()) (err error) {
	err = uv.setupConfigUsers(sysConfig)
	if err != nil {
		return
	}

	uv.userNameField = tview.NewInputField().
		SetLabel(uitext.UserNameInputLabel).
		SetFieldWidth(maxUserNameLength).
		SetAcceptanceFunc(uv.userNameAcceptanceCheck)

	uv.passwordField = tview.NewInputField().
		SetFieldWidth(passwordFieldWidth).
		SetLabel(uitext.PasswordInputLabel).
		SetMaskCharacter('*')

	uv.confirmPasswordField = tview.NewInputField().
		SetFieldWidth(passwordFieldWidth).
		SetLabel(uitext.ConfirmPasswordInputLabel).
		SetMaskCharacter('*')

	uv.navBar = navigationbar.NewNavigationBar().
		AddButton(backButtonText, previousPage).
		AddButton(uitext.ButtonNext, func() {
			uv.onNextButton(nextPage)
		}).
		SetAlign(tview.AlignCenter).
		SetOnFocusFunc(func() {
			uv.navBar.SetSelectedButton(navButtonNext)
		}).
		SetOnBlurFunc(func() {
			uv.navBar.SetSelectedButton(noSelection)
		})

	uv.form = tview.NewForm().
		SetButtonsAlign(tview.AlignCenter).
		AddFormItem(uv.userNameField).
		AddFormItem(uv.passwordField).
		AddFormItem(uv.confirmPasswordField).
		AddFormItem(uv.navBar)

	uv.flex = tview.NewFlex().
		SetDirection(tview.FlexRow)

	formWidth, formHeight := uiutils.MinFormSize(uv.form)
	centeredForm := uiutils.CenterHorizontally(formWidth, uv.form)

	uv.flex.AddItem(centeredForm, formHeight+uv.navBar.GetHeight(), formProportion, true)
	uv.centeredFlex = uiutils.CenterVerticallyDynamically(uv.flex)

	// Box styling
	uv.centeredFlex.SetBackgroundColor(tview.Styles.PrimitiveBackgroundColor)

	return
}

// HandleInput handles custom input.
func (uv *UserView) HandleInput(event *tcell.EventKey) *tcell.EventKey {
	// Allow Up-Down to navigate the form
	switch event.Key() {
	case tcell.KeyUp:
		return tcell.NewEventKey(tcell.KeyBacktab, 0, tcell.ModNone)
	case tcell.KeyDown:
		return tcell.NewEventKey(tcell.KeyTab, 0, tcell.ModNone)
	}

	return event
}

// Reset resets the page, undoing any user input.
func (uv *UserView) Reset() (err error) {
	uv.navBar.ClearUserFeedback()
	uv.navBar.SetSelectedButton(noSelection)
	uv.form.SetFocus(0)

	uv.user.Name = ""
	uv.user.Password = ""

	return
}

// Name returns the friendly name of the view.
func (uv *UserView) Name() string {
	return "USERACCOUNT"
}

// Title returns the title of the view.
func (uv *UserView) Title() string {
	return uitext.SetupUserTitle
}

// Primitive returns the primary primitive to be rendered for the view.
func (uv *UserView) Primitive() tview.Primitive {
	return uv.centeredFlex
}

// OnShow gets called when the view is shown to the user
func (uv *UserView) OnShow() {
}

func (uv *UserView) setupConfigUsers(sysConfig *configuration.SystemConfig) (err error) {
	const (
		rootUserName = "root"
		sudoersGroup = "wheel"
		newUserIndex = 1
	)

	// The configuration provided by the attended installer should have an empty users section, no other view should have filled in this information.
	if len(sysConfig.Users) != 0 {
		return fmt.Errorf("unsupported configuration, expected no users")
	}

	// To setup the user account:
	// 1) Create a passwordless-root account
	// 2) Create the requested user account
	// 3) Give the new user account sudo privileges
	rootUser := configuration.User{
		Name: rootUserName,
	}

	// Give the user a secondary group of wheel:
	// The User's primary group should remain the default value -- its user name.
	newUser := configuration.User{
		SecondaryGroups: []string{sudoersGroup},
	}

	sysConfig.Users = []configuration.User{rootUser, newUser}
	uv.user = &sysConfig.Users[newUserIndex]

	return
}

func (uv *UserView) userNameAcceptanceCheck(textToCheck string, lastRune rune) bool {
	uv.navBar.ClearUserFeedback()

	err := validateUserName(textToCheck)
	if err != nil {
		uv.navBar.SetUserFeedback(uiutils.ErrorToUserFeedback(err), tview.Styles.TertiaryTextColor)
		return false
	}

	err = validateUserNameRune(lastRune, len(textToCheck) == 1)
	if err != nil {
		uv.navBar.SetUserFeedback(uiutils.ErrorToUserFeedback(err), tview.Styles.TertiaryTextColor)
		return false
	}

	return true
}

func (uv *UserView) onNextButton(nextPage func()) {
	enteredUserName := uv.userNameField.GetText()
	enteredPassword := uv.passwordField.GetText()
	uv.navBar.ClearUserFeedback()

	err := validateUserName(enteredUserName)
	if err != nil {
		uv.navBar.SetUserFeedback(uiutils.ErrorToUserFeedback(err), tview.Styles.TertiaryTextColor)
		return
	}

	if enteredPassword != uv.confirmPasswordField.GetText() {
		uv.navBar.SetUserFeedback(uitext.PasswordMismatchFeedback, tview.Styles.TertiaryTextColor)
		return
	}

	err = uv.passwordValidator.Check(enteredPassword)
	if err != nil {
		uv.navBar.SetUserFeedback(uiutils.ErrorToUserFeedback(err), tview.Styles.TertiaryTextColor)
		return
	}

	uv.user.Name = enteredUserName
	uv.user.Password = enteredPassword
	nextPage()
}

func validateUserName(userName string) (err error) {
	const isFirstRune = true

	if userName == "" {
		return fmt.Errorf(uitext.UserNameEmptyError)
	}

	if len(userName) > maxUserNameLength {
		return fmt.Errorf(uitext.UserNameInvalidLengthErrorFmt, maxUserNameLength)
	}

	firstRune := userName[0]

	// Only check the first and last rune for special cases.
	// The rest of the username is validated by the userNameField's AcceptanceFunc
	err = validateUserNameRune(rune(firstRune), isFirstRune)
	if err != nil {
		return
	}

	return
}

func validateUserNameRune(r rune, isFirstRune bool) (err error) {
	if (r >= 'a' && r <= 'z') || (r >= 'A' && r <= 'Z') || (r >= '0' && r <= '9') || r == '_' {
		return
	}

	if !isFirstRune && (r == '-' || r == '.') {
		return
	}

	if isFirstRune {
		return fmt.Errorf(uitext.UserNameInvalidStartError)
	}

	return fmt.Errorf(uitext.UserNameInvalidRuneError)
}
