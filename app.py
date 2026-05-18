import sys
import io
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CodePayload(BaseModel):
    script_code: str

@app.post("/run")
def run_dynamic_script(payload: CodePayload):
    # Redirect system output to capture print statements
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        # Execute the raw string code sent by the VM
        exec(payload.script_code, {"__builtins__": __builtins__})
        error_msg = None
    except Exception as e:
        print(f"Execution Error: {str(e)}")
        error_msg = str(e)
    finally:
        # Restore normal system output
        sys.stdout = old_stdout
        
    return {
        "success": error_msg is None,
        "output": redirected_output.getvalue()
    }
