# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Moonray Project

add_pats_test(
    SCRIPT Test_ND_min.py
    OUTPUT Test_ND_min.exr
    CANONICALS Test_ND_min.exr
    RENDER_ARGS -size 600 800
)
