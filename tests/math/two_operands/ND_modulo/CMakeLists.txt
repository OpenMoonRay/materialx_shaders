# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Moonray Project

add_pats_test(
    SCRIPT Test_ND_modulo.py
    OUTPUT Test_ND_modulo.exr
    CANONICALS Test_ND_modulo.exr
    RENDER_ARGS -size 600 800
)
