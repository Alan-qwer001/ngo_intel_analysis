#!/usr/bin/env python
"""NPO Intel Scout - 单组织分析入口"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
from ngo_intel.core.models import Organization
from ngo_intel.core.pipeline import AnalysisPipeline
from ngo_intel.output.report_builder import ReportBuilder

def main():
    parser = argparse.ArgumentParser(description="对单个NGO/基金会进行开源情报分析")
    parser.add_argument("name", help="组织名称")
    parser.add_argument("--data", "-d", help="手动整理的数据JSON文件路径（可选）", default="")
    parser.add_argument("--auto", "-a", help="自动从官网采集数据（实验性）", action="store_true")
    parser.add_argument("--website", "-w", help="指定官网URL（配合--auto使用）", default="")
    parser.add_argument("--type", "-t", help="组织类型", default="foundation")
    args = parser.parse_args()

    org = Organization(name=args.name, org_type=args.type, website=args.website)
    pipeline = AnalysisPipeline(org, data_path=args.data, auto_collect=args.auto)
    report = pipeline.run()

    print(f"\n分析完成: {org.name}")
    print(f"关键结论:")
    for pt in report.conclusion_points:
        print(f"  - {pt}")
    if report.critical_warnings:
        print(f"\n警告:")
        for w in report.critical_warnings:
            print(f"  ! {w}")
    docx_path = ReportBuilder(report).save()
    print(f"\n报告输出: {docx_path}")

if __name__ == "__main__":
    main()