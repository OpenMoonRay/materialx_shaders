# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Moonray Project

add_pats_test(
    SCRIPT Test_one_operand.py
    OUTPUT Test_one_operand.exr
    CANONICALS Test_one_operand.exr
    RENDER_ARGS -size 600 800
)
