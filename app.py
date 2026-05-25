import streamlit as st
import subprocess
import platform
import psutil
from datetime import datetime
import os

st.set_page_config(page_title='Zyos Support Agent', layout='wide')

os.makedirs('reports', exist_ok=True)

APPROVED_ACTIONS = {
    'Restart Camera Service': 'Restart-Service FrameServer',
    'Kill Teams': 'taskkill /F /IM Teams.exe',
    'Kill Zoom': 'taskkill /F /IM Zoom.exe',
    'Get Camera Devices': "Get-PnpDevice | Where-Object {$_.Class -match 'Camera|Image|Media'}",
    'Get Camera Processes': 'Get-Process Teams,Zoom,obs64,chrome,msedge -ErrorAction SilentlyContinue',
    'Get Event Logs': "Get-WinEvent -LogName System -MaxEvents 50 | Where-Object {$_.Message -match 'camera|usb|video|webcam'}"
}


def run_powershell(command):
    result = subprocess.run(
        ['powershell', '-Command', command],
        capture_output=True,
        text=True
    )

    return result.stdout if result.stdout else result.stderr


st.title('Zyos Support Agent')
st.caption('AI-Assisted Windows Diagnostics & Remediation')

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader('Interactive Diagnostics')

    issue = st.text_area(
        'Describe the issue',
        placeholder='Example: My Jabra camera is not working in Teams'
    )

    if st.button('Analyze'):
        st.success('Initial analysis complete')

        st.write('### Recommended Actions')

        for action_name, command in APPROVED_ACTIONS.items():

            if st.button(action_name):
                output = run_powershell(command)

                st.code(output)

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

                with open(f'reports/{timestamp}.txt', 'w', encoding='utf-8') as f:
                    f.write(output)

with col2:
    st.subheader('System Information')

    st.metric('OS', platform.system())
    st.metric('Hostname', platform.node())
    st.metric('CPU Count', psutil.cpu_count())
    st.metric('RAM Used %', psutil.virtual_memory().percent)

st.divider()

st.markdown('### Next Phase')

st.markdown('''
- Microsoft Graph integration
- OneDrive diagnostics
- Teams remediation
- Intune support
- Remote support integration
- Multi-tenant customer deployment
- Approval policies
- Fleet dashboard
''')
