---
name: "prd-writer"
description: "Write concise product requirement notes by inspecting page artifacts. Invoke when user asks for PRD, 需求文档, 需求细则, or page logic summary."
---

# PRD Writer

Write page requirement docs that are short by default. The goal is "enough to execute", not "everything visible on the screen".

## Workflow

1. Read the source artifact first.
   - If the user gives a route or page path, locate the page component and related constants.
   - If the user gives a prototype or screenshot, inspect that artifact before writing.
   - If both UI and code exist, treat code as the rule source.

2. Extract only product-relevant logic.
   - Focus on search, tabs, filters, sorting, list rules, card actions, submit logic, empty states, URL sync, and data mapping.
   - Keep exact copy only when the wording changes behavior or decision.
   - Ignore decorative layout details unless the user explicitly asks for them.

3. Group by function, not by every visible block.
   - Prefer `1、功能点` style output.
   - Merge related logic into the same item.
   - Do not force `入口` / `权限` / `模块展示` sections on every page.

4. Switch to detailed mode only when needed.
   - Use detailed output only if the user explicitly asks for `详细版` / `完整PRD` / `逐字段` / `全量需求`, or the page is a complex publish form.
   - In detailed mode, still stay compact and skip decorative content.

5. Cut before returning.
   - Remove repeated explanations.
   - Remove lines that only say something exists but do not explain rules.
   - Omit assumptions unless the user explicitly asks to补齐.

## Default Output Rules

- Prefer Chinese unless the user asks otherwise.
- Default to 3-8 numbered items for one page.
- Each item should contain the rule itself, not a long preface.
- Mention limits, options, sorting, filtering, URL handling, result states, and action consequences when they matter.
- Do not automatically include `入口` / `权限` unless the user asks for them or the page truly depends on access differences.
- Do not restate obvious UI chrome like "展示标题" or "展示按钮" unless there is logic tied to it.
- Do not explain product value, design rationale, implementation effort, or future-state ideas unless asked.

## Detailed Mode Rules

- If the user explicitly asks for a detailed PRD, follow their structure first.
- Keep exact strings for placeholders, button copy, and error copy when those strings matter.
- Cover required state, options, limits, success/failure, preview, and delete logic only when the page defines them.

## Output Format

### 三段式结构

1. **需求版本与背景**：用1-2句话简述痛点
2. **交互流程**：梳理核心主流程
3. **需求详情**：必须严格输出 Markdown 三列表格

### 表格格式

```
| 步骤/板块 | 详情 (必须穷举前置条件、正常交互、异常校验、边界限制) | 示意图 |
| :--- | :--- | :--- |
| (具体模块) | (按点列出校验逻辑) | (占位) |
```

### 核心规范

1. 必须使用 Markdown 三列表格
2. **飞书兼容性警告**：绝对禁止在表格内使用 `<br>`、`<p>` 等任何 HTML 换行标签
3. 表格单元格内如果需要分点或分段描述，请直接使用分号（；）、顿号（、）分隔，或者使用全角空格排版。必须确保输出的是最纯粹的文本
4. **视觉信息过滤**：禁止描述任何视觉样式（如颜色、圆角、阴影、渐变等）！只保留组件名称、状态和文案内容

## Example Output

### 需求版本

| 版本 | 变更内容 | 上线时间 |
| ---- | -------- | -------- |
| v1.0 | 首页三大核心场景入口上线 | 2026- |

### 需求背景

提供三大核心场景入口，降低操作门槛，提升效率。

### 交互逻辑

| Step 1 : 入口选择 | 用户在首页选择对应场景入口卡片 |
| ----------------- | ------------------------------------------------------------ |
| Step 2 : 流程分流 | 根据入口弹出配置弹窗或直接跳转合成页 |

### 需求详情

| 功能/模块 | 功能详情 | 图示 |
| -------------- | -------- | ---- |
| 底部弹窗 | UI显示：弹窗标题区（文案：选择克隆方式；组件：帮助图标）；选项卡片区（录制声音卡片文案：录制声音；上传文件卡片文案：上传文件）；组件：黑色遮罩层。交互逻辑：点击"录制声音"关闭弹窗，跳转至【录制页面】；点击"上传文件"关闭弹窗，延迟300ms后跳转至【配置页面】；点击黑色遮罩层关闭弹窗，不执行跳转；弹窗动画时长300ms；需防抖处理避免多次点击。 | [占位] |
