# NPO Intel Scout --- 上下文记忆系统

## 项目身份

NPO Intel Scout（非营利组织情报侦察系统）是一个纯算法驱动的开源情报分析工具，专门针对国际 NGO 和基金会。输入组织名称和开源数据，输出一份带可视化图表的 Word 分析报告。

## 关键决策记录

### 决策1: 无 LLM 架构

- **做出时间**: 2026-06-25，项目初始化阶段
- **决策内容**: 所有分析模块使用纯算法（规则引擎、正则匹配、统计计算），不集成任何大语言模型
- **决策理由**:
  - 用户可用资源有限，无法承担 API 成本或部署模型
  - 分析质量和可复现性要求高于表达流畅性
  - 开源情报强调可验证性，LLM 的幻觉风险不可接受
  - 数据提取和分析环节必须 100% 可审计
- **后续影响**:
  - 报告的文字部分较为干瘪，缺乏因果推理和战略解读
  - 此缺陷被明确记录在 README.md 的已知缺陷中
  - v0.3 规划中保留"可选 LLM 集成"路径，但仅用于叙事生成，不用于数据提取

### 决策2: 国际基金会为首个实现模板

- **做出时间**: 2026-06-25
- **决策内容**: 第一期仅实现 InternationalFoundationTemplate，其他组织类型回退到同一模板
- **决策理由**:
  - 首个验证案例是开放社会基金会（OSF），属于国际基金会
  - 这类组织财务公开性最好，数据最容易获取
  - 模板系统已支持热扩展，后续加模板不需要改框架
- **后续影响**: v0.4 规划中增加国内 NGO、协会、智库模板

### 决策3: 批量模式为主交互方式

- **决策内容**: 设计为输入 CSV 组织列表，批量产出 .docx 报告
- **决策理由**: 用户明确偏好批量处理而非逐个交互
- **实现位置**: scripts/batch_analyze.py

### 决策4: ManualCollector 优先，WebCollector 为实验性

- **决策内容**: v0.1 同时提供手动 JSON 输入和自动网页采集两种数据来源，但自动采集标注为"实验性"
- **决策理由**: 不同 NGO 网站结构差异大，自动采集成功率不可保证
- **使用引导**: 对结构清晰的网站用 --auto，其他情况用 --data 提供手动整理的 JSON

## 项目架构速览

### 数据流

```
组织名称 → data_path → ManualCollector → 从 JSON 读
        → auto → WebCollector → 从官网爬
    ↓
结构化数据 (Dict) → Template.build(raw_data) →
    8个 Analyzer 链式执行：
    Overview → Financial → Activities → Legal
    → PESTLE → 7S → Risk → Synthesis → AnalysisReport
    → DocxGenerator → .docx 报告
```

### 分析器职责边界

| 分析器 | 输入依赖 | 输出 | 核心算法 |
|--------|---------|------|---------|
| OverviewAnalyzer | raw_data 基础字段 | governance + news | 字段映射 |
| FinancialAnalyzer | financial_records | financial + risk_matrix | YoY 计算 + 区域变动率 |
| ActivitiesAnalyzer | grant_records | grants | 排序 + 截断 |
| LegalRiskAnalyzer | legal_records | legal | 风险等级分类 |
| PESTLEAnalyzer | pestle_factors | pestle | 维度映射 |
| SevenSAnalyzer | seven_s_scores | seven_s + signals | 加权评分 + 阈值 |
| RiskAnalyzer | legal + seven_s + financial | critical_warnings | 风险聚合 |
| SynthesisAnalyzer | 所有分析结果 | conclusion_points | 文本拼接 |

### 数据模型核心类

```python
@dataclass class Organization: name, org_type, founder, headquarters, website
@dataclass class FinancialRecord: year, total_expenditure, regional_breakdown
@dataclass class LegalRecord: jurisdiction, risk_level, status, trend
@dataclass class AnalysisReport: organization, financial, governance, grants, legal, news, pestle, seven_s, strategic_signals, conclusion_points, critical_warnings
```

## OSF 调研上下文（首个验证案例）

OSF 2022-2024 三年支出: $1,318M -> $1,745M -> $1,190M

2024 区域特征: 美国最大($242M)，拉美唯一增长(+12.3%)，亚太最大跌幅(-67.9%)

法律环境: 俄罗斯(禁止)、匈牙利(重税)、中国(限制)、印度(监控)、美国(FARA上升)、肯尼亚(新风险)

7S 评分: 48/70，Staff 最弱(5/10)，Strategy 和 Values 最强(8/10)

最大资助: Access Now $6M(5年)，数字权利领域

## 代码约定

- 分析器类以 Analyzer 结尾，采集器以 Collector 结尾
- 分析器必须继承 BaseAnalyzer，实现 analyze() -> AnalysisReport
- 所有采集器输出统一 Dict[str, Any] 格式
- 所有数据模型使用 @dataclass
- 分析器之间不直接调用，所有数据通过 AnalysisReport 传递
- 分析器应尽量幂等

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1 | 2026-06-25 | 核心架构、8个分析器、手动采集器、Word报告、OSF示例 |
| v0.1.1 | 2026-06-25 | 添加 WebCollector（实验性自动采集） |

## 待解决问题

### 短期
- [x] WebCollector 基础实现
- [ ] JS 渲染页面采集能力不足
- [ ] 非标准表格的财务解析适应性弱

### 中期
- [ ] 置信度评分系统
- [ ] 数据完整性校验

### 长期
- [ ] LLM 可选集成（仅叙事）
- [ ] 多组织对比
- [ ] 时间序列追踪

## 对 AI Agent 的说明

1. **保持无 LLM 架构**：除非用户明确要求，不要引入 LLM 依赖。所有分析必须可复现、可审计。
2. **OSF 是验证基线**：任何改动应保证 python scripts/analyze.py "Open Society Foundations" --data data/samples/osf_data.json 能正常运行。
3. **扩展优先于重构**：优先通过新增分析器/采集器/模板来扩展，而不是修改现有核心模块。
4. 完整文档在 README.md，示例数据在 data/samples/osf_data.json。