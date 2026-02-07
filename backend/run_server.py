"""Run the FastAPI server. Uses the same Python that runs this script."""
import sys
import subprocess

if __name__ == "__main__":
    subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8001",
            "--reload",
        ],
        check=True,
    )
