import os
import platform
import subprocess
from datetime import datetime

import psutil
import streamlit as st

st.set_page_config(page_title="Zyos Support Agent", layout="wide")

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

APPROVED_ACTIONS = {
    "Get Camera Devices": "Get-PnpDevice | Where-Object {$_.Class -match 'Camera|Image|Media'} | Format-Table -AutoSize",
    "Get Camera Processes": "Get-Process Teams,Zoom,obs64,chrome,msedge,firefox,Discord -ErrorAction SilentlyContinue | Select-Object ProcessName,Id,CPU,StartTime | Format-Table -AutoSize",
    "Get FrameServer Status": "Get-Service FrameServer | Format-List *",
    "Get Recent Camera Event Logs": "Get-WinEvent -LogName System -MaxEvents 150 | Where-Object {$_.Message -match 'camera|usb|video|webcam|FrameServer|Jabra'} | Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message | Format-List",
    "Restart Camera Service": "Restart-Service FrameServer -Force; Get-Service FrameServer",
    "Kill Teams": "taskkill /F /IM Teams.exe",
    "Kill Zoom": "taskkill /F /IM Zoom.exe",
}

DIAGNOSTIC_ACTIONS = [
    "Get Camera Devices",
    "Get Camera Processes",
    "Get FrameServer Status",
    "Get Recent Camera Event Logs",
]

REMEDIATION_ACTIONS = [
    "Restart Camera Service",
    "Kill Teams",
    "Kill Zoom",
]


def run_powershell(command: str) -> dict:
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            capture_output=True,
            text=True,
            timeout=90,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }
    except Exception as exc:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(exc),
            "returncode": -1,
        }


def save_report(name: str, content: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.lower().replace(" ", "_").replace("/", "_")
    path = os.path.join(REPORT_DIR, f"{timestamp}_{safe_name}.txt")
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    return path


def display_result(action_name: str, result: dict):
    output = result["stdout"] or result["stderr"] or "No output returned."
    saved_path = save_report(action_name, output)

    if result["success"]:
        st.success(f"{action_name} completed")
    else:
        st.error(f"{action_name} failed. Return code: {result['returncode']}")

    st.code(output, language="text")
    st.caption(f"Saved report: {saved_path}")


def run_full_camera_diagnostic():
    combined = []
    for action_name in DIAGNOSTIC_ACTIONS:
        command = APPROVED_ACTIONS[action_name]
        result = run_powershell(command)
        output = result["stdout"] or result["stderr"] or "No output returned."
        combined.append(f"\n\n==============================\n{action_name}\n==============================\n{output}")
    full_report = "".join(combined)
    report_path = save_report("full_camera_diagnostic", full_report)
    return full_report, report_path


st.title("Zyos Support Agent")
st.caption("Local Windows diagnostics and approved remediation prototype")

left, right = st.columns([2, 1])

with left:
    st.subheader("Camera Troubleshooting")

    issue = st.text_area(
        "Describe the issue",
        value="My Jabra PanaCast camera is not working",
    )

    if st.button("Run Full Camera Diagnostic", type="primary"):
        with st.spinner("Running local diagnostics..."):
            full_report, report_path = run_full_camera_diagnostic()
        st.success("Full diagnostic complete")
        st.code(full_report, language="text")
        st.caption(f"Saved report: {report_path}")

    st.markdown("### Individual Diagnostics")
    for action_name in DIAGNOSTIC_ACTIONS:
        if st.button(action_name, key=f"diag_{action_name}"):
            with st.spinner(f"Running {action_name}..."):
                result = run_powershell(APPROVED_ACTIONS[action_name])
            display_result(action_name, result)

    st.markdown("### Approved Remediation")
    st.warning("These actions can close apps or restart Windows services. Use only after reviewing diagnostics.")
    for action_name in REMEDIATION_ACTIONS:
        if st.button(action_name, key=f"fix_{action_name}"):
            with st.spinner(f"Running {action_name}..."):
                result = run_powershell(APPROVED_ACTIONS[action_name])
            display_result(action_name, result)

with right:
    st.subheader("System Information")
    st.metric("OS", platform.system())
    st.metric("Hostname", platform.node())
    st.metric("CPU Count", psutil.cpu_count())
    st.metric("RAM Used %", f"{psutil.virtual_memory().percent}%")

    st.subheader("How to use")
    st.markdown(
        """
1. Click **Run Full Camera Diagnostic**.
2. Review the output.
3. If Teams or Zoom is holding the camera, use the approved remediation buttons.
4. Upload or paste the saved report here if the issue is not obvious.
        """
    )

st.divider()
st.markdown(
    """
### Next Phase
- Microsoft Graph integration
- Office 365 diagnostics
- Teams remediation workflows
- OneDrive sync health
- Intune device status
- Remote support integration
    """
)
