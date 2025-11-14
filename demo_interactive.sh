#!/bin/bash
# Demo script untuk interactive mode
#
# Cara pakai:
# chmod +x demo_interactive.sh
# ./demo_interactive.sh

echo "======================================"
echo "Friday Screener - Interactive Demo"
echo "======================================"
echo ""
echo "Cara menggunakan Interactive Mode:"
echo ""
echo "1. Jalankan:"
echo "   make run"
echo "   ATAU"
echo "   python -m src.main"
echo ""
echo "2. Pilih mode:"
echo "   1 - Screen single stock"
echo "   2 - Compare multiple stocks"
echo "   q - Quit"
echo ""
echo "3. Ikuti prompt untuk input ticker"
echo ""
echo "======================================"
echo "Memulai Interactive Mode..."
echo "======================================"
echo ""

python -m src.main interactive
