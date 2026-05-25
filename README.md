<p align="center">
  <h1 align="center">🔍 Binary License Scanner<br><sub>二进制许可证扫描器</sub></h1>
</p>

<p align="center">
  <strong>Scan compiled binaries. Audit open source licenses. Ship compliant software.</strong><br>
  <sub>分析编译后的二进制文件，审计开源许可证，确保合规交付。</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/platform-macOS%20|%20Linux%20|%20Windows-lightgrey.svg" alt="Cross-platform macOS Linux Windows">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Claude%20Code-skill-8A2BE2.svg" alt="Claude Code Skill">
</p>

---

## Table of Contents | 目录

- [What is Binary License Scanner? | 什么是二进制许可证扫描器？](#what-is-binary-license-scanner)
- [Features | 功能特性](#features)
- [Quick Start | 快速开始](#quick-start)
- [Installation | 安装](#installation)
- [Usage | 使用方法](#usage)
- [How It Works | 工作原理](#how-it-works)
- [Supported Libraries | 支持的库识别](#supported-libraries)
- [Use Cases | 使用场景](#use-cases)
- [FAQ | 常见问题](#faq)
- [Contributing | 贡献指南](#contributing)
- [License | 许可证](#license)

---

## What is Binary License Scanner?

**Binary License Scanner** is an open source license compliance tool that extracts linked library dependencies from compiled binaries (.dylib, .so, .dll, executables) and generates a complete license audit report.

Stop guessing what third-party libraries are bundled in your binary — run one command and get a Markdown table with every library's name, official homepage, GitHub repository, and open source license.

### 什么是二进制许可证扫描器？

**二进制许可证扫描器** 是一个开源许可证合规工具，能从编译后的二进制文件中提取所有链接库依赖，并生成完整的许可证审计报告。

不再猜测你的二进制文件里捆绑了哪些第三方库 — 一条命令即可获得 Markdown 表格，列出每个库的名称、官网地址、GitHub 仓库和开源许可证。

---

## Features

| Feature | Description |
|---------|-------------|
| **Cross-Platform** | macOS (Mach-O), Linux (ELF), Windows (PE) — auto-detected |
| **Zero Config** | Point at a binary, get results. No setup required |
| **Built-in Knowledge Base** | 150+ common libraries pre-indexed with licenses and URLs |
| **Web Search Fallback** | Unknown libraries automatically looked up via web search |
| **Markdown Output** | Clean, copy-paste ready table for compliance docs |
| **System Library Detection** | OS-vendor libraries (libc, kernel32.dll) flagged correctly |

### 功能特性

| 功能 | 说明 |
|------|------|
| **跨平台** | macOS (Mach-O)、Linux (ELF)、Windows (PE) 自动检测 |
| **零配置** | 指向二进制文件，即刻出结果 |
| **内置知识库** | 预置 150+ 常见库的许可证和 URL 信息 |
| **网络搜索回退** | 未知库自动通过网络搜索查找信息 |
| **Markdown 输出** | 整洁、可直接复制用于合规文档的表格 |
| **系统库识别** | 正确标记操作系统供应商库（libc、kernel32.dll 等） |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/liu-coco/binary-license-scanner.git
cd binary-license-scanner

# Scan a binary
python3 scripts/analyze_binary.py /path/to/your/binary

# Example: scan macOS system binary
python3 scripts/analyze_binary.py /bin/ls
```

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/liu-coco/binary-license-scanner.git
cd binary-license-scanner

# 扫描一个二进制文件
python3 scripts/analyze_binary.py /path/to/your/binary

# 示例：扫描 macOS 系统命令
python3 scripts/analyze_binary.py /bin/ls
```

**Output | 输出：**
```json
{
  "platform": "Darwin",
  "libraries": [
    {"full_path": "/usr/lib/libutil.dylib", "name": "libutil.dylib"},
    {"full_path": "/usr/lib/libSystem.B.dylib", "name": "libSystem.B.dylib"}
  ]
}
```

---

## Installation

### As a Claude Code Skill

This tool is built as a **Claude Code Skill**. Once installed, invoke it directly:

```
/binary-license-scanner analyze /path/to/binary
```

Install via the `.skill` file from [Releases](https://github.com/liu-coco/binary-license-scanner/releases).

### Standalone Python Script

No dependencies beyond Python 3.8+ and standard system tools (`otool` on macOS, `ldd` on Linux, `dumpbin` on Windows).

```bash
chmod +x scripts/analyze_binary.py
```

### 安装

### 作为 Claude Code 技能

本工具构建为 **Claude Code 技能**。安装后直接调用：

```
/binary-license-scanner analyze /path/to/binary
```

通过 [Releases](https://github.com/liu-coco/binary-license-scanner/releases) 下载 `.skill` 文件安装。

### 作为独立 Python 脚本

除了 Python 3.8+ 和标准系统工具外无其他依赖。

```bash
chmod +x scripts/analyze_binary.py
```

---

## Usage

```bash
# JSON output (default)
python3 scripts/analyze_binary.py /path/to/binary

# Names only
python3 scripts/analyze_binary.py /path/to/binary --names-only
```

### With Claude Code

```
/binary-license-scanner 分析 /path/to/binary
```

The skill will:
1. Extract linked libraries using the script
2. Check the built-in knowledge base for known libraries
3. Search the web for unknown libraries
4. Output a formatted Markdown license audit table

### 使用方法

```bash
# JSON 格式输出（默认）
python3 scripts/analyze_binary.py /path/to/binary

# 仅输出库名
python3 scripts/analyze_binary.py /path/to/binary --names-only
```

### 配合 Claude Code 使用

```
/binary-license-scanner 分析 /path/to/binary
```

技能将自动：
1. 使用脚本提取链接库
2. 在内置知识库中查找已知库
3. 对未知库进行网络搜索
4. 输出格式化的 Markdown 许可证审计表格

---

## Output Example | 输出示例

```markdown
## License Audit: myapp

| Library | Homepage / GitHub | License |
|---------|-------------------|---------|
| libc++.1.dylib | [libcxx.llvm.org](https://libcxx.llvm.org) | Apache-2.0 |
| libcurl.dylib | [github.com/curl/curl](https://github.com/curl/curl) | MIT |
| libSystem.B.dylib | — | System (Apple) |
| libz.1.dylib | [zlib.net](https://zlib.net) | zlib |
```

---

## How It Works

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Binary     │────▶│ Extract Linked  │────▶│ Lookup Each      │
│   (.dylib,   │     │ Libraries       │     │ Library          │
│   .so, .dll) │     │ (otool/ldd/     │     │ (knowledge base  │
│              │     │  dumpbin)        │     │  + web search)   │
└──────────────┘     └─────────────────┘     └────────┬─────────┘
                                                       │
                                              ┌────────▼─────────┐
                                              │  Markdown Table  │
                                              │  License Audit   │
                                              └──────────────────┘
```

1. **Detect binary format** — PE (Windows), Mach-O (macOS), or ELF (Linux)
2. **Invoke platform tool** — `otool -L` / `ldd` / `dumpbin /dependents`
3. **Parse dependencies** — extract library names, deduplicate
4. **Lookup** — match against 150+ known libraries; web search for unknowns
5. **Render** — Markdown table with Library, Homepage, License columns

### 工作原理

1. **检测二进制格式** — PE (Windows)、Mach-O (macOS) 或 ELF (Linux)
2. **调用平台工具** — `otool -L` / `ldd` / `dumpbin /dependents`
3. **解析依赖** — 提取库名称，去重
4. **查询匹配** — 与 150+ 已知库匹配；未知库通过网络搜索
5. **渲染输出** — 包含库名、主页、许可证列的 Markdown 表格

---

## Supported Libraries | 支持的库识别

The knowledge base (`references/known-libraries.md`) covers:

| Category | Libraries |
|----------|-----------|
| **C/C++ Runtimes** | libc++, libstdc++, libgcc_s, libunwind |
| **Compression** | zlib, bzip2, lzma, lz4, zstd |
| **SSL/TLS/Crypto** | OpenSSL, GnuTLS, NSS |
| **Data Formats** | libxml2, expat, json-c, yaml, protobuf |
| **Databases** | PostgreSQL, MySQL, SQLite, MariaDB, Redis |
| **Graphics/UI** | libpng, libjpeg, libwebp, freetype, cairo, GTK, Qt, SDL2, Vulkan |
| **Audio/Video** | FFmpeg, x264, x265, libvpx, opus, vorbis, FLAC, PulseAudio |
| **Networking** | curl, nghttp2, libssh2, libwebsockets, ZeroMQ |
| **Math/Scientific** | OpenBLAS, BLAS, LAPACK, FFTW, GSL, GMP |
| **Language Runtimes** | Python, Lua, Perl, Ruby, PHP, V8, Node.js |

知识库覆盖 150+ 常用库，涵盖 C/C++ 运行时、压缩、加密、数据格式、数据库、图形界面、音视频、网络、科学计算、语言运行时等类别。

---

## Use Cases | 使用场景

- **Open source compliance audits** — verify all third-party licenses before release
- **M&A due diligence** — audit a target company's binary dependencies
- **SBOM generation** — produce a Software Bill of Materials for binaries
- **CI/CD pipelines** — gate deployments on license policy compliance
- **Security research** — understand what libraries a binary links against
- **开源合规审计** — 发布前验证所有第三方许可证
- **并购尽职调查** — 审计目标公司的二进制依赖
- **SBOM 生成** — 为二进制文件生成软件物料清单
- **CI/CD 流水线** — 基于许可证策略合规性控制部署
- **安全研究** — 了解二进制文件链接了哪些库

---

## FAQ | 常见问题

<details>
<summary><strong>Q: What binary formats are supported? | 支持哪些二进制格式？</strong></summary>

- **macOS**: Mach-O (.dylib, executables)
- **Linux**: ELF (.so, executables)
- **Windows**: PE (.dll, .exe)
</details>

<details>
<summary><strong>Q: Does it work cross-platform? | 是否支持跨平台？</strong></summary>

Yes. The script auto-detects the host platform and uses the appropriate tool. If the binary format doesn't match the host (e.g., analyzing a PE file on macOS), it falls back to `objdump`.

是的。脚本自动检测宿主平台并使用对应工具。如果二进制格式与宿主不匹配（如在 macOS 上分析 PE 文件），会自动回退到 `objdump`。
</details>

<details>
<summary><strong>Q: What if a library isn't in the knowledge base? | 如果库不在知识库中怎么办？</strong></summary>

The Claude Code skill will automatically search the web for unknown libraries and present their license and homepage. The standalone script only extracts library names — you need to look up licenses yourself or contribute to the knowledge base.

Claude Code 技能会自动搜索未知库的许可证和主页。独立脚本仅提取库名 — 你需要自行查找许可证或向知识库贡献数据。
</details>

<details>
<summary><strong>Q: Can I contribute library data? | 我可以贡献库数据吗？</strong></summary>

Absolutely! Edit `references/known-libraries.md` and open a pull request. Every addition helps the community ship compliant software.

当然！编辑 `references/known-libraries.md` 并提交 Pull Request。每一条贡献都能帮助社区交付合规软件。
</details>

---

## Contributing | 贡献指南

Contributions are welcome! Here's how:

1. **Add libraries** — edit `references/known-libraries.md` with new entries
2. **Improve detection** — enhance `scripts/analyze_binary.py` for edge cases
3. **Report bugs** — open an [Issue](https://github.com/liu-coco/binary-license-scanner/issues)

Please ensure:
- Library URLs are official or the primary GitHub mirror
- License names follow [SPDX identifiers](https://spdx.org/licenses/) where possible
- Script changes are tested on at least one platform

欢迎贡献！参与方式：

1. **添加库** — 编辑 `references/known-libraries.md` 添加新条目
2. **改进检测** — 增强 `scripts/analyze_binary.py` 的边缘情况处理
3. **报告 Bug** — 提交 [Issue](https://github.com/liu-coco/binary-license-scanner/issues)

请确保：
- 库 URL 为官方网站或主要 GitHub 镜像
- 许可证名称尽可能遵循 [SPDX 标识符](https://spdx.org/licenses/)
- 脚本变更至少在一种平台上通过测试

---

## License | 许可证

MIT © [liu-coco](https://github.com/liu-coco)

This project is open source and free to use for personal and commercial purposes. See [LICENSE](LICENSE) for details.

本项目为开源项目，可自由用于个人和商业用途。详见 [LICENSE](LICENSE)。

---

<p align="center">
  <sub>Built with ❤️ for the open source compliance community | 为开源合规社区而构建</sub>
</p>
