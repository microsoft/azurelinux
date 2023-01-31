# Coding Standard
The coding standard followed in this code base is similar in most ways to the
style followed by the Linux kernel. Naturally there are exceptions. Most
notably is the indentation (more on this later). Above all else we ask
that when modifying the code that you follow the most important rule:
check the surrounding code and imitate its style [1].

## C Standard and Compiler Stuff
Code should hold as close to the C99 standard as possible with the exception
that GCC specific extensions are generally accepted. The code must compile
without warnings for the primary target compiler when all warnings are
enabled. If a warning is unavoidable, the offending line must be documented
with an explanation of why said code can not be modified to appease the
compiler [2].

It is worth noting however that this code base has yet to run into a compiler
warning that wasn't the authors fault. It is likely that if you do find
yourself disabling `-Werror` you're probably doing something wrong.

## Comments
There are two acceptable commenting styles: block, line.  Block comments
are used to document a largeish block of code, typically a function. Sometimes
block comments are useful with a function to document a loop or a particularly
tricky part of an algorithm. Line comments are typically a single sentence on a
single line. They provide some brief explanation of a line or two of code.

NOTE: Comments are most useful to convey the purpose, parameters and results
from functions and objects in a system. Excessive use of comments within a
function is indicative of two things: over documentation and code that needs
to be refactored. To combat the first case let's say that it's safe to assume
that your code will be read by competent C programmers. The second case can be
tricky and there's no rule of thumb. Follow your instincts and keep in mind
that excessive line comments are a sort of "code smell" that may mean your
code would benefit from some restructuring.

### Examples
```c
/*
 * This block comment could apply to some function and describe its inner
 * workings.  Notice these sentences have traditional capitalization and
 * punctuation... that's because it has to be read in a way completely
 * unlike the Post-It style content of next-line and line comments.
 */
```
```c
// This is *not* an acceptable block comment.
// Don't do this.
// Please.
```
```c
/* This is a line comment */
```

## Whitespace
All indentation must be spaces, not tabs. Lines are indented in multiples of
4 spaces. Each line of code and documentation will end with a non-whitespace
character. There must *not* be any whitespace between the last line of code
or documentation in a file and the end of the file.

## Naming Variables, Functions and Other Stuff
Names should clearly convey the purpose of whatever is being named. While the
data type of a variable conveys some information, this alone is insufficient.
Multiple word names are descriptive and most easily read if words are
separated with the underscore character, "_".

