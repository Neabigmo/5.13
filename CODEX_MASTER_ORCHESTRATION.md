# CODEX_MASTER_ORCHESTRATION.md

> 项目：k-NN / local learning rules 的稳定性微积分  
> 目标：让 Codex 阅读本文件后，自动拆分项目文档、建立任务系统，并以“总设计师 + 审查专员”的身份调度本地 Claude Code 完成低级实现、枚举、绘图、LaTeX 维护等工作。  
> 核心原则：Codex 负责方向、定义、证明审查、文献判断、最终整合；Claude Code 负责高 token、低层级、可验证的工程任务。  
> 语言：中文为主，数学论文正文可用英文。  
> 质量要求：默认最高质量；未经用户明确同意，不允许为了省事简化任务、弱化证明、跳过测试、跳过引用核验或降低可复现性。

---

## 0. Codex 启动后的第一动作

Codex 读完本文件后，不要立刻写论文，不要直接开始证明，不要把全文塞给 Claude Code。请按以下顺序执行：

1. 在仓库根目录创建清晰的 Git 项目结构。
2. 将本文件拆分为若干小文档，放入 `docs/project-control/`。
3. 生成仓库级 `AGENTS.md`，只放长期稳定的工作规范，不要放过长研究细节。
4. 建立 `tasks/` 任务系统，并生成首批任务卡。
5. 建立 Claude Code 调度脚本和任务报告格式。
6. 初始化 git，做第一次 commit。
7. 从 `tasks/TASK_INDEX.md` 中选择第一批低级任务，委派给 Claude Code。
8. Claude Code 返回报告后，Codex 必须审查 diff、测试结果、数学定义一致性，再决定是否合并。

Codex 必须避免一次性吸收和反复复述全部研究内容。Codex 只保留项目蓝图、定义规范、审查标准和关键数学主张。低级实现、穷举、图表、LaTeX 机械整理等任务都应通过最小任务卡委派给 Claude Code。

---

## 1. 用户本地环境与固定偏好

这些是项目的长期本地约定。Codex 必须写入 `AGENTS.md` 和必要的脚本中。

### 1.1 代理设置

用户默认代理端口为 `7897`。系统代理有时混乱，联网命令需要显式设置代理变量。

推荐命令模板：

```bash
export HTTP_PROXY=http://127.0.0.1:7897
export HTTPS_PROXY=http://127.0.0.1:7897
export ALL_PROXY=socks5://127.0.0.1:7897
export http_proxy=http://127.0.0.1:7897
export https_proxy=http://127.0.0.1:7897
export all_proxy=socks5://127.0.0.1:7897
```

Codex 和 Claude Code 在执行任何需要联网的命令前，都应显式设置这些变量，除非用户另有说明。

### 1.2 Conda 环境

优先使用用户已有 conda 环境：

```bash
conda activate pytorch-clean
```

在非交互脚本中优先使用：

```bash
conda run -n pytorch-clean python -V
conda run -n pytorch-clean pytest
```

如需安装依赖，先检查环境，再以最小必要方式安装。不要破坏用户环境。需要新增依赖时，记录在 `environment.yml` 或 `pyproject.toml`。

### 1.3 Git 管理

必须使用 git 进行版本管理。

基本规则：

- 每个任务使用独立分支或 worktree。
- 每次 Claude Code 完成任务后，Codex 审查后再 commit。
- commit message 必须说明任务编号。
- 不允许大而混乱的 commit。
- 生成文件、结果文件、图表、脚本都要有清晰目录。
- API key、`.env`、临时缓存、日志中的 secret 不得提交。

### 1.4 质量标准

默认要求最高质量：

- 不允许“先写个简化版以后再说”，除非用户明确同意。
- 不允许跳过测试。
- 不允许把未证明的猜想写成定理。
- 不允许把计算枚举结果写成数学证明，除非另有形式化证明。
- 不允许降低论文目标来适配容易完成的代码。
- 不允许 Claude Code 擅自改数学定义。
- 不允许 Codex 未审查就接受 Claude Code 结果。

