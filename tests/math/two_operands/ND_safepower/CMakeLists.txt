# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Moonray Project

add_pats_test(
    SCRIPT Test_ND_safepower.py
    OUTPUT Test_ND_safepower.exr
    CANONICALS Test_ND_safepower.exr
    RENDER_ARGS -size 600 800
)
