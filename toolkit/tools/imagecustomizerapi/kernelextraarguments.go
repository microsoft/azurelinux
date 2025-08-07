package imagecustomizerapi

import (
	"bytes"
	"fmt"
	"strings"
)

/*
	The following code is based on the 'quoting' section in grub
	documentation: https://www.gnu.org/software/grub/manual/grub/grub.html#Quoting

	Here is a copy for convenience:

	There are three quoting mechanisms: the escape character, single quotes, and
	double quotes.

	(1)
	A non-quoted backslash (\) is the escape character. It preserves the literal
	value of the next character that follows, with the exception of newline.

	(2)
	Enclosing characters in single quotes preserves the literal value of each
	character within the quotes.

	(3)
	A single quote may not occur between single
	quotes, even when preceded by a backslash.

	(4)
	Enclosing characters in double quotes preserves the literal value of all
	characters within the quotes, with the exception of ‘$’ and ‘\’.

	(5)
	The ‘$’ character retains its special meaning within double quotes.

	(6)
	The backslash retains its special meaning only when followed by one of the
	following characters: ‘$’, ‘"’, ‘\’, or newline. A backslash-newline pair is
	treated as a line continuation (that is, it is removed from the input stream
	and effectively ignored.

	(7)
	A double quote may be quoted within double quotes by preceding it with a
	backslash.
*/

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
			// In some cases (see (6) above), the escape charater is not meant
			// escape the next character - so, we should not remove the next
			// character from the stream.
			return start, nil
		}
	}
	return i, fmt.Errorf("missing escaped character. '\\' must be followed by a character")
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
	return i, fmt.Errorf("invalid double-quoted string: missing closing double-quotes")
}

func processSingleQuotedString(text string, start int, count int) (lastProcessed int, err error) {
	i := start + 1
	for i < count {
		if text[i] == '\'' {
			return i, nil
		}
		i++
	}
	return i, fmt.Errorf("invalid single-quoted string: missing closing single-quote")
}

func validateQuotedSubstrings(kernelArguments string) (err error) {
	count := len(kernelArguments)
	for i := 0; i < count; i++ {
		switch {
		case kernelArguments[i] == '"':
			i, err = processDoubleQuotedString(kernelArguments, i, count)
			if err != nil {
				return err
			}
		case kernelArguments[i] == '\'':
			i, err = processSingleQuotedString(kernelArguments, i, count)
			if err != nil {
				return err
			}
		case kernelArguments[i] == '\\':
			i, err = processEscapedCharacter(kernelArguments, i, count, "" /*skip all*/)
			if err != nil {
				return err
			}
		}
	}
	return nil
}

func validateKernelArgumentsFormat(kernelArguments string) (err error) {
	// Disallow special characters to avoid breaking the grub.cfg file.
	// In addition, disallow the "`" character, since it is used as the sed
	// escape character by `installutils.setGrubCfgAdditionalCmdLine()`.
	if strings.ContainsAny(kernelArguments, "$`") {
		return fmt.Errorf("the extraCommandLine value contains invalid characters")
	}

	err = validateQuotedSubstrings(kernelArguments)
	if err != nil {
		return err
	}

	return nil
}