Variable and function names must be lowercase. Words in each name must be
separated by an underscore character: "_". Macros and constants (anything
declared with \#define) must be in all-caps, again with words separated by
underscores.

Objects created using the GObject system follow the GObject naming convention
with individual words in object names as upper case characters.

### Exceptions
Exceptions to these rules are made for compliance with the TCG
specifications. All function names, parameters, and other data types must
be implemented faithfully to the specification and so may violate the naming
conventions defined here.

### Examples
```c
unsigned int table_index = find_index(jacket_table, "color", COLOR_RED);
```
```c
int last_item = 0;
while (!last_item) {
     /* ... */
}
```
```c
int char_found = is_alpha (c);
```

Single letter variable names should be avoided.  Exceptions are:
* "i", "j", and "k" are loop counters or temporary array indexes
* "m" and "n" are row and column indexes for multidimensional arrays
* "c" and "s" are temporary/parameter characters or strings
* "r", "g", "b", and "a" are red, green, blue, and alpha levels, but only when
* they are used together
* "x", "y", and "z" are coordinate values

Abbreviated words in variable names should be avoided.  Exceptions are:
* "char" = character
* "col" = column.  Typically there is also "row" so it is not confused with color
* "cnt" = count
* "pos" = position
* "rem" = remainder
* "ctx" = context

Function names should follow the naming conventions of variables and clearly
describe not only what the function does, but also the nature of what it
returns (if anything). Functions that return boolean integers should be named
to reflect the true condition even if they are created to detect false
conditions. Functions should never be hidden in conditional statements, with
the exception of loops where it makes the code more simple.
```c
bool is_number_prime = is_prime(i);
```
```c
if (is_number_prime) {
    /* ... */
}
```
```c
while (!labeled_correctly(sample[i])) {
    /* ... */
}
```

A function that is exported for use in multiple source files should be
prefixed with the source file (or object module) name where it is defined.
For example, the file list.c may contain the implementation of a dynamic
list ADT including an exported method for creating a list instance and an
internal (static) method for overflow checking. The first function might be
named "list_create", and the second, "is_overflowed".

The use of the static keyword when defining functions is a useful way to scope
the visibility of the function to the same translation unit. A negative side
effect of this is preventing the testing of the function through the unit
testing harness. Generally we accept exposing symbols to get better test
coverage.

## Files
Typically every header file has the same base filename as an associated source
file. Exceptions to this rule are generally limited to modules that will
expose a separate set symbols to external consumers. In this case the internal
version of the header should be suffixed with '-priv'.

Files names are formatted in the same way as described above with the
exception of hyphens "-" separating words.

The body of each header file must be surrounded by an include guard (aka
"header guard"). These guards shall be given the same name as the file in
which they reside. Their names shall be all caps, with words separated by
the underscore character "_".

Header files should never define functions or variables.

Header files should only \#include what is necessary to allow a file that
includes it to compile.  Associated source files will always \#include the
header of the same name, but should \#include files whose resources are used
within the source even if they are already included in that header. This
provides a complete context for readers of the source file... i.e., they
don't have to search through headers to determine where a resource came from.

Files included by all source files must conform to the following format and
order. Each entry in the list below defines a contiguous block of `include`
directives separated by a blank line:
* System headers - These are headers provided by the core c libraries
(typically from libc).
* External dependencies - These are headers installed on the platform defining
interfaces to external libraries.
* Standard TSS2 headers - These are headers that define the public TSS2 types
and interfaces. They are all located under $(srcdir)/include/* and will be
installed as part of the `install` build target. These *must* be included
using the quoted include variant (using `"` instead of the angle brackets).
* Internal headers - These are headers defining the interfaces to code modules
that are internal to the project.

Headers in each block must listed in alphabetical order.

### Example
header: `example-module.h`
```
/*
 * BSD license block
 */
#ifndef EXAMPLE_MODULE_H
#define EXAMPLE_MODULE_H

#include <stdint.h>
#include <sys/types.h>

#include "tss2/tss2_tpm2_types.h"

#include "internal-module.h"

/*
 * preprocess or directives and declarations using stuff from included headers
 */

#endif /* EXAMPLE_MODULE_H */
```

implementation: `example-module.c`
```
/*
 * BSD license block
 */
#include <inttypes.h>
#include <stdint.h>

#include <foo/bar.h>

#include "tss2/tss2_tcti.h"
#include "tss2/tss2_tpm2_types.h"

#include "example-module.h"
#include "internal-module.h"

/*
 * Implementation / code using headers listed above.
 */
```

## Types
Types shall be selected for their use case. Variables should only be of a
signed type if something should ever be negative. A common, incorrect use, is
to declare loop counters as int instead of unsigned, or to use an int to hold
the size of some object.

## Formatting
Always use space characters, 4 spaces per level of indentation.

Conditional statements (such as if, else, while, for, switch, etc) must place
the opening brace on the same line after the end of the control flow statement.
The closing brace should be placed at the same column position as the beginning
of the associated control flow statement on a line by itself.

Function definitions specify the return type on a line, followed by the
function name followed by the first parameter. Each additional parameter is
listed on a separate line aligned with the line above. The opening brace
defning the functions scope must be on the following line at column position 0.

A space must separate a control flow statement or function and the opening
parenthesis.

Line length should not exceed 80 characters and should be split on the nearest
whitespace or delimiter character. When splitting lines with

### Example
```c
if (some_int > 0) {
    statement1;
    statement2;
}
```
```c
void
some_function (short_t       arg_1,
               longer_name_t arg_2)
{
    statement1;
    statement2;
}
```
```c
some_long_variable_name =
    some_long_function_name (lots_of_parameters_1, lots_of_parameters_2);
```
```c
some_long_variable_name = some_long_function_name (lots_of_parameters_1,
                                                   lots_of_parameters_2,
                                                   lots_of_parameters_3);
```
These formatting conditions are contrary to Kernighan and Ritchie's "one true brace style" [3].

## References
1. GNOME C Coding Style : https://developer.gnome.org/programming-guidelines/stable/c-coding-style.html.en
2. Alan Bridger, Mick Brooks, and Jim Pisano, C Coding Standards, 2001, http://www.alma.nrao.edu/development/computing/docs/joint/0009/2001-02-28.pdf
3. Brian Kernighan, Dennis Ritchie, The C Programing Language, 1988
