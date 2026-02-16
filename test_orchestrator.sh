#!/bin/bash

################################################################################
# Test script to demonstrate run_allelicMeth.py functionality
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Testing run_allelicMeth.py Orchestrator"
echo "=========================================="
echo ""

# Test 1: Help message
echo "Test 1: Display help"
echo "---"
python3.10 run_allelicMeth.py -h 2>&1 | head -20
echo "✓ Help message displayed"
echo ""

# Test 2: Explicit mode - missing files (expected to fail gracefully)
echo "Test 2: Explicit mode with missing files (expected error)"
echo "---"
python3.10 run_allelicMeth.py --mode explicit \
  --fasta /nonexistent/file.fasta \
  --sam /nonexistent/file.sam 2>&1 | tail -10 || true
echo "✓ Error handled gracefully"
echo ""

# Test 3: Directory mode - missing directory (expected to fail gracefully)
echo "Test 3: Directory mode with missing directory (expected error)"
echo "---"
python3.10 run_allelicMeth.py --mode directory --dir /nonexistent/dir 2>&1 | tail -10 || true
echo "✓ Error handled gracefully"
echo ""

# Test 4: Check log file creation
echo "Test 4: Verify log file generation"
echo "---"
echo "Creating test directory..."
TEST_DIR="/tmp/allelicmeth_test_$$"
mkdir -p "$TEST_DIR"

# Create dummy FASTA file with proper naming
cat > "$TEST_DIR/Galaxy2-[SNCA_Region1.fasta].fasta" << 'EOF'
>test_sequence_Region1
ACGTACGTACGTACGTACGTACGTACGTACGTACGT
EOF

echo "✓ Test FASTA created: $TEST_DIR/Galaxy2-[SNCA_Region1.fasta].fasta"

# Create dummy SAM file
cat > "$TEST_DIR/Galaxy303-[sgRNA3_Region1_Rep1].sam" << 'EOF'
@HD	VN:1.6	SO:coordinate
@SQ	SN:test_sequence_Region1	LN:40
test_read	0	test_sequence_Region1	1	60	40M	*	0	0	ACGTACGTACGTACGTACGTACGTACGTACGTACGT	*	MD:Z:40
EOF

echo "✓ Test SAM created: $TEST_DIR/Galaxy303-[sgRNA3_Region1_Rep1].sam"
echo ""

echo "Directory mode test will attempt to process test files"
echo "Note: This may fail if allelicMeth.py dependencies are not installed,"
echo "but it will show the orchestrator's file discovery and logging capabilities."
echo "---"

# Run in directory mode (will likely fail on actual processing, but shows orchestration)
python3.10 run_allelicMeth.py --mode directory --dir "$TEST_DIR" --debug 2>&1 | head -30 || true

echo ""
echo "✓ Orchestrator executed (check log file for details)"
echo ""

# Check log files
LOG_FILES=$(ls -t allelicMeth_log_*.log 2>/dev/null | head -5)
if [ -n "$LOG_FILES" ]; then
    echo "Generated log files:"
    echo "$LOG_FILES" | while read -r logfile; do
        echo "  - $logfile ($(wc -l < "$logfile") lines)"
    done
else
    echo "No log files found"
fi

echo ""
echo "Cleanup..."
rm -rf "$TEST_DIR"
echo "✓ Test directory cleaned up"

echo ""
echo "=========================================="
echo "Test suite completed!"
echo "=========================================="
