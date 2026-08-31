# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Moonray Project

function(${PROJECT_NAME}_link_options target)
    if(IsDarwinPlatform)
        target_link_options(${target} PRIVATE -Wl,-ld_classic)
    else()
        target_link_options(${target}
            PRIVATE
                -Wl,--enable-new-dtags              # Use RUNPATH instead of RPATH
        )
    endif()
endfunction()
