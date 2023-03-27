@echo off

call %~dp0uwc_group_bot\venv_uwc_bot\Scripts\activate

cd %~dp0uwc_group_bot

set TOKEN=6286601698:AAFyd7gUZ2uGTK3GM3QESYXn5rg3At388uw

python bot_uwc_main.py

pause