import subprocess
from nicegui import ui

BOT_COMMAND = "python3 nanobot.py"  # Change this to your main CLI command

def run_bot_action(action: str):
    """Executes a CLI command and updates the web terminal."""
    try:
         Runs: python3 nanobot.py [action]
        result = subprocess.check_output(f"{BOT_COMMAND} {action}", shell=True, stderr=subprocess.STDOUT)
        output_log.append(f"<b>[Bot]:</b> {result.decode('utf-8')}")
    except subprocess.CalledProcessError as e:
        output_log.append(f"<span style='color:red'><b>[Error]:</b> {e.output.decode('utf-8')}</span>")

ui.query('body').style('background-color: #1a1a1a; color: white; font-family: sans-serif;')

with ui.column().classes('w-full items-center p-8'):
    ui.label('🐈 Nanobot Control Center').classes('text-4xl font-bold mb-4')
    
    with ui.row().classes('gap-4 mb-8'):
        ui.button('Start Agent', on_click=lambda: run_bot_action('agent')).props('color=green shadow')
        ui.button('Onboard', on_click=lambda: run_bot_action('onboard')).props('color=blue outline')
        ui.button('Clear History', on_click=lambda: run_bot_action('--clear')).props('color=red outline')

    ui.label('Live Output').classes('text-xl font-semibold self-start')
    output_log = ui.log(max_lines=20).classes('w-full h-64 bg-black text-green-400 p-4 border border-gray-700 rounded-lg font-mono')

    with ui.row().classes('w-full items-center mt-4'):
        cmd_input = ui.input(placeholder='Type custom command...').classes('flex-grow bg-gray-800 rounded p-2')
        ui.button('Send', on_click=lambda: [run_bot_action(cmd_input.value), setattr(cmd_input, 'value', '')])

ui.run(title='Nanobot WebUI', port=8080, dark=True)

