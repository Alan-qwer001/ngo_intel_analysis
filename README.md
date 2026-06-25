# NPO Intel Scout

非营利组织情报侦察系统 — 对国际非政府组织（NGO）和基金会进行开源情报（OSINT）分析的 Python 工具包。

## 快速开始

```bash
pip install -r requirements.txt

# 方式一：提供手动整理的数据文件
python scripts/analyze.py "开放社会基金会" --data data/samples/osf_data.json

# 方式二：自动从官网采集（实验性）
python scripts/analyze.py "Open Society Foundations" --auto

# 批量分析
python scripts/batch_analyze.py data/inputs/组织列表.csv
```

## 项目结构

```
ngo_intel/
├── ngo_intel/          # 主包（core/collectors/analyzers/templates/output）
│   └── collectors/
│       ├── base.py             # 采集器基类
│       ├── collector_manual.py # 手动JSON输入
│       └── web_collector.py    # 自动网页采集（实验性）
├── scripts/            # 命令行入口
├── data/               # 输入、缓存、输出
├── requirements.txt
└── README.md
```

## 分析框架

| 框架 | 用途 |
|------|------|
| PESTLE | 政治/经济/社会/技术/法律/环境六维宏观分析 |
| McKinsey 7S | 战略/结构/系统/价值观/风格/人员/能力七维评估 |
| 风险矩阵 | 区域风险等级映射 + 趋势方向判断 |
| 同行业对标 | 与同类基金会的横向比较 |
| 财务趋势分析 | 年度支出变动率、区域结构变化 |

## 使用流程

1. 选择数据来源：手动 JSON 或自动采集
2. 运行 python scripts/analyze.py "组织名" --data data/数据.json
3. 在 data/outputs/ 查看生成的 .docx 报告

## 已知缺陷（v0.1）

### 1. 自动采集为实验性功能
WebCollector 已实现，能自动访问组织官网尝试提取以下数据：成立年份、总部地址、财务数据（表格）、资助记录（列表）、新闻事件、领导层信息。但由于不同 NGO 网站结构差异大，采集成功率不保证。

- 能稳定工作的场景：网站有标准表格结构（如 OSF 的 /who-we-are/financials）
- 可能失败的情况：纯图片展示、JavaScript 渲染、非标准页面布局
- 遇失败时建议回退到手动 JSON 输入方式

### 2. 无深度分析文字
报告基于规则算法和预设模板，不生成因果推理、战略解读、情景推演等自然语言分析。
规划 (v0.3)：可选 LLM 集成（仅用于撰写分析文字，约￥0.1/次），不用于数据提取。

### 3. 单个模板
仅实现了国际基金会模板。其他类型组织回退到同一模板。
规划 (v0.4)：增加国内NGO、协会、智库模板。

### 4. 数据质量依赖用户
无置信度评分或完整性校验。输入数据质量直接影响报告质量。
规划 (v0.3)：置信度评分 + 低置信度结论标注。

### 5. 无持久化存储
每次分析独立，无法跨组织对比。
规划 (v0.5)：SQLite 分析历史 + 跨组织对比。

### 6. 图表中文支持
图表标签目前英文，中文字体依赖系统安装。
规划 (v0.2)：可配图表语言 + 内置字体。

## 路线图

| 版本 | 重点 | 功能 |
|------|------|------|
| v0.1 | 基础框架 | 手动数据、自动采集（实验性）、规则分析器、Word报告、OSF示例 |
| v0.2 | 采集增强 | WebCollector 覆盖率提升、缓存、代理支持、URL模板注册表 |
| v0.3 | 质量与深度 | 置信度评分、LLM可选、数据校验 |
| v0.4 | 模板扩展 | 多类型组织模板 |
| v0.5 | 历史与规模 | SQLite、跨组织对比 |

## 依赖

python-docx、matplotlib、numpy、requests、beautifulsoup4、lxml

## License

MIT