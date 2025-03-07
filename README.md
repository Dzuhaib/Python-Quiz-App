# Setting Up the Virtual Environment in VSCode

To ensure that the `google-generativeai` package is accessible in your script, follow these steps:

1. **Activate the Virtual Environment**:
   Make sure your virtual environment is activated. You can do this by running the following command in the terminal:
   ```
   .venv\Scripts\activate
   ```

2. **Select the Python Interpreter**:
   In VSCode, you need to select the Python interpreter that corresponds to your virtual environment:
   - Open the Command Palette (Ctrl + Shift + P).
   - Type and select "Python: Select Interpreter".
   - Choose the interpreter that points to your virtual environment (it should look something like `E:\Class Projects\Quiz web app\.venv\Scripts\python.exe`).

3. **Run the Script**:
   After selecting the correct interpreter, try running your script again. The `google.generativeai` module should now be accessible.

If you continue to experience issues, please ensure that the virtual environment is properly set up and that you are running the script from the terminal where the environment is activated.
