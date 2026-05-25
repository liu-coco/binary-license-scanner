#!/usr/bin/env python3
"""Extract linked libraries from a binary file across macOS, Linux, and Windows."""

import argparse
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

# Libraries to exclude from results (system internals, not real dependencies)
SKIP_PATTERNS = [
    r"^linux-vdso\.so",
    r"^linux-gate\.so",
    r"^/usr/lib/system/",  # macOS system internals
]


def is_pe_file(path: Path) -> bool:
    """Check if file is a Windows PE executable."""
    try:
        with open(path, "rb") as f:
            return f.read(2) == b"MZ"
    except OSError:
        return False


def is_macho_file(path: Path) -> bool:
    """Check if file is a macOS Mach-O binary."""
    magic_map = {
        b"\xfe\xed\xfa\xce": True,
        b"\xce\xfa\xed\xfe": True,
        b"\xfe\xed\xfa\xcf": True,
        b"\xcf\xfa\xed\xfe": True,
        b"\xca\xfe\xba\xbe": True,
    }
    try:
        with open(path, "rb") as f:
            header = f.read(4)
            return header in magic_map
    except OSError:
        return False


def is_elf_file(path: Path) -> bool:
    """Check if file is an ELF binary."""
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"\x7fELF"
    except OSError:
        return False


def parse_otool_output(output: str) -> list[str]:
    """Parse macOS otool -L output."""
    libs = []
    for line in output.strip().split("\n"):
        line = line.strip()
        # Skip the header line (binary path ending with ':')
        if line.endswith(":"):
            continue
        # Lines format: "/path/to/lib.dylib (compatibility version ...)"
        if "(" in line:
            lib_path = line.split("(")[0].strip()
            if lib_path.startswith("/"):
                libs.append(lib_path)
    return libs


def parse_ldd_output(output: str) -> list[str]:
    """Parse Linux ldd output."""
    libs = []
    for line in output.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        match = re.match(r"\s*(.+?)\s*=>\s*(.+?)\s+\(0x", line)
        if match:
            libs.append(match.group(2))
        else:
            parts = line.split()
            if parts:
                libs.append(parts[0])
    return libs


def parse_dumpbin_output(output: str) -> list[str]:
    """Parse Windows dumpbin /dependents output."""
    libs = []
    in_deps = False
    for line in output.strip().split("\n"):
        line = line.strip()
        if "dependencies:" in line.lower():
            in_deps = True
            continue
        if in_deps:
            if not line or line.startswith("Summary"):
                break
            if re.match(r"^\d", line):
                break
            if line.endswith(".dll"):
                libs.append(line)
    return libs


def parse_objdump_output(output: str) -> list[str]:
    """Parse objdump -p output (cross-platform fallback)."""
    libs = []
    for line in output.strip().split("\n"):
        line = line.strip()
        if "NEEDED" in line:
            match = re.search(r"NEEDED\s+(.+)", line)
            if match:
                libs.append(match.group(1).strip())
        elif "DLL Name:" in line:
            match = re.search(r"DLL Name:\s*(.+)", line)
            if match:
                libs.append(match.group(1).strip())
    return libs


def is_skipped(lib: str) -> bool:
    """Check if a library should be skipped."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, lib):
            return True
    return False


def get_lib_basename(lib_path: str) -> str:
    """Extract basename from a library path, stripping version suffixes."""
    name = Path(lib_path).name
    name = re.sub(r"(\.dylib|\.so|\.dll).*", r"\1", name)
    return name


def extract_dependencies(path: Path) -> list[dict]:
    """Extract library dependencies from a binary file."""
    system = platform.system()
    output = ""

    if system == "Darwin":
        result = subprocess.run(
            ["otool", "-L", str(path)], capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Warning: otool failed: {result.stderr}", file=sys.stderr)
        output = result.stdout
        raw_libs = parse_otool_output(output)

    elif system == "Linux":
        if is_elf_file(path):
            result = subprocess.run(
                ["ldd", str(path)], capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Warning: ldd failed: {result.stderr}", file=sys.stderr)
            output = result.stdout
            raw_libs = parse_ldd_output(output)
        elif is_pe_file(path):
            result = subprocess.run(
                ["objdump", "-p", str(path)], capture_output=True, text=True
            )
            output = result.stdout
            raw_libs = parse_objdump_output(output)
        else:
            print(f"Error: Cannot determine binary format of {path}", file=sys.stderr)
            sys.exit(1)

    elif system == "Windows":
        if is_pe_file(path):
            result = subprocess.run(
                ["dumpbin", "/dependents", str(path)],
                capture_output=True, text=True, shell=True
            )
            output = result.stdout
            raw_libs = parse_dumpbin_output(output)
            if not raw_libs:
                result = subprocess.run(
                    ["objdump", "-p", str(path)], capture_output=True, text=True
                )
                output = result.stdout
                raw_libs = parse_objdump_output(output)
        elif is_elf_file(path):
            result = subprocess.run(
                ["objdump", "-p", str(path)], capture_output=True, text=True
            )
            output = result.stdout
            raw_libs = parse_objdump_output(output)
        else:
            print(f"Error: Cannot determine binary format of {path}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: Unsupported platform: {system}", file=sys.stderr)
        sys.exit(1)

    # Deduplicate and filter
    seen = set()
    libs = []
    for lib in raw_libs:
        basename = get_lib_basename(lib)
        if is_skipped(lib) or is_skipped(basename):
            continue
        if basename not in seen:
            seen.add(basename)
            libs.append({"full_path": lib, "name": basename})

    return libs


def main():
    parser = argparse.ArgumentParser(
        description="Extract linked libraries from a binary file"
    )
    parser.add_argument("binary", type=Path, help="Path to the binary file")
    parser.add_argument(
        "-j", "--json", action="store_true", help="Output as JSON (default)"
    )
    parser.add_argument(
        "--names-only", action="store_true", help="Output only library names"
    )
    args = parser.parse_args()

    if not args.binary.exists():
        print(f"Error: File not found: {args.binary}", file=sys.stderr)
        sys.exit(1)

    libs = extract_dependencies(args.binary)

    if args.names_only:
        for lib in libs:
            print(lib["name"])
    else:
        print(json.dumps({"platform": platform.system(), "libraries": libs}, indent=2))


if __name__ == "__main__":
    main()
