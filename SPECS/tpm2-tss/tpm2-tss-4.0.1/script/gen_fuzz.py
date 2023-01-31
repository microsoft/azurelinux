#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause
import os
import argparse
import itertools

# Makefile-fuzz-generated.am is created from this template.
MAKEFILE_FUZZ = """# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2018 Intel Corporation
# All rights reserved.

if ENABLE_TCTI_FUZZING
TESTS_FUZZ = %s
%s
endif # ENABLE_TCTI_FUZZING
"""
# Each fuzz target in Makefile-fuzz-generated.am is created from this template.
MAKEFILE_FUZZ_TARGET = """
noinst_PROGRAMS += test/fuzz/%s.fuzz
test_fuzz_%s_fuzz_CFLAGS = $(FUZZ_CFLAGS)
test_fuzz_%s_fuzz_LDADD    = $(FUZZLDADD)
nodist_test_fuzz_%s_fuzz_SOURCES  = test/fuzz/main-sys.c \\
        test/fuzz/%s.fuzz.c

DISTCLEANFILES += test/fuzz/%s.fuzz.c"""
# Common include definitions needed for fuzzing an SYS call
SYS_TEMPLATE_HEADER = """/* SPDX-License-Identifier: BSD-2-Clause */
/***********************************************************************
 * Copyright (c) 2018, Intel Corporation
 *
 * All rights reserved.
 ***********************************************************************/
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <poll.h>
#include <stdarg.h>

#include <setjmp.h>

#include "tss2_mu.h"
#include "tss2_sys.h"
#include "tss2_tcti_device.h"

#include "tss2-tcti/tcti-common.h"
#include "tss2-tcti/tcti-device.h"

#define LOGMODULE fuzz
#include "tss2_tcti.h"
#include "util/log.h"
#include "test.h"
#include "test-options.h"
#include "context-util.h"
#include "tss2-sys/sysapi_util.h"
#include "tcti/tcti-fuzzing.h"

int
test_invoke (
        TSS2_SYS_CONTEXT *sysContext)"""
# Template to call a SYS _Complete function which takes no arguments
SYS_COMPLETE_TEMPLATE_NO_ARGS = (
    SYS_TEMPLATE_HEADER
    + """
{
    %s (sysContext);

    return EXIT_SUCCESS;
}
"""
)
# Template to call a SYS _Complete function which takes arguments
SYS_COMPLETE_TEMPLATE_HAS_ARGS = (
    SYS_TEMPLATE_HEADER
    + """
{
    %s

    %s (
        sysContext,
        %s
    );

    return EXIT_SUCCESS;
}
"""
)
# Template to call a SYS _Prepare function
SYS_PREPARE_TEMPLATE_HAS_ARGS = (
    SYS_TEMPLATE_HEADER
    + """
{
    int ret;
    %s

    ret = fuzz_fill (
        sysContext,
        %d,
        %s
    );
    if (ret) {
        return ret;
    }

    %s (
        sysContext,
        %s
    );

    return EXIT_SUCCESS;
}
"""
)


def gen_file(function):
    """
    Generate a c file used as the fuzz target given the function definition
    from a header file.
    """
    # Parse the function name from the function definition
    function_name = (
        function.split("\n")[0].replace("TSS2_RC", "").replace("(", "").strip()
    )
    # Parse the function arguments into an array. Do not include sysContext.
    args = [
        arg.strip()
        for arg in function[function.index("(") + 1 : function.index(");")].split(",")
        if not "TSS2_SYS_CONTEXT" in arg
    ]
    # Prepare and Complete functions require different methods of generation.
    # Call the appropriate function to generate a c target specific to that
    # type of function.
    if "_Complete" in function_name:
        return gen_complete(function, function_name, args)
    if "_Prepare" in function_name:
        return gen_prepare(function, function_name, args)
    raise NotImplementedError("Unknown function type %r" % (function_name,))


