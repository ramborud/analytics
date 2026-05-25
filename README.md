# Zyos Support Agent MVP

Local-first Windows support agent prototype for diagnostics, approved remediation, and future Microsoft 365 / remote support integration.

## Current Scope

This MVP is intentionally simple and safe:

- Runs locally on Windows
- Provides a Streamlit UI
- Runs approved PowerShell diagnostic actions
- Supports camera troubleshooting workflows
- Logs remediation output to `reports/`
- Includes a Windows bootstrap installer

## First Use Case

Camera troubleshooting, especially Jabra PanaCast / Teams / Zoom issues.

The agent can check:

- Camera devices in Device Manager
- Camera-related running processes
- Windows Camera Frame Server status
- Recent camera / USB / video system event logs
- Basic system health

Approved remediation actions include:

- Restart Windows Camera Frame Server
- Kill Teams
- Kill Zoom

## Local Install

Open PowerShell as Administrator and run:

```powershell
git clone https://github.com/ramborud/analytics.git C:\Zyos\AgentLab\zyos-support-agent-v1
cd C:\Zyos\AgentLab\zyos-support-agent-v1
.\scripts\install.ps1
```

Then open:

```text
http://localhost:8501
```

## Manual Run

```powershell
cd C:\Zyos\AgentLab\zyos-support-agent-v1
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

## Security Model

This prototype does not allow arbitrary command execution from the UI.

The app only runs commands that exist in the approved action registry inside `app.py`.

Before customer deployment, the platform needs:

- Authentication
- Signed installer
- Code signing
- Tenant isolation
- Encrypted secrets
- Centralized audit logging
- Rollback support
- Policy-based remediation
- Microsoft Graph app registration
- Remote support architecture

## Roadmap

### Phase 1

- Local camera diagnostics
- OneDrive diagnostics
- Teams diagnostics
- Outlook / Office auth diagnostics
- PowerShell module separation

### Phase 2

- Microsoft Graph integration
- Entra ID sign-in diagnostics
- Intune device status
- OneDrive sync health
- Teams device troubleshooting

### Phase 3

- Zyos support portal
- Remote support integration
- Fleet deployment
- Customer tenant separation
- Agent as a Service packaging