---

## 2. 项目研究目标

最终论文目标：

**A Stability Calculus for Local Learning Rules: Exact Delete-One, Replace-One, and Leave-One-Out Characterizations for k-Nearest Neighbors**

中文定位：

**局部学习规则的稳定性微积分：k-NN 的删一点、换一点与留一稳定性的精确刻画**

核心研究问题：

1. delete-one、add-one、replace-one、leave-one-out、uniform stability 之间有哪些一般关系？
2. 在 uniform stability 层面，delete-one 与 replace-one 是否本质等价到常数？
3. 对固定 tie-breaking 的 deterministic k-NN，样本删除或替换何时改变预测？
4. 在有限无权图最短路度量上，1-NN 的 LOO stability 与 replace-one stability 是否可精确分离？
5. 最小反例的顶点数、标签结构、tie-breaking 依赖是什么？
6. 这些分离如何推广到任意 k？
7. 这些 worst-case 分离如何与经典 k-NN consistency、hypothesis stability、LOO-CV、conformal prediction 的稳定性证书共存？

---

## 3. Codex 与 Claude Code 的分工

### 3.1 Codex 拥有的任务

Codex 是总设计师、审查专员和数学质量负责人。以下任务不得完全交给 Claude Code：

1. 最终定义体系设计。
2. 关键数学定理的真实性判断。
3. 证明草稿的审查与修正。
4. 文献检索、文献筛选、新颖性判断。
5. 最终论文叙事、摘要、引言、贡献表述。
6. 投稿策略、期刊定位、审稿风险判断。
7. 对 Claude Code 输出进行 diff 审查、测试复现、数学一致性检查。
8. 决定一个任务是否完成。

Codex 可以让 Claude Code 起草、枚举、生成候选，但必须亲自审查。

### 3.2 Claude Code 拥有的任务

Claude Code 是执行代理。适合交给它的任务：

1. 搭建代码仓库结构。
2. 实现 finite metric space、graph metric、deterministic k-NN。
3. 实现 stability definitions 的可计算版本。
4. 写 pytest。
5. 穷举小图、标签、tie-breaking、训练样本。
6. 搜索最小反例。
7. 生成 JSON witness。
8. 生成图表、LaTeX 表格。
9. 写脚本、README、环境文件。
10. 对已给定文献条目做 BibTeX 格式整理。
11. 检查 LaTeX 编译错误。
12. 生成附录中的算法伪代码初稿。

Claude Code 不应独立决定论文贡献是否足够，也不应独立给出最终数学结论。

---

## 4. Context Firewall：上下文节省与信息隔离

用户希望节省 Codex token，因此 Codex 不应把完整论文蓝图、完整文献综述、全部证明草稿都发给 Claude Code。

Codex 委派任务时必须遵守：

1. 每次只给 Claude Code 一个任务卡。
2. 任务卡只包含该任务必需的上下文。
3. 不把完整论文草稿发给 Claude Code。
4. 不把未冻结的数学定义混入任务卡。
5. Claude Code 只需返回结构化报告，不需要长篇解释。
6. 对于代码任务，Claude Code 应返回：
   - 修改文件列表；
   - 新增函数/类；
   - 运行命令；
   - 测试结果；
   - 发现的不确定性；
   - 后续建议。
7. 对于枚举任务，Claude Code 应返回：
   - 搜索空间；
   - 约束；
   - witness；
   - 无解范围；
   - 输出文件路径；
   - reproducibility command。
8. 对于 LaTeX 任务，Claude Code 应返回：
   - 修改章节；
   - 新增定理/引理编号；
   - 未证明 claim；
   - 编译结果。

---

## 5. Codex 首次拆分文档

Codex 读完本文件后，应创建以下文档。

```text
docs/project-control/
├── 00_PROJECT_CHARTER.md
├── 01_RESEARCH_BLUEPRINT.md
├── 02_DEFINITIONS_SPEC.md
├── 03_CODE_ARCHITECTURE.md
├── 04_CLAUDE_DELEGATION_PROTOCOL.md
├── 05_LITERATURE_REVIEW_PROTOCOL.md
├── 06_PROOF_AUDIT_PROTOCOL.md
├── 07_GIT_AND_ENVIRONMENT.md
└── 08_PUBLICATION_STRATEGY.md
```

每个文档用途：

### `00_PROJECT_CHARTER.md`

写项目目标、最终论文定位、角色分工、质量标准、禁止事项。

### `01_RESEARCH_BLUEPRINT.md`

写研究问题、目标定理、预期章节、milestones。

### `02_DEFINITIONS_SPEC.md`

写所有稳定性定义。这个文档是代码实现和论文写作的唯一权威来源。

必须包括：

- sample;
- finite metric space;
- graph shortest-path metric;
- deterministic tie-breaking;
- k-NN prediction;
- 0-1 loss;
- delete-one stability;
- add-one stability;
- replace-one stability;
- CVloo / LOO stability;
- pointwise stability;
- expected stability;
- uniform stability;
- consistency;
- allowed/disallowed duplicate points;
- allowed/disallowed conflicting labels.

### `03_CODE_ARCHITECTURE.md`

写 `src/` 模块设计、测试设计、输出文件规范、实验脚本规范。

### `04_CLAUDE_DELEGATION_PROTOCOL.md`

写 Claude Code 调度方式、任务卡模板、报告模板、命令模板、allowed tools、上下文隔离。

### `05_LITERATURE_REVIEW_PROTOCOL.md`

写文献检索策略。Codex 负责查找与筛选，Claude Code 仅做格式化和整理。

### `06_PROOF_AUDIT_PROTOCOL.md`

写证明审查流程。包括如何区分 theorem、lemma、conjecture、computational evidence。

### `07_GIT_AND_ENVIRONMENT.md`

写 conda、proxy、git、分支、worktree、依赖、测试命令。

### `08_PUBLICATION_STRATEGY.md`

写 Machine Learning / TMLR / JMLR / COLT 等目标的贡献强度要求、风险和应对。

---

## 6. 仓库结构

Codex 应创建如下结构：

```text
knn-stability-calculus/
├── AGENTS.md
├── CODEX_MASTER_ORCHESTRATION.md
├── README.md
├── pyproject.toml
├── environment.yml
├── .gitignore
├── .env.template
├── docs/
│   ├── project-control/
│   ├── literature/
│   ├── proof-notes/
│   └── decisions/
├── tasks/
│   ├── TASK_INDEX.md
│   ├── backlog/
│   ├── active/
│   ├── done/
│   └── reports/
├── tools/
│   ├── run_claude_task.py
│   ├── make_task.py
│   ├── collect_report.py
│   └── validate_repo.py
├── src/
│   └── knn_stability/
│       ├── __init__.py
│       ├── metrics.py
│       ├── graph_metrics.py
│       ├── tie_breaking.py
│       ├── knn.py
│       ├── stability.py
│       ├── enumeration.py
│       └── witnesses.py
├── tests/
│   ├── test_metrics.py
│   ├── test_graph_metrics.py
│   ├── test_tie_breaking.py
│   ├── test_knn.py
│   ├── test_stability.py
│   └── test_witnesses.py
├── experiments/
│   ├── search_minimal_1nn.py
│   ├── search_tie_free.py
│   ├── search_k_gadgets.py
│   ├── certify_minimality.py
│   └── make_tables_and_figures.py
├── outputs/
│   ├── witnesses/
│   ├── tables/
│   ├── figures/
│   └── logs/
└── paper/
    ├── main.tex
    ├── refs.bib
    ├── sections/
    │   ├── 01_intro.tex
    │   ├── 02_related_work.tex
    │   ├── 03_definitions.tex
    │   ├── 04_general_calculus.tex
    │   ├── 05_knn_characterization.tex
    │   ├── 06_finite_metric_separations.tex
    │   ├── 07_k_extension.tex
    │   ├── 08_consistency_and_prediction.tex
    │   └── 09_discussion.tex
    └── figures/
```

---

## 7. Claude Code 调度方式

### 7.1 基本原则

优先使用 Claude Code 的非交互模式，避免它加载不必要上下文。使用 `--bare` 和 `-p`。

基本命令模板：

```bash
export HTTP_PROXY=http://127.0.0.1:7897
export HTTPS_PROXY=http://127.0.0.1:7897
export ALL_PROXY=socks5://127.0.0.1:7897
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}"

claude --bare -p "$(cat tasks/active/TASK-001.md)" \
  --allowedTools "Read,Edit,Bash" \
  --output-format json \
  > tasks/reports/TASK-001.report.json
```

如果需要 Claude Code 创建新文件，而 `Write` 工具可用，可改为：

```bash
--allowedTools "Read,Edit,Write,Bash"
```

如果 `Write` 不可用，则让 Claude 用 `Bash` 通过 heredoc 创建文件。

### 7.2 不要暴露 API key

Codex 不得把 API key 写入任务卡、commit、日志或报告。只允许通过环境变量读取：

```bash
export ANTHROPIC_API_KEY=...
```

创建 `.env.template`，但不创建真实 `.env`：

```bash
ANTHROPIC_API_KEY=
HTTP_PROXY=http://127.0.0.1:7897
HTTPS_PROXY=http://127.0.0.1:7897
ALL_PROXY=socks5://127.0.0.1:7897
```

`.gitignore` 必须包含：

```gitignore
.env
*.key
*.pem
tasks/reports/*.raw.json
outputs/logs/
__pycache__/
.pytest_cache/
```

### 7.3 Claude Code 报告格式

每个 Claude Code 任务必须以 JSON 或 Markdown 报告形式返回。

推荐 JSON schema：

```json
{
  "task_id": "TASK-001",
  "status": "completed | blocked | failed",
  "summary": "one-paragraph summary",
  "files_changed": [
    {"path": "src/knn_stability/metrics.py", "change": "created"}
  ],
  "commands_run": [
    {"cmd": "conda run -n pytorch-clean pytest", "exit_code": 0}
  ],
  "tests": {
    "passed": true,
    "details": "12 passed"
  },
  "mathematical_assumptions": [
    "finite metric distance matrix is symmetric and satisfies triangle inequality"
  ],
  "ambiguities": [
    "label tie-breaking for even k needs confirmation"
  ],
  "next_steps": [
    "implement graph shortest-path metric"
  ]
}
```

Codex 必须读取报告，并执行：

```bash
git diff --stat
git diff
conda run -n pytorch-clean pytest
```

必要时还要运行具体实验脚本。

---

## 8. 任务卡模板

每个任务卡必须短、清晰、可验收。模板如下：

```markdown
# TASK-XXX: short title

## Owner

Claude Code

## Role

You are an execution agent. Do not redefine mathematical concepts. Implement exactly what is specified here.

## Goal

One clear goal.

## Context

Only the minimal context needed for this task.

## Inputs

- relevant files
- relevant definitions
- constraints

## Required work

1. Step one.
2. Step two.
3. Step three.

## Do not do

- Do not change definitions.
- Do not edit unrelated files.
- Do not simplify assumptions.
- Do not claim a theorem is proved.
- Do not touch API keys.

## Validation

Run:

```bash
conda run -n pytorch-clean pytest
```

Additional commands if needed.

## Report

Return a structured report with:
- status;
- files changed;
- commands run;
- tests;
- ambiguities;
- next steps.
```

---

## 9. 初始任务队列

Codex 首次拆分后，应创建以下任务。

### TASK-001: Initialize repository skeleton

Owner: Claude Code  
Goal: 创建目录、pyproject、environment、README、paper skeleton、tests skeleton。  
Codex review: 检查结构与 AGENTS.md 是否正确。

### TASK-002: Implement finite metric spaces

Owner: Claude Code  
Goal: 实现 `FiniteMetricSpace`，验证距离矩阵。  
Codex review: 检查 triangle inequality、错误处理、测试。

### TASK-003: Implement graph shortest-path metrics

Owner: Claude Code  
Goal: 用 unweighted connected graph 构造 shortest-path metric。  
Codex review: 检查 disconnected graph rejection。

### TASK-004: Implement deterministic tie-breaking

Owner: Claude Code  
Goal: 固定点序 tie-breaking、标签 tie-breaking。  
Codex review: 检查是否与定义文档一致。

### TASK-005: Implement deterministic k-NN classifier

Owner: Claude Code  
Goal: 支持 ordered neighbors、binary labels、odd/even k。  
Codex review: 手工测试 tie case。

### TASK-006: Implement stability indicators

Owner: Claude Code  
Goal: delete-one、replace-one、LOO、uniform brute-force helper。  
Codex review: 重点检查定义一致性。

### TASK-007: Search minimal 1-NN witnesses

Owner: Claude Code  
Goal: 穷举小图，生成 witness JSON。  
Codex review: 检查搜索空间和约束。

### TASK-008: Search tie-free witnesses

Owner: Claude Code  
Goal: 排除距离 tie 的分离反例。  
Codex review: 检查 tie-free 条件是否真正实现。

### TASK-009: Generate minimality certificate

Owner: Claude Code  
Goal: 生成无解范围表、可复现命令、输出 hash。  
Codex review: 将其标为 computational evidence，不得误称 proof。

### TASK-010: Draft LaTeX definitions section

Owner: Claude Code  
Goal: 按 `02_DEFINITIONS_SPEC.md` 起草 definitions.tex。  
Codex review: 数学符号逐行检查。

### TASK-011: Generate figures for witnesses

Owner: Claude Code  
Goal: networkx + matplotlib 生成 PDF/SVG。  
Codex review: 检查图是否清晰、标签是否正确。

### TASK-012: Implement k-gadget search

Owner: Claude Code  
Goal: 为 k=3,5,7 搜索/验证 gadget。  
Codex review: 提炼成 theorem 候选。

### TASK-013: Prepare related-work table skeleton

Owner: Claude Code  
Goal: 根据 Codex 给出的文献列表整理表格，不进行独立文献判断。  
Codex review: 文献准确性由 Codex 负责。

---

## 10. Codex 专属任务队列

以下任务 Codex 不应交给 Claude Code 完成最终判断。

### C-TASK-001: Freeze definitions

产出：`docs/project-control/02_DEFINITIONS_SPEC.md` 的冻结版本。  
要求：每个稳定性定义都有符号、量词、评价点、样本扰动方式、loss 类型。

### C-TASK-002: Literature review

Codex 查找、阅读、筛选文献。重点：

- Bousquet–Elisseeff stability；
- Rogers–Wagner / Devroye–Wagner k-local / deleted estimate；
- Kearns–Ron algorithmic stability and LOO；
- Cover–Hart / Stone k-NN consistency；
- Mukherjee–Niyogi–Poggio–Rifkin LOO stability and consistency；
- k-NN LOOCV recent work；
- conformal prediction 中 LOO stability / replace-one stability。

产出：

```text
docs/literature/
├── LIT_TABLE.md
├── novelty_assessment.md
└── refs_to_add.bib
```

### C-TASK-003: Prove uniform no-separation theorem

Codex 负责证明。Claude Code 只可检查 LaTeX 编译或画 implication diagram。

### C-TASK-004: Derive exact k-NN perturbation criterion

Codex 负责推导定理陈述和证明。Claude Code 只可验证例子或生成辅助图。

### C-TASK-005: Convert computational witnesses into mathematical lemmas

Codex 审查 witness，并将其转为 lemma/theorem。Claude Code 不能把 witness 直接写成最终 theorem。

### C-TASK-006: Publication strategy and contribution sheet

Codex 负责 Machine Learning / TMLR / JMLR 的投稿论证。

---

## 11. 推荐脚本：`tools/run_claude_task.py`

Codex 应让 Claude Code 或自己创建该脚本。目标：统一调度 Claude Code。

功能需求：

1. 读取 `tasks/active/TASK-XXX.md`。
2. 设置代理环境变量。
3. 使用 `claude --bare -p` 调用 Claude Code。
4. 输出 JSON 报告到 `tasks/reports/`。
5. 记录命令、时间、退出码。
6. 不打印 API key。
7. 失败时写入 `.failed.json`。

伪代码：

```python
import os
import subprocess
from pathlib import Path

def run_task(task_path: Path):
    task_id = task_path.stem
    env = os.environ.copy()
    env["HTTP_PROXY"] = env.get("HTTP_PROXY", "http://127.0.0.1:7897")
    env["HTTPS_PROXY"] = env.get("HTTPS_PROXY", "http://127.0.0.1:7897")
    env["ALL_PROXY"] = env.get("ALL_PROXY", "socks5://127.0.0.1:7897")

    prompt = task_path.read_text(encoding="utf-8")
    out_path = Path("tasks/reports") / f"{task_id}.report.json"

    cmd = [
        "claude",
        "--bare",
        "-p",
        prompt,
        "--allowedTools",
        "Read,Edit,Bash",
        "--output-format",
        "json",
    ]

    result = subprocess.run(cmd, env=env, text=True, capture_output=True)
    out_path.write_text(result.stdout, encoding="utf-8")

    if result.returncode != 0:
        fail_path = Path("tasks/reports") / f"{task_id}.failed.stderr.txt"
        fail_path.write_text(result.stderr, encoding="utf-8")
        raise SystemExit(result.returncode)
```

---

## 12. 数学定义冻结规则

在代码完成前，Codex 必须冻结 v0.1 定义。

需要明确：

1. 训练样本是 set、multiset 还是 ordered tuple？
2. 是否允许重复点？
3. 是否允许同一点不同标签？
4. k-NN 查询点是否可以是训练点？
5. LOO 中被删点是否作为评价点？
6. replace-one 的 replacement 是否来自任意 labeled point，还是来自分布？
7. tie-breaking 是顶点全序、样本索引顺序，还是标签顺序？
8. 0-1 loss 的标签空间是什么？
9. consistency 是 classical distributional consistency，还是 finite-sequence notion？
10. uniform stability 的 supremum 范围是什么？

没有冻结定义前，Claude Code 不得实现 stability 模块。

---

## 13. 证明审查规则

Codex 审查任何证明草稿时必须检查：

1. 量词是否正确；
2. 定义是否一致；
3. 是否把 pointwise 结论误写成 uniform 结论；
4. 是否把 expected 结论误写成 worst-case 结论；
5. 是否把 computational evidence 写成 proof；
6. 是否隐藏了 tie-breaking 假设；
7. 是否默认了无重复点或无 label conflict；
8. 是否把 fixed k 与 k_n 混淆；
9. 是否把 classification 与 regression 混淆；
10. 是否与已有经典结果冲突。

如果有任何不确定，标记为 `Conjecture` 或 `Claim under review`，不得写成 theorem。

---

## 14. 文献检索规则

Codex 负责文献检索，不把这个任务完全交给 Claude Code。Claude Code 可以整理 `refs.bib`，但不能决定新颖性。

文献记录模板：

```markdown
# Paper note: Author Year

## Citation

BibTeX key:

## What it proves

## Stability notions used

## Algorithm class

## Relation to k-NN

## Relation to delete-one / replace-one / LOO

## Does it already solve our problem?

Yes / No / Partial

## How our work differs

## Must cite in paper?

Yes / No
```

Codex 应优先使用原始论文、期刊页面、作者 PDF、官方 proceedings 页面。不要依赖二手博客做最终引用判断。

---

## 15. 论文主线与目标定理

### Theorem 1: Uniform no-separation theorem

大意：

在 bounded loss 下，uniform delete-one/add-one stability 与 replace-one stability 之间存在常数因子控制。真正的强分离只能发生在较弱定义中。

### Theorem 2: Exact k-NN perturbation criterion

大意：

对 deterministic k-NN，删除或替换样本改变查询点预测，当且仅当扰动改变前 k 邻域并使 vote margin 或 tie-breaking 决策跨越阈值。

### Theorem 3: Minimal finite graph separation for 1-NN

大意：

在有限无权图最短路度量上，pointwise LOO stability 与 pointwise replace-one stability 可严格分离；给出最小反例并证明最小性。

### Theorem 4: k-NN gadget lifting

大意：

把 1-NN 分离构造推广到任意 k。奇数 k 和偶数 k 分别处理。

### Theorem 5: Consistency compatibility

大意：

worst-case finite-metric 分离不否定 classical k-NN consistency；在连续分布/无 tie/margin 条件下某些 expected stability 可恢复，在离散原子分布中可失败。

### Optional Theorem 6: Consequence for conformal prediction

大意：

LOO-based stability certificate 与 replace-one-based certificate 在 local learners 上可以有常数级分离，因此二者在 distribution-free prediction 中不应被无条件互换。

---

## 16. 代码验收标准

每个代码任务必须满足：

```bash
conda run -n pytorch-clean python -m pytest
conda run -n pytorch-clean python experiments/search_minimal_1nn.py --max_vertices 4
```

若 LaTeX 已建立：

```bash
latexmk -pdf paper/main.tex
```

如果没有 `latexmk`，则记录缺失，不要伪造编译成功。

代码风格：

- Python 3.11+；
- type hints；
- dataclasses where helpful；
- simple and auditable over clever；
- deterministic outputs；
- no random search unless seed is fixed；
- all experiment parameters saved to JSON；
- graph enumeration must record assumptions。

---

## 17. Claude Code agent 分工建议

如果要用多个 Claude Code agent，可使用任务卡模拟角色，不必让每个 agent 读完整项目。

### Agent A: Infrastructure Builder

任务：目录、pyproject、环境、测试骨架。

### Agent B: Definition Implementer

任务：根据冻结定义实现 metrics / kNN / stability。

### Agent C: Enumerator

任务：穷举图、标签、tie-breaking、samples。

### Agent D: Witness Analyst

任务：整理 witness JSON，生成表格，不做最终数学判断。

### Agent E: Figure Maker

任务：根据 witness 生成图。

### Agent F: LaTeX Mechanic

任务：维护 LaTeX 编译、交叉引用、图表插入。

### Agent G: Test Auditor

任务：写 pytest、mutation-like edge cases。

Codex 应作为总审查者检查所有 agent 的输出。

---

## 18. Git 工作流

推荐：

```bash
git init
git checkout -b main
git add .
git commit -m "INIT: project orchestration document"

git checkout -b task/TASK-001-init
# run Claude Code task
git diff
conda run -n pytorch-clean pytest
git add .
git commit -m "TASK-001: initialize repository skeleton"
git checkout main
git merge --no-ff task/TASK-001-init
```

并行任务可用 worktree：

```bash
git worktree add ../knn-stability-TASK-002 -b task/TASK-002-metrics
git worktree add ../knn-stability-TASK-003 -b task/TASK-003-graph-metrics
```

每个 worktree 独立运行 Claude Code，Codex 汇总审查。

---

## 19. 立即执行的 Codex 启动提示

当用户在 Codex 中打开本仓库时，可以直接给 Codex 这段话：

```text
Read CODEX_MASTER_ORCHESTRATION.md. 
Act as principal architect and reviewer, not as the low-level implementer.
First split the master document into the requested project-control documents.
Create AGENTS.md, tasks/TASK_INDEX.md, the initial task cards, and a Claude Code delegation script.
Use git from the beginning.
Use the conda environment pytorch-clean.
For network commands, explicitly set proxy variables to 127.0.0.1:7897.
Do not simplify the plan without my explicit approval.
After setup, delegate TASK-001 to local Claude Code using claude --bare -p and review its report before committing.
```

---

## 20. 失败与阻塞处理

如果 Codex 发现 Claude Code 不可用：

1. 运行：

```bash
which claude
claude --version
```

2. 若不可用，创建 `docs/decisions/BLOCKED_CLAUDE_CODE_SETUP.md`，说明缺失。
3. 不要伪造 Claude Code 报告。
4. 不要擅自改为 Codex 全部亲自执行，除非用户同意。
5. 可以先创建任务卡和仓库结构，等待用户配置 Claude Code。

