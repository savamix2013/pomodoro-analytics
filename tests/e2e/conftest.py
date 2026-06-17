import os
import time
import subprocess
import httpx
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def api_server():
    # Set up environment variables to point to local database and cache (running in docker)
    env = os.environ.copy()
    env["DB_HOST"] = "127.0.0.1"
    env["CACHE_HOST"] = "127.0.0.1"
    
    server_port = "8005"
    server_url = f"http://127.0.0.1:{server_port}"
    
    # Start the FastAPI server using uvicorn in a background process
    log_file = open("uvicorn_e2e.log", "w")
    proc = subprocess.Popen(
        ["poetry", "run", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", server_port],
        env=env,
        stdout=log_file,
        stderr=log_file,
    )
    
    # Wait for the server to spin up and respond to /app/ping
    start_time = time.time()
    while True:
        try:
            response = httpx.get(f"{server_url}/app/ping", timeout=1.0)
            if response.status_code == 200:
                break
        except httpx.RequestError:
            pass
        
        if time.time() - start_time > 10.0:
            proc.terminate()
            log_file.close()
            raise RuntimeError(f"Failed to start FastAPI server on port {server_port}.")
        time.sleep(0.5)
        
    yield server_url
    
    # Clean up the process at the end of the test session
    proc.terminate()
    try:
        proc.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        proc.kill()
    log_file.close()

@pytest.fixture(scope="function")
def api_client(api_server):
    with sync_playwright() as p:
        request_context = p.request.new_context(base_url=api_server)
        yield request_context
        request_context.dispose()


@pytest.fixture(autouse=True)
def init_models():
    # Override root init_models to prevent async DB operations on E2E tests
    pass
