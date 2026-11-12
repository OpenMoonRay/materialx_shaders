# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Moonray Project

# if building at the same time as scene_rdl2 we need to get access to the
# scene_rdl2 python module before it is installed so point to it in the
# build directory. Otherwie it should already be in the environment
if (CMAKE_PROJECT_NAME STREQUAL "openmoonray")
    set(PYTHONPATH_WITH_SCENE_RDL2 ${CMAKE_BINARY_DIR}/moonray/scene_rdl2/mod/python/py_scene_rdl2:$ENV{PYTHONPATH})
elseif (CMAKE_PROJECT_NAME STREQUAL "openmoonray_dwa")
    set(PYTHONPATH_WITH_SCENE_RDL2 ${CMAKE_BINARY_DIR}/openmoonray/moonray/scene_rdl2/mod/python/py_scene_rdl2:$ENV{PYTHONPATH})
else()
    set(PYTHONPATH_WITH_SCENE_RDL2 $ENV{PYTHONPATH})
endif()

# This script imports the compiled scene_rdl2 python extension module, which
# dlopen()s sanitizer-instrumented shared libraries when built with
# -fsanitize=address,undefined. The plain python3 interpreter invoked below
# is not itself sanitizer-instrumented, so some lazily-resolved sanitizer
# symbols (e.g. UBSan's vptr type cache) fail to resolve unless the
# sanitizer runtime is preloaded into the interpreter process up front.
set(GENERATE_PYTHON_CREATE_FUNCTIONS_ENV "")
if (CMAKE_EXE_LINKER_FLAGS MATCHES "-fsanitize")
    execute_process(
        COMMAND ${CMAKE_CXX_COMPILER} -print-file-name=libclang_rt.asan.so
        OUTPUT_VARIABLE SANITIZER_RUNTIME_LIB
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    if (EXISTS "${SANITIZER_RUNTIME_LIB}")
        set(GENERATE_PYTHON_CREATE_FUNCTIONS_ENV LD_PRELOAD=${SANITIZER_RUNTIME_LIB})
    endif()
endif()

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/shaders.py
    COMMAND ${CMAKE_COMMAND} -E env PYTHONPATH=${PYTHONPATH_WITH_SCENE_RDL2} RDL2_DSO_PATH=${CMAKE_BINARY_DIR}/rdl2dso:$ENV{RDL2_DSO_PATH} ${GENERATE_PYTHON_CREATE_FUNCTIONS_ENV} ${GENERATE_PYTHON_CREATE_FUNCTIONS}  -o ${CMAKE_CURRENT_BINARY_DIR}/shaders.py
    COMMENT "Generating shaders.py"
    DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/../generate_python_create_functions/generate_python_create_functions"
)

add_custom_target(
	shaders ALL
	DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/shaders.py
)

add_dependencies(shaders all_moonray_dsos)

if (CMAKE_PROJECT_NAME STREQUAL "openmoonray_dwa" OR CMAKE_PROJECT_NAME STREQUAL "openmoonray")
	add_dependencies(shaders scene_rdl2)
endif()

set(python_install_dir
		python/lib/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/${PACKAGE_NAME})

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/shaders.py DESTINATION ${python_install_dir})
