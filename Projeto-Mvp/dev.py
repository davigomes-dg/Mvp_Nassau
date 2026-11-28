"""Inicia o front-end e as APIs locais do Notaê em um único terminal."""
from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"
SERVICES = [
    ("Flask + SQLite", [sys.executable, "-m", "backend.app"]),
    (
        "FastAPI de cursos",
        [
            sys.executable,
            "-m",
            "uvicorn",
            "api_uninassau_aracaju:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
    ),
    (
        "Front-end",
        [
            sys.executable,
            "-m",
            "http.server",
            "5500",
            "--bind",
            "127.0.0.1",
            "--directory",
            str(FRONTEND),
        ],
    ),
]


def forward_output(name: str, stream, messages: queue.Queue) -> None:
    try:
        for line in iter(stream.readline, ""):
            messages.put((name, line.rstrip()))
    finally:
        stream.close()


def stop_processes(processes) -> None:
    for _name, process in processes:
        if process.poll() is None:
            try:
                process.terminate()
            except OSError:
                pass

    for _name, process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except OSError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass


def main() -> int:
    messages: queue.Queue = queue.Queue()
    processes = []
    readers = []
    environment = os.environ.copy()
    environment["PYTHONUNBUFFERED"] = "1"

    try:
        for name, command in SERVICES:
            process = subprocess.Popen(
                command,
                cwd=ROOT,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
            processes.append((name, process))
            reader = threading.Thread(
                target=forward_output,
                args=(name, process.stdout, messages),
                daemon=True,
            )
            reader.start()
            readers.append(reader)

        print("Notaê iniciado. Abra http://127.0.0.1:5500")
        print("Flask/SQLite: http://127.0.0.1:5000")
        print("FastAPI:      http://127.0.0.1:8000")
        print("Pressione Ctrl+C para encerrar os três serviços.\n")

        while True:
            try:
                name, line = messages.get(timeout=0.2)
                if line:
                    print("[" + name + "] " + line)
            except queue.Empty:
                pass

            for name, process in processes:
                return_code = process.poll()
                if return_code is not None:
                    raise RuntimeError(
                        name + " encerrou inesperadamente (código "
                        + str(return_code)
                        + ")."
                    )
    except KeyboardInterrupt:
        print("\nEncerrando os serviços…")
        return 0
    except (OSError, RuntimeError) as error:
        print("\nNão foi possível manter todos os serviços ativos: " + str(error))
        return 1
    finally:
        stop_processes(processes)
        for reader in readers:
            reader.join(timeout=1)

    return 0


if __name__ == "__main__":
    sys.exit(main())
