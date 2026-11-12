# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Moonray Project

add_pats_test(
    SCRIPT Test_ND_divide.py
    OUTPUT Test_ND_divide.exr
    CANONICALS Test_ND_divide.exr
    RENDER_ARGS -size 600 800
)
