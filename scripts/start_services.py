import subprocess
import sys
from pathlib import Path
from loguru import logger
import time
import signal
import os
import psutil
import requests
import select
from rich.console import Console
from rich.table import Table
from scripts.verify_server import verify_server
from timeline.logs.config import setup_logging
import threading

console = Console()

class ServiceManager:
    def __init__(self):
        self.processes = []
        setup_logging("services")
        
    def setup_logging(self):
        """Configure loguru logging"""
        logger.remove()  # Remove default handler
        logger.add(
            "timeline/logs/services.log",
            rotation="1 day",
            retention="7 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="INFO"
        )
        logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>")

    def check_port(self, port):
        """Check if port is available"""
        try:
            requests.get(f"http://localhost:{port}")
            return False
        except requests.ConnectionError:
            return True

    def start_process(self, name, command):
        """Start a process with error handling"""
        try:
            logger.debug(f"Starting {name} with command: {command}")
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1  # Line buffered
            )
            
            # Start output monitoring threads
            def monitor_output(pipe, prefix):
                for line in pipe:
                    logger.debug(f"{prefix} | {line.strip()}")
                    
            threading.Thread(target=monitor_output, 
                            args=(process.stdout, f"{name} OUT"),
                            daemon=True).start()
            threading.Thread(target=monitor_output, 
                            args=(process.stderr, f"{name} ERR"),
                            daemon=True).start()
            
            self.processes.append({"name": name, "process": process})
            logger.success(f"Started {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start {name}: {str(e)}")
            return False

    def check_health(self):
        """Check health of all processes"""
        table = Table(title="Service Status")
        table.add_column("Service", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("PID", style="magenta")
        table.add_column("Memory", style="yellow")
        
        for service in self.processes:
            process = service["process"]
            if process.poll() is None:  # Process is running
                try:
                    proc = psutil.Process(process.pid)
                    memory = f"{proc.memory_info().rss / 1024 / 1024:.1f} MB"
                    status = "🟢 Running"
                except psutil.NoSuchProcess:
                    memory = "N/A"
                    status = "🔴 Dead"
            else:
                memory = "N/A"
                status = "🔴 Stopped"
            
            table.add_row(
                service["name"],
                status,
                str(process.pid),
                memory
            )
        
        console.print(table)

    def cleanup(self):
        """Clean up all processes"""
        logger.info("Shutting down services...")
        for service in self.processes:
            try:
                process = service["process"]
                if process.poll() is None:  # Process is still running
                    logger.info(f"Stopping {service['name']}...")
                    process.terminate()
                    process.wait(timeout=5)
            except Exception as e:
                logger.error(f"Error stopping {service['name']}: {str(e)}")
        logger.success("All services stopped")

def start_services():
    """Start all services in the correct order"""
    manager = ServiceManager()
    
    try:
        # Check ports
        if not manager.check_port(8010):
            logger.error("Port 8010 is already in use!")
            return
            
        # Start timeline watcher
        logger.info("Starting timeline watcher...")
        if not manager.start_process("Timeline Watcher", ["timeline", "watch"]):
            raise Exception("Failed to start timeline watcher")
            
        # Start dev docs server
        logger.info("Starting dev docs server...")
        if not manager.start_process("Dev Docs Server", ["dev-docs"]):
            raise Exception("Failed to start dev docs server")
            
        if not verify_server():
            raise Exception("Dev docs server failed verification")
            
        logger.success("All services started!")
        logger.info("Access documentation at: http://localhost:8010/dev")
        logger.info("Access timeline at: http://localhost:8010/dev/timeline")
        logger.info("Press Ctrl+C to stop all services")
        logger.info("Press 'h' to check service health")
        
        # Monitor processes
        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if line.strip() == 'h':
                    manager.check_health()
            
            # Check process health
            for service in manager.processes:
                if service["process"].poll() is not None:
                    logger.error(f"{service['name']} died unexpectedly!")
                    raise Exception(f"{service['name']} died")
                    
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Error in services: {str(e)}")
    finally:
        manager.cleanup()

if __name__ == "__main__":
    start_services() 