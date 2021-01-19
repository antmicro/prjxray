#!/bin/bash
# Copyright (C) 2017-2020  The Project X-Ray Authors.
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC

if ! test $(find . -name "segdata_gtp_channel_[0123]_mid_left.txt" | wc -c) -eq 0
then
    ${XRAY_MERGEDB} gtp_channel_0_mid_left build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_1_mid_left build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_2_mid_left build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_3_mid_left build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_0_mid_left build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_1_mid_left build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_2_mid_left build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_3_mid_left build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_0_mid_right build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_1_mid_right build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_2_mid_right build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_3_mid_right build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_0_mid_right build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_1_mid_right build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_2_mid_right build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_3_mid_right build/mask_gtp_channelx.db
fi

if ! test $(find . -name "segdata_gtp_channel_[0123].txt" | wc -c) -eq 0
then
    ${XRAY_MERGEDB} gtp_channel_0 build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_1 build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_2 build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} gtp_channel_3 build/segbits_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_0 build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_1 build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_2 build/mask_gtp_channelx.db
    ${XRAY_MERGEDB} mask_gtp_channel_3 build/mask_gtp_channelx.db
fi