def gen_complete(function, function_name, args):
    """
    Generate the c fuzz target for a SYS _Complete call
    """
    if not args:
        # Fill in the no args template. Simple case.
        return function_name, SYS_COMPLETE_TEMPLATE_NO_ARGS % (function_name)
    # Generate the c variable definitions.
    arg_definitions = (";\n" + " " * 4).join(
        [arg.replace("*", "") for arg in args]
    ) + ";"
    # Generate the c arguments. For arguments that are pointers find replace *
    # with & so that we pass a pointer to the definition which has been
    # allocated on the stack.
    arg_call = (",\n" + " " * 8).join(
        [arg.replace("*", "&").split()[-1] for arg in args]
    )
    # Fill in the template
    return (
        function_name,
        SYS_COMPLETE_TEMPLATE_HAS_ARGS % (arg_definitions, function_name, arg_call),
    )


def gen_prepare(function, function_name, args):
    """
    Generate the c fuzz target for a SYS _Prepare call
    """
    if not args:
        return function_name, None
    # Generate the c variable definitions. Make sure to initialize to empty
    # structs (works for initializing anything) or c compiler will complain.
    arg_definitions = (" = {0};\n" + " " * 4).join(
        [arg.replace("*", "").replace("const", "") for arg in args]
    ) + " = {0};"
    # Generate the c arguments. For arguments that are pointers find replace *
    # with & so that we pass a pointer to the definition which has been
    # allocated on the stack.
    arg_call = (",\n" + " " * 8).join(
        [arg.replace("*", "&").split()[-1] for arg in args]
    )
    # Generate the call to fuzz_fill. The call should be the sysContext, double
    # the number of arguments for the _Prepare call, and then for each _Prepare
    # argument pass two to fuzz_fill, the sizeof the _Prepare argument, and a
    # pointer to it.
    fill_fuzz_args = (",\n" + " " * 8).join(
        [
            ("sizeof (%s), &%s" % tuple([arg.replace("*", "").split()[-1]] * 2))
            for arg in args
        ]
    )
    # Fill in the template
    return (
        function_name,
        SYS_PREPARE_TEMPLATE_HAS_ARGS
        % (arg_definitions, len(args) * 2, fill_fuzz_args, function_name, arg_call),
    )


def functions_from_include(header):
    """
    Parse out and yield each function definition from a header file.
    """
    with open(header, "r") as header_fd:
        current_function = ""
        for line in header_fd:
            # Functions we are interested in start with _Complete or _Prepare
            if "_Complete" in line or "_Prepare" in line:
                # Set the current_function to this line
                current_function = line
            elif current_function and ");" in line:
                # When we reach the closing parenthesis yield the function
                yield current_function + line.rstrip()
                current_function = ""
            elif current_function:
                # Add all the arguments to the function
                current_function += line


def gen_files(header):
    # Generate a fuzz target c file from each function in the header file
    for current_function in functions_from_include(header):
        function_name, contents = gen_file(current_function)
        # Skip the yield if there is no fuzz target that can be generated
        if contents is None:
            continue
        # Yield the function name and the contents of its generated file
        yield function_name, contents


def main():
    parser = argparse.ArgumentParser(description="Generate libfuzzer for sys")
    parser.add_argument(
        "--header",
        default="include/tss2/tss2_sys.h",
        help="Header file to look in (default include/tss2/tss2_sys.h)",
    )
    args = parser.parse_args()

    functions = dict(gen_files(args.header))
    # Write the generated target to the file for its function name
    for function_name, contents in functions.items():
        filepath = os.path.join("test", "fuzz", function_name + ".fuzz.c")
        with open(filepath, "w") as fuzzer_fd:
            fuzzer_fd.write(contents)
    # Fill in the Makefile-fuzz-generated.am template using the function names.
    # Create a list of the compiled fuzz targets
    files = " \\\n    ".join(
        ["test/fuzz/%s.fuzz" % (function) for function in functions]
    )
    # Create the Makefile targets for each generated file
    targets = "\n".join(
        [
            MAKEFILE_FUZZ_TARGET % tuple(list(itertools.chain(([function] * 6))))
            for function in functions
        ]
    )
    # Write out the Makefile-fuzz-generated.am file
    with open("Makefile-fuzz-generated.am", "w") as makefile_fd:
        makefile_fd.write(MAKEFILE_FUZZ % (files, targets))


if __name__ == "__main__":
    main()
