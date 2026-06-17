<div align="center">

```
 ██╗  ██╗███████╗██╗   ██╗████████╗██████╗  █████╗  ██████╗███████╗
 ██║ ██╔╝██╔════╝╚██╗ ██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
 █████╔╝ █████╗   ╚████╔╝    ██║   ██████╔╝███████║██║     █████╗  
 ██╔═██╗ ██╔══╝    ╚██╔╝     ██║   ██╔══██╗██╔══██║██║     ██╔══╝  
 ██║  ██╗███████╗   ██║      ██║   ██║  ██║██║  ██║╚██████╗███████╗
 ╚═╝  ╚═╝╚══════╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝
```

### *Python-Based Keystroke Capture Framework for Endpoint Threat Research*

<br/>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](.)
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-T1056.001-red?style=for-the-badge)](https://attack.mitre.org/techniques/T1056/001/)
[![CipherNest](https://img.shields.io/badge/Research-CipherNest-1a1a2e?style=for-the-badge)](https://github.com/ciphernest)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20%2F%20PoC-orange?style=for-the-badge)](.)

<br/>

> **A keystroke logging proof-of-concept built to teach defenders what they're up against.**  
> Built by [CipherNest](https://github.com/ciphernest) — security research, stripped bare.

</div>

---

## ⚠️ Legal Disclaimer

> This project is developed **strictly for educational purposes**, authorized penetration testing engagements, and academic security research. Deploying this tool on any system you do not own — or without **explicit written authorization** — is a criminal offense under:
>
> - 🇮🇳 **India**: Information Technology Act, 2000 — Section 43, 66, 66C  
> - 🇺🇸 **USA**: Computer Fraud and Abuse Act (CFAA), 18 U.S.C. § 1030  
> - 🇬🇧 **UK**: Computer Misuse Act 1990  
> - 🌐 **EU**: NIS2 Directive and national equivalents  
>
> **The author and CipherNest bear zero liability for unauthorized or malicious use.**  
> This code exists to build defenders — not to arm attackers.

---

## Table of Contents

1. [Overview](#-overview)
2. [Research Context](#-research-context)
3. [MITRE ATT&CK Mapping](#-mitre-attck-mapping)
4. [Features](#-features)
5. [Architecture](#-architecture)
6. [Installation](#-installation)
7. [Usage](#-usage)
8. [Sample Output](#-sample-output)
9. [Detection Engineering](#-detection-engineering)
10. [Limitations & Scope](#-limitations--scope)
11. [Ethical Boundaries](#-ethical-boundaries)
12. [Roadmap](#-roadmap)
13. [Author](#-author)
14. [License](#-license)

---

## 🔍 Overview

**KeyTrace** is a lightweight, research-grade keystroke logging framework written in Python. It captures keyboard input at the OS listener level, timestamps each event, and persists the log to disk — mirroring exactly the behavior of real-world credential-harvesting implants documented in threat intelligence reports.

This project is published under the **CipherNest** research brand as an educational artifact. Its goals are threefold:

- **Offense awareness** — understand how input capture works at the implementation level
- **Detection engineering** — build signatures, auditd rules, and SIEM alerts against this exact behavior
- **Red team training** — use in authorized lab environments to simulate T1056.001 activity

If you're a defender who wants to know what you're detecting, this project shows you the source code.

---

## 📚 Research Context

Keyloggers are one of the oldest and most reliable forms of credential theft. Despite their age, they remain highly effective against unmonitored endpoints. Modern threat actors — from commodity RAT operators to APT groups — embed keystroke capture as a standard collection module.

### Why this matters to defenders

| Threat Category | Real-world Examples |
|---|---|
| Commodity Malware | Agent Tesla, HawkEye, Snake Keylogger |
| RAT Modules | njRAT, AsyncRAT, DarkComet |
| APT Implants | FIN7 (Carbanak), Lazarus Group modules |
| InfoStealers | RedLine, Vidar, Formbook |

All of the above implement the same fundamental primitive: **hook keyboard input → buffer → exfiltrate**. KeyTrace implements the first two stages without network egress, making it safe to study in isolation.

### Python's role in real-world keyloggers

Python-based keyloggers appear frequently in incidents because:

1. `pynput` and `keyboard` libraries offer OS-level hook access with minimal privilege requirements
2. Python scripts compile to PyInstaller binaries that evade simple hash-based detection
3. Cross-platform support reduces attacker development overhead
4. Script-based delivery bypasses many application whitelisting controls

---

## 🎯 MITRE ATT&CK Mapping

KeyTrace directly implements documented adversary techniques:

| Tactic | Technique ID | Technique Name | KeyTrace Behavior |
|---|---|---|---|
| **Collection** | T1056.001 | Input Capture: Keylogging | Core keystroke listener |
| **Credential Access** | T1056 | Input Capture | Password harvesting via timing context |
| **Discovery** | T1082 | System Information Discovery | Platform/OS fingerprinting (config) |
| **Persistence** *(extended)* | T1053.003 | Cron Job | Autostart via cron (optional module) |
| **Defense Evasion** *(extended)* | T1027 | Obfuscated Files or Information | Base64 log encoding (optional module) |

This mapping enables security teams to build **ATT&CK-aligned detection rules** directly from this project's behavior.

---

## ✨ Features

```
Core Engine
├── Real-time keystroke capture via pynput OS listener hooks
├── Full Unicode support — captures international keyboard layouts
├── Special key normalization (Shift, Ctrl, Alt, Fn keys tagged cleanly)
├── Timestamp precision per keystroke (ISO 8601 format)
└── Configurable buffer flush interval (default: 60 seconds)

Logging Layer
├── Persistent log output to configurable file path
├── Session boundary markers (start/stop timestamps)
├── Graceful shutdown with final buffer flush
└── Log rotation support (size-based)

Research Modules (optional)
├── Base64 encoded log output (obfuscation simulation)
├── Active window title capture (context tagging)
└── Verbose console mode for live monitoring in lab environments

Platform Support
├── Linux (Ubuntu 20.04+, Kali, Parrot)
└── Windows 10 / 11
```

---

## 🏗️ Architecture

```
keytrace/
├── keytrace.py          ← Entry point, CLI argument parsing
├── listener.py          ← pynput keyboard hook, event dispatch
├── logger.py            ← Log formatting, file I/O, rotation
├── config.py            ← Runtime configuration (paths, intervals, flags)
├── utils.py             ← Key normalization, platform detection, encoding
├── modules/
│   ├── window_tracker.py   ← Active window title capture (optional)
│   └── encoder.py          ← Base64/obfuscation module (optional)
├── logs/
│   └── .gitkeep            ← Output directory (keylog.txt gitignored)
├── requirements.txt
├── .gitignore
└── README.md
```

### Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                   Keyboard Hardware                      │
└──────────────────────────┬──────────────────────────────┘
                           │  OS Keyboard Event
                           ▼
┌─────────────────────────────────────────────────────────┐
│              pynput Listener Thread                      │
│                                                         │
│   on_press(key)                on_release(key)          │
│       │                              │                  │
│       ▼                              ▼                  │
│   Key Normalization           Buffer Flush Trigger      │
│   (printable / special)       (interval or key event)   │
└──────────────────────────┬──────────────────────────────┘
                           │  Normalized keystroke + timestamp
                           ▼
┌─────────────────────────────────────────────────────────┐
│               In-Memory Buffer                          │
│         [ (timestamp, key_str), ... ]                   │
└──────────────────────────┬──────────────────────────────┘
                           │  On flush trigger
                           ▼
┌─────────────────────────────────────────────────────────┐
│               Logger (File I/O)                         │
│                                                         │
│   Format → Append → logs/keylog.txt                     │
│   Optional: Base64 encode before write                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip
- Linux: `sudo` or root for system-level hook (depends on display server)
- Windows: Run as Administrator for full hook coverage

### Steps

```bash
# Clone the repository
git clone https://github.com/ciphernest/keytrace.git
cd keytrace

# (Recommended) Create virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```txt
pynput>=1.7.6
```

> **Why only pynput?**  
> Minimizing dependencies reduces noise in dependency audits and keeps the attack surface of the research tool itself small. This is intentional design — the same principle real-world implants use to avoid detection by package-level scanning.

---

## 🚀 Usage

```bash
# Basic run — logs to ./logs/keylog.txt
python keytrace.py

# Custom output path
python keytrace.py --output /tmp/research_session.txt

# Verbose mode — live keystroke echo to console (lab/demo use)
python keytrace.py --verbose

# Set custom flush interval (seconds)
python keytrace.py --flush-interval 30

# Enable active window tracking (context-aware logs)
python keytrace.py --window-tracking

# Encode log output in Base64 (simulates obfuscation)
python keytrace.py --encode base64

# Stop the listener cleanly
# Press Ctrl+C or send SIGTERM — final buffer flush guaranteed
```

---

## 📄 Sample Output

**Standard log (`logs/keylog.txt`):**

```
====================================================
  KeyTrace Session Start
  Timestamp : 2025-06-18T14:30:00.123456
  Platform  : Linux-6.8.0-generic
  PID       : 14872
====================================================

[2025-06-18T14:30:12.441] s
[2025-06-18T14:30:12.503] s
[2025-06-18T14:30:12.601] h
[2025-06-18T14:30:12.714] [Key.space]
[2025-06-18T14:30:12.812] -
[2025-06-18T14:30:12.899] i
[2025-06-18T14:30:13.012] [Key.space]
[2025-06-18T14:30:13.101] /
[2025-06-18T14:30:13.199] e
[2025-06-18T14:30:13.310] t
[2025-06-18T14:30:13.401] c
[2025-06-18T14:30:13.500] /
[2025-06-18T14:30:13.612] p
[2025-06-18T14:30:13.712] a
[2025-06-18T14:30:13.811] s
[2025-06-18T14:30:13.901] s
[2025-06-18T14:30:14.002] w
[2025-06-18T14:30:14.099] d
[2025-06-18T14:30:14.201] [Key.enter]

====================================================
  KeyTrace Session End
  Timestamp : 2025-06-18T14:45:00.991234
  Duration  : 900.87s
  Keys Captured : 847
====================================================
```

**With window tracking enabled:**

```
[2025-06-18T14:32:01.441] [Window: Terminal — bash] s
[2025-06-18T14:32:01.503] [Window: Terminal — bash] u
[2025-06-18T14:32:11.812] [Window: Firefox — gmail.com] p
[2025-06-18T14:32:11.901] [Window: Firefox — gmail.com] a
[2025-06-18T14:32:12.012] [Window: Firefox — gmail.com] s
[2025-06-18T14:32:12.099] [Window: Firefox — gmail.com] s
```

---

## 🛡️ Detection Engineering

This section is the **most important part of this project** for blue teamers. Every behavior KeyTrace exhibits has a detectable footprint. Here is how to catch it.

### Behavioral Indicators

| Observable Behavior | Where to Look | Confidence |
|---|---|---|
| Python process spawning keyboard listener thread | Process tree / EDR | High |
| File writes to log path at regular intervals | `auditd` file watches | High |
| `pynput` library import / listener thread creation | Sysmon / eBPF tracing | High |
| Elevated privilege Python process | `sudo` audit logs | Medium |
| Autostart cron entry (extended module) | Cron audit / `/etc/cron*` | Medium |

### auditd Rules

Drop these into `/etc/audit/rules.d/keytrace.rules` to detect KeyTrace log writes:

```bash
# Watch KeyTrace default output path
-w /path/to/logs/keylog.txt -p wa -k keylogger_write

# Watch /tmp for suspicious Python log files
-w /tmp -p wa -k tmp_python_write

# Monitor Python processes opening keyboard event files (Linux)
-a always,exit -F arch=b64 -S open -F path=/dev/input -F perm=r -k keyboard_device_read

# Detect cron-based persistence additions
-w /etc/cron.d -p wa -k cron_persistence
-w /var/spool/cron -p wa -k cron_persistence
```

Reload rules:

```bash
sudo auditctl -R /etc/audit/rules.d/keytrace.rules
sudo service auditd restart
```

Query for hits:

```bash
ausearch -k keylogger_write --interpret
ausearch -k keyboard_device_read --interpret
```

### Sysmon Rules (Windows)

```xml
<!-- Event ID 11: FileCreate — log file creation -->
<FileCreate onmatch="include">
  <TargetFilename condition="contains">keylog</TargetFilename>
  <TargetFilename condition="end with">.txt</TargetFilename>
</FileCreate>

<!-- Event ID 10: ProcessAccess — pynput hooking input -->
<ProcessAccess onmatch="include">
  <SourceImage condition="end with">python.exe</SourceImage>
  <GrantedAccess condition="is">0x1fffff</GrantedAccess>
</ProcessAccess>
```

### YARA Rule (PyInstaller-packed variant)

```yara
rule KeyTrace_PyInstaller_Keylogger {
    meta:
        description = "Detects PyInstaller-packed Python keylogger artifacts"
        author      = "CipherNest"
        reference   = "https://github.com/ciphernest/keytrace"
        mitre       = "T1056.001"

    strings:
        $py1 = "pynput" ascii
        $py2 = "on_press" ascii
        $py3 = "on_release" ascii
        $py4 = "keyboard.Listener" ascii
        $log = "keylog" ascii nocase

    condition:
        uint16(0) == 0x5A4D and        // PE header
        3 of ($py*) and
        $log
}
```

### Sigma Rule (SIEM)

```yaml
title: Python Keyboard Listener Process Spawned
id: a3f92c1d-0011-4abc-beef-ciphernest001
status: experimental
description: Detects Python process spawning keyboard listener — possible keylogger activity
author: CipherNest
date: 2025/06/18
references:
  - https://attack.mitre.org/techniques/T1056/001/
tags:
  - attack.collection
  - attack.t1056.001
logsource:
  product: linux
  category: process_creation
detection:
  selection:
    Image|endswith: '/python3'
    CommandLine|contains:
      - 'pynput'
      - 'keyboard.Listener'
      - 'on_press'
  condition: selection
falsepositives:
  - Legitimate accessibility software using keyboard hooks
  - IDE plugins with keyboard shortcut listeners
level: medium
```

---

## 🔒 Limitations & Scope

KeyTrace is deliberately **scoped as a research proof-of-concept**. It does not implement features that would make it production malware:

| Feature | Status | Why |
|---|---|---|
| Network exfiltration / C2 | ❌ Not implemented | Out of ethical scope for this repo |
| Process injection / hiding | ❌ Not implemented | Rootkit territory — separate research domain |
| Anti-forensics / log wiping | ❌ Not implemented | Out of scope |
| Encrypted C2 comms | ❌ Not implemented | Out of scope |
| Encrypted local logs | ⚠️ Optional research module | Demonstrates obfuscation surface for defenders |
| Active window tracking | ⚠️ Optional research module | Useful for detection signature building |
| Cross-platform keyboard hooks | ✅ Implemented | Core research primitive |
| Timestamped persistent logging | ✅ Implemented | Core research primitive |

If you're looking for a full RAT or C2 framework — that's not this project and not this author's work.

---

## ⚖️ Ethical Boundaries

**Only use KeyTrace on:**

- ✅ Your own personal machines and VMs
- ✅ Dedicated security research lab environments (air-gapped preferred)
- ✅ Systems covered by a signed penetration testing scope/authorization letter
- ✅ CTF challenge environments

**Never use KeyTrace on:**

- ❌ Shared or public systems
- ❌ Employer or university systems without written authorization
- ❌ Family or friends' devices (even "to test")
- ❌ Any production environment

Security research is a privilege. Abuse it and you're not a researcher — you're a criminal.

---

## 🗺️ Roadmap

- [ ] AES-256 encrypted log output (research: simulating modern implant obfuscation)
- [ ] YARA rule auto-generation for each build variant
- [ ] Integration demo with auditd pipeline for correlated red/blue lab walkthrough
- [ ] Docker-based isolated test environment with pre-configured detection stack
- [ ] Blog post: *"Building KeyTrace — and then catching it"* on CipherNest

---

## 👤 Author

<div align="center">

**Shivasairaj**  
Security Researcher · CipherNest 

 	www.youtube.com/@CipherNest7


*"The best way to build a detector is to understand the attacker's source code."*

</div>

---

## 📄 License

```
MIT License

Copyright (c) 2025 CipherNest / Shivasairaj

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

---

<div align="center">

**CipherNest** — Security research, stripped bare.

*If this helped you build a better detector, it did its job.*

</div>
