# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Moonray Project

# Tests camera stereo left view with dof.

add_pats_test(
    SCRIPT Test_ND_subtract.py
    OUTPUT Test_ND_subtract.exr
    CANONICALS Test_ND_subtract.exr
    RENDER_ARGS -size 600 800
)
