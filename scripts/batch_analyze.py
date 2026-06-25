#!/usr/bin/env python
"""NPO Intel Scout - 批量分析入口"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
from ngo_intel.core.engine import BatchEngine
from ngo_intel.core.models import Organization
from ngo_intel.output.report_builder import ReportBuilder

def main():
    parser = argparse.ArgumentParser(description="批量分析多个NGO/基金会")
    parser.add_argument("csv_path", help="CSV文件路径（列: name,type,data_path,website）")
    parser.add_argument("--auto", "-a", help="自动采集", action="store_true")
    args = parser.parse_args()

    engine = BatchEngine()
    results = engine.run_from_csv(args.csv_path)
    print(f"\n批量处理完成: {len(results)} 个组织")
    for r in results:
        status = "!" if r["warnings"] else "OK"
        print(f"  [{status}] {r['org']}: {len(r['warnings'])} 条警告")

if __name__ == "__main__":
    main()