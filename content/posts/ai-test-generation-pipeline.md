---
title: "AI 帮你写测试到底靠不靠谱？我搭了一套自动化测试生成流水线"
date: 2026-06-26
draft: false
tags: ["AI", "测试", "自动化", "项目实战", "开发工具"]
---

上周刷到一个帖子，有人让 Claude 给他的 Python 项目写 100 个单元测试。结果跑下来一半是 `assert True`，四分之一测的是不存在的方法，剩下四分之一里还有几个压根不会跑通（因为 mock 对象传错了类型）。

评论区炸了："AI 写测试就是垃圾"、"还不如不写，给你虚假的安全感"。

但这事儿换一个角度看——不是 AI 不行，是你把 AI 当实习生用了。给他一把螺丝刀让他自己修发动机，他当然会搞砸。

你给他一本维修手册让他照着来，结果就不一样了。

今天聊聊怎么搭一条真正能用的 AI 测试生成流水线。

## AI 写测试的"不可能三角"

先定义一下问题。用 AI 生成测试代码，有三大诉求：

| 诉求 | 什么意思 |
|------|----------|
| **覆盖率** | 各种分支、边界条件都测到 |
| **真实性** | 测试真的在 run，不是 `assert True` 糊弄 |
| **可维护性** | 代码过段时间重构了，测试还能看 |

问题是这三个东西天然冲突。

你要覆盖率，AI 会无脑生成大量重复测试。你要真实性，最稳妥的办法就是让 AI 写最保守的断言——但保守意味着测不出什么有价值的东西。你要可维护性，就得多写注释、抽公共方法——这又跟 AI 的"一句话干完"风格对着干。

💡 **核心洞察：AI 测试生成的瓶颈不在模型能力，而在约束条件不够。** 不给规矩，AI 就按"最低能耗路径"走——怎么写省 token 就怎么来。

## 人工 vs AI vs 混合：差距在哪

我拿同一个 Python 函数测了三轮。

**被测函数（一个简单的价格计算器）：**

```python
def calculate_price(base_price: float, discount_rate: float, tax_rate: float) -> dict:
    """计算最终价格
    
    Args:
        base_price: 基础价格（必须大于0）
        discount_rate: 折扣率（0-1之间）
        tax_rate: 税率（0-1之间）
    
    Returns:
        dict: {final_price, original_price, discount_amount, tax_amount}
    """
    if base_price <= 0:
        raise ValueError("base_price must be positive")
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")
    if not 0 <= tax_rate <= 1:
        raise ValueError("tax_rate must be between 0 and 1")
    
    discount_amount = base_price * discount_rate
    after_discount = base_price - discount_amount
    tax_amount = after_discount * tax_rate
    final_price = after_discount + tax_amount
    
    return {
        "final_price": round(final_price, 2),
        "original_price": round(base_price, 2),
        "discount_amount": round(discount_amount, 2),
        "tax_amount": round(tax_amount, 2),
    }
```

**方案 A：纯人工写（15 分钟）** — 8 个测试，覆盖所有边界条件、异常路径、浮点精度问题。质量高，但慢。

**方案 B：纯 AI 直接生成（30 秒）** — 15 个测试。看起来覆盖很全面，但仔细看了发现：`test_zero_discount` 里的断言写错了（用了 `assertEqual` 但比较的是浮点数）、`test_negative_discount` 用的异常类型是通用的 `Exception` 而非 `ValueError`。一半的测试要么跑不过，要么测的点不对。

**方案 C：AI + 约束条件生成（2 分钟）** — 先给 AI 明确规则（用 pytest、用 `pytest.approx` 处理浮点、异常必须匹配具体类型），再生成。结果 10 个测试，9 个直接能跑通，最后一个 mock 路径没覆盖对——但那是函数的实际 bug，不是测试的问题。

结论很直白：AI 不是不能写测试，是**裸写不行**。

## 搭一套 AI 测试生成流水线，三步搞定

下面是我跑了几轮之后收敛到的最小可行方案。

### 第一步：定义你的测试规范

AI 需要一份显式的"测试编写规范"。不要假设它知道你项目的惯例。

创建一个 `.ai-test-rules.md` 放到项目根目录：

```markdown
# AI Test Generation Rules

## Tech Stack
- Python 3.11+, pytest 8.x, pytest-cov
- pytest.approx() for float comparisons
- unittest.mock for mocking external services

## Conventions
1. One test file per module: `tests/test_<module>.py`
2. Use pytest fixtures, NOT setUp/tearDown
3. Test naming: `test_<function>_<scenario>`
4. Every test must have a docstring describing the scenario
5. Mock all external HTTP calls at the session level
6. Edge cases are mandatory: empty input, None, overflow, zero

## What NOT to do
- Do NOT use assert True
- Do NOT catch and swallow exceptions in tests
- Do NOT test private functions (underscore prefix) directly
- Do NOT write integration tests in unit test files
```

这份规范贴给 AI 之后，生成质量直接上一个台阶。不是 AI 变聪明了，是它终于知道规矩了。

### 第二步：AI + 代码分析 → 精准生成

与其直接让 AI"给这个文件写测试"，不如先做代码分析，把关键信息喂给 AI。

我写了个小脚本做这件事：

```python
import ast
import json

def analyze_file_for_testing(filepath):
    """提取函数签名和文档，供 AI 生成测试用"""
    with open(filepath) as f:
        tree = ast.parse(f.read())
    
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_info = {
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "has_return": any(
                    isinstance(n, ast.Return) for n in ast.walk(node)
                ),
                "lineno": node.lineno,
                "docstring": ast.get_docstring(node) or "",
            }
            # 收集异常处理
            handlers = []
            for child in ast.walk(node):
                if isinstance(child, ast.Raise):
                    handlers.append("raises exception")
            func_info["handlers"] = handlers
            functions.append(func_info)
    
    return {"file": filepath, "functions": functions}
```

输出长这样：

```json
{
  "file": "pricing.py",
  "functions": [
    {
      "name": "calculate_price",
      "args": ["base_price", "discount_rate", "tax_rate"],
      "has_return": true,
      "docstring": "计算最终价格...",
      "handlers": ["raises ValueError"]
    }
  ]
}
```

把这个 JSON + `.ai-test-rules.md` 一起喂给 AI，生成效率完全不同。

💡 **我试过的 prompt 模板：**

```
根据以下函数分析，生成 pytest 单元测试文件。

测试规范：{把 .ai-test-rules.md 粘贴进来}

函数分析：
{analyze_file_for_testing() 的输出}

要求：
1. 完整覆盖所有函数，包括所有异常路径
2. 每个测试有 docstring
3. 用 pytest.approx 处理浮点断言
4. 直接用代码块输出，不要解释
```

### 第三步：覆盖率驱动迭代

别指望一次生成就搞定。跑覆盖率，然后让 AI 补漏。

```bash
pytest --cov=src --cov-report=term-missing tests/
```

看输出里 `MISSED` 列——那些就是 AI 没覆盖到的行。把这份报告发回给 AI：

```
以下函数的分支未被测试覆盖，请补充测试：
{messy coverage output}
```

通常两到三轮迭代后，覆盖率能到 85% 以上。剩下的 15% 通常是真正的边界情况（比如网络超时、磁盘写满），人工补两三个测试就行了。

## 这套方案的硬约束

坦诚讲，不是所有项目都适合这套流程。

**❌ 不擅长的场景：**

1. **UI 密集型代码** — AI 生成的 Selenium/Playwright 测试极其脆弱，selector 一变就红
2. **异步/并发逻辑** — asyncio 代码的测试，AI 经常搞混 event loop 的生命周期
3. **复杂状态机** — 多状态流转的测试，AI 生成的路径覆盖要么不全要么重复
4. **遗留代码** — 没有类型注解、函数 500 行起步的代码，AI 生成的测试又长又看不懂

**✅ 适合的场景：**

1. **纯函数/工具函数** — 输入输出清晰的函数，AI 的表现最好
2. **API 封装层** — 一个函数对应一个 API 端点，模式固定
3. **数据转换函数** — JSON 转 XML、时间格式转换这类纯逻辑
4. **新项目起步** — 从零开始的项目，先让 AI 写一批基础测试，人工迭代

## 几个踩过的坑

**坑 1：AI 会悄悄简化逻辑**

我遇到过 AI 生成的测试用它自己重写的简化版函数来验证原函数——等于自己抄自己的作业然后说全对。肉眼很难发现，因为测试文件里没有显式的 mock。

**修复方法：** 每次跑完测试后，随机抽 3 个测试，手动检查它的断言逻辑是不是在绕圈子。

**坑 2：浮点比较是重灾区**

AI 写 `assert result == 0.1` 时眼睛都不眨。但在 Python 里 `0.1 + 0.2 != 0.3`。不教它用 `pytest.approx`，你永远有一批浮点测试既不通也不报错（因为刚好在某些平台下神奇地相等了）。

**修复方法：** 测试规范里显式要求用 `pytest.approx`，并且在 CI 里跑不同架构。

**坑 3：mock 过深**

AI 默认会 mock 一切外部依赖，包括标准库。结果你测的不是你的代码，测的是"AI 对标准库的理解"。有一次 AI mock 了 `requests.get` 但忘了配 `status_code`，测试跑绿灯但实际代码里调了三次 `response.json()` 而 mock 只配了一次返回值——静默通过。

**修复方法：** 限制 mock 深度——只 mock 网络/数据库/文件系统，标准库和第三方库的核心方法不 mock。

## 聊聊我的感受

跑了几个月 AI 测试生成，我对它的定位变了三次。

最早觉得是神器——"交给 AI，以后不用写测试了"。

然后觉得是鸡肋——"AI 写的都是表面测试，不如不写"。

现在觉得是**工具**——恰当地用，能让你的测试密度提升 3-5 倍，但替代不了你对"什么值得测"的判断。

写测试这件事实质上是对代码的逻辑建模过程。你先把逻辑跑一遍，边边角角摸清楚，然后把它写下来。这个过程本身就是代码质量提升的一部分。AI 帮你做的是**执行层的加速**——它会打字、会找文档、会复用模式。但"测什么"的决策权，始终在你这儿。

所以我的最终建议很直白：

> 用 AI 写测试的骨架，自己写测试的灵魂。

跑完流水线，拿到的是一套覆盖率 85%、语法正确的测试套件。剩下的 15%——那些真正暴露业务理解的边界条件——自己补上，你的测试就从"数量好看"变成了"真有用"。

---
——Seb

*如果你也在搭类似的流水线，有什么坑或者心得，欢迎交流。觉得有用的话，去 GitHub 上给我的项目点个星吧。*
