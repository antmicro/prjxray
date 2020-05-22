SYNTH ?= vivado
YOSYS ?= $(XRAY_DIR)/third_party/yosys/yosys

BIT2FASM_ARGS= --part "$(XRAY_DIR)/database/$(XRAY_DATABASE)/$(XRAY_PART)" --verbose

all: iddr_features.fasm

clean:
	rm -rf build-syn*
	rm -rf build-par*
	rm -rf *.log
	rm -rf *.edif
	rm -rf *.bit
	rm -rf *.bin
	rm -rf *.dcp
	rm -rf *.fasm

ifeq ($(SYNTH), yosys)
%.edif: %.v $(YOSYS)
	$(YOSYS) -p "read_verilog $< ; synth_xilinx -flatten -nosrl; write_edif -pvector bra -attrprop $@"  -l $@.log

else ifeq ($(SYNTH), vivado)
%.edif: %.v tcl/syn.tcl
	mkdir -p build-syn.$(basename $@)
	cd build-syn.$(basename $@) && env PROJECT_NAME=$(basename $@) $(XRAY_VIVADO) -mode batch -source ../tcl/syn.tcl -nojournal -log ../$@.log
	rm -rf *.backup.log
endif

%.bit: %.edif tcl/par.tcl
	mkdir -p build-par.$(basename $@)
	cd build-par.$(basename $@) && env PROJECT_NAME=$(basename $@) $(XRAY_VIVADO) -mode batch -source ../tcl/par.tcl -nojournal -log ../$@.log
	rm -rf *.backup.log

%.fasm: %.bit
	$(XRAY_BIT2FASM) $(BIT2FASM_ARGS) $< > $@ || (rm -rf $@ && false)
	@sort -u -o $@ $@

.PHONY: clean all
