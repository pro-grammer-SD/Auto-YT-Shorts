import time
import ast
from functools import wraps
from rich.console import Console

console = Console()

def retry_on_quota_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                msg = str(e)
                if "RESOURCE_EXHAUSTED" in msg:
                    try:
                        err_obj = ast.literal_eval(msg)
                        delay = 0
                        for d in err_obj.get("error", {}).get("details", []):
                            if d.get("@type") == "type.googleapis.com/google.rpc.RetryInfo":
                                delay = int(d.get("retryDelay", "0s").replace("s", ""))
                        if delay:
                            console.print(f"[yellow]⚠️ Quota hit. Retrying in {delay}s...[/yellow]")
                            time.sleep(delay)
                            continue
                    except Exception as parse_err:
                        console.print(f"[red]❌ Quota parse error:[/red] {parse_err}")
                raise
    return wrapper
