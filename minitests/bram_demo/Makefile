bitread_dump = ${XRAY_BITREAD} specimen_00$(1)/design.bit -o design_$(1).bits -z -y > bitread_dump_$(1)

bittool_dump_1:
	${XRAY_BITTOOL} list_config_packets specimen_001/design.bit > $@

bittool_dump_2:
	${XRAY_BITTOOL} list_config_packets specimen_002/design.bit > $@

bitread_dump_1:
	$(call bitread_dump,1)

bitread_dump_2:
	$(call bitread_dump,2)

.PHONY: bitread_dump_1 bitread_dump_2

bitread_test: bitread_dump_1 bitread_dump_2
	@echo "Bitread dump diff"
	diff bitread_dump_1 bitread_dump_2
	#@echo "Bits diff"
	#diff design_1.bits design_2.bits

