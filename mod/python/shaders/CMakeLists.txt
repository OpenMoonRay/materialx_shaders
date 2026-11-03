# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Moonray Project

# If materialx_shaders is being built standalone (its own top-level project),
# scene_rdl2 is located via find_package(SceneRdl2) above and its python
# module is expected to already be in the environment/PYTHONPATH.
#
# If materialx_shaders is instead built in-tree as part of a larger combined
# build (e.g. openmoonray), scene_rdl2 is a sibling add_subdirectory() target
# rather than a found package, so its python module's build-tree location
# needs to be added to PYTHONPATH explicitly, and shaders.py's generation
# needs a real build-order dependency on scene_rdl2's compiled python module.
#
# This reuses the same PROJECT_NAME/CMAKE_PROJECT_NAME comparison the root
# CMakeLists.txt already uses to tell these two cases apart. Unlike checking
# whether a build-tree directory already exists, this is independent of
# add_subdirectory() call order -- it's set the moment this project's own
# project() call runs. The scene_rdl2 python module's actual location/
# dependency is then expressed via $<TARGET_FILE...> generator expressions,
# which CMake only resolves once the whole project's target graph is known
# (after every add_subdirectory() has been processed), so this works no
# matter whether scene_rdl2's add_subdirectory() call comes before or after
# materialx_shaders's.
if (NOT "${PROJECT_NAME}" STREQUAL "${CMAKE_PROJECT_NAME}")
    set(PYTHONPATH_WITH_SCENE_RDL2 "$<TARGET_FILE_DIR:__scene_rdl2__>:$ENV{PYTHONPATH}")
    set(SCENE_RDL2_PYTHON_MODULE_DEP "$<TARGET_FILE:__scene_rdl2__>")
else()
    set(PYTHONPATH_WITH_SCENE_RDL2 $ENV{PYTHONPATH})
    set(SCENE_RDL2_PYTHON_MODULE_DEP "")
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
            ${SCENE_RDL2_PYTHON_MODULE_DEP}
)

add_custom_target(
	shaders ALL
	DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/shaders.py
)

add_dependencies(shaders all_shader_dsos)

set(python_install_dir
		python/lib/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/${PACKAGE_NAME})

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/shaders.py DESTINATION ${python_install_dir})
