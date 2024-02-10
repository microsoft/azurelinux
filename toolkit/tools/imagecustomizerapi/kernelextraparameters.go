package imagecustomizerapi

import (
	"bytes"
	"fmt"
	"strings"
)

// KernelExtraParameters defines one or more extra kernel parameters.
type KernelExtraParameters string

func (e KernelExtraParameters) IsValid() error {
	err := validateKernelParametersFormat(string(e))
	if err != nil {
		return err
	}

	return nil
}

// if escapedCharacters is empty, it means always escape the next character.
// if escapedCharacters is not empty, it means escape only if the next
// character is one of escapedCharacters.
func processEscapedCharacter(text string, start int, count int, escapedCharacters string) (lastProcessed int, err error) {
	i := start + 1
	if i < count {
		if len(escapedCharacters) == 0 || bytes.IndexByte([]byte(escapedCharacters), text[i]) != -1 {
			// character is meant to be escaped
			return i, nil
		} else {
			// character is not meant to be escaped
			return start, nil
		}
	}
	return i, fmt.Errorf("missing escaped character. '\\' must be followed by a character.")
}

func processDoubleQuotedString(text string, start int, count int) (lastProcessed int, err error) {
	i := start + 1
	for i < count {
		switch {
		case text[i] == '\\':
			i, err = processEscapedCharacter(text, i, count, "$\"\\n")
			if err != nil {
				return i, err
			}
		default:
			if text[i] == '"' {
				return i, nil
			}
		}
		i++
	}
	return i, fmt.Errorf("invalid double-quoted string. Missing closing double-quotes.")
}

func processSingleQuotedString(text string, start int, count int) (lastProcessed int, err error) {
	i := start + 1
	for i < count {
		if text[i] == '\'' {
			return i, nil
		}
		i++
	}
	return i, fmt.Errorf("invalid single-quoted string. Missing closing single-quote.")
}

func validateQuotedSubstrings(kernelParameters string) (err error) {
	count := len(kernelParameters)
	for i := 0; i < count; i++ {
		switch {
		case kernelParameters[i] == '"':
			i, err = processDoubleQuotedString(kernelParameters, i, count)
			if err != nil {
				return err
			}
		case kernelParameters[i] == '\'':
			i, err = processSingleQuotedString(kernelParameters, i, count)
			if err != nil {
				return err
			}
		case kernelParameters[i] == '\\':
			i, err = processEscapedCharacter(kernelParameters, i, count, "" /*skip all*/)
			if err != nil {
				return err
			}
		}
	}
	return nil
}

func validateKernelParametersFormat(kernelParameters string) (err error) {
	// Disallow special characters to avoid breaking the grub.cfg file.
	// In addition, disallow the "`" character, since it is used as the sed
	// escape character by `installutils.setGrubCfgAdditionalCmdLine()`.
	if strings.ContainsAny(kernelParameters, "\n$`") {
		return fmt.Errorf("the ExtraCommandLine value contains invalid characters")
	}

	err = validateQuotedSubstrings(kernelParameters)
	if err != nil {
		return err
	}

	return nil
}