如果 API key 缺失：

1. 检查 `ANTHROPIC_API_KEY` 是否存在。
2. 若不存在，写入阻塞报告。
3. 不要要求用户把 key 写入仓库。
4. 不要打印 key。

如果代理失败：

1. 显式设置 7897 代理。
2. 记录失败命令和 stderr。
3. 尝试无代理一次，但必须记录。
4. 不要无限重试。

---

## 21. 完成标准

本项目阶段性完成的标准不是“有代码”，而是：

1. 定义冻结；
2. 代码实现与定义一致；
3. 小图枚举可复现；
4. 最小 witness 有 JSON、图、表；
5. 无解范围有 computational certificate；
6. 关键定理有证明草稿；
7. 文献表说明新颖性；
8. LaTeX 初稿可编译；
9. Codex 审查报告标记所有未解决风险；
10. 所有任务都有 git 记录。

最终论文投稿前，必须有：

- `paper/main.pdf`;
- `paper/refs.bib`;
- `outputs/witnesses/*.json`;
- `outputs/tables/*.tex`;
- `outputs/figures/*.pdf`;
- `docs/literature/LIT_TABLE.md`;
- `docs/proof-notes/`;
- `tasks/reports/`;
- `README.md` reproduction instructions;
- Machine Learning contribution sheet draft.

---

## 22. 禁止事项清单

Codex 和 Claude Code 都必须遵守：

- 不要把 API key 写入任何文件。
- 不要把 `.env` commit。
- 不要让 Claude Code 读取完整研究蓝图，除非任务确实需要。
- 不要把 Claude Code 的数学判断当成最终结论。
- 不要把枚举证据写成形式证明。
- 不要修改冻结定义，除非创建 decision record 并经 Codex 审查。
- 不要为了尽快完成而减少测试或缩小搜索空间。
- 不要省略代理设置。
- 不要破坏 `pytorch-clean` 环境。
- 不要混淆 LOO、delete-one、replace-one。
- 不要忽视 tie-breaking。
- 不要忽视 duplicate samples 和 conflicting labels。
- 不要写“显然”而不给证明。
- 不要写“已有文献未研究”而不做文献核验。

---

## 23. Decision record 模板

当定义、范围、投稿策略发生变化时，Codex 必须创建：

```text
docs/decisions/DR-YYYYMMDD-short-title.md
```

模板：

```markdown
# Decision Record: title

## Date

YYYY-MM-DD

## Status

Proposed / Accepted / Rejected / Superseded

## Context

Why this decision is needed.

## Decision

What we decide.

## Alternatives considered

1. ...
2. ...

## Consequences

Positive:
- ...

Negative / risks:
- ...

## Required follow-up

- ...
```

---

## 24. 第一批可执行命令

Codex 可以按以下命令开始：

```bash
export HTTP_PROXY=http://127.0.0.1:7897
export HTTPS_PROXY=http://127.0.0.1:7897
export ALL_PROXY=socks5://127.0.0.1:7897

conda run -n pytorch-clean python -V

mkdir -p docs/project-control docs/literature docs/proof-notes docs/decisions
mkdir -p tasks/backlog tasks/active tasks/done tasks/reports
mkdir -p tools src/knn_stability tests experiments outputs/witnesses outputs/tables outputs/figures outputs/logs
mkdir -p paper/sections paper/figures

git init
```

然后创建拆分文档、`AGENTS.md`、任务卡、调度脚本。

---

## 25. 给 Codex 的最终提醒

你是总设计师和审查专员。  
你不是低级实现工人。  
你可以调用 Claude Code 完成大量低级工作，但你必须：

1. 定义任务；
2. 限制上下文；
3. 要求报告；
4. 审查 diff；
5. 运行测试；
6. 检查数学一致性；
7. 决定是否接受；
8. 记录到 git；
9. 维护最高质量标准。

如果某一步不确定，创建 decision record，而不是偷懒简化。
