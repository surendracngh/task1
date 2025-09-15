#!/usr/bin/env python3
"""
Safe-ish controlled stress / benchmark script for local testing.

WARNING:
- Use only on machines you OWN or have permission to test.
- Start with short durations (e.g., --duration 10) to observe behavior.
- Monitoring hardware temps and fan speeds is your responsibility.
- Do NOT use defaults to intentionally damage hardware.

What this script does:
- CPU: spawns N worker processes performing heavy numeric work (matrix multiplications)
  in a tight loop for a fixed duration.
- GPU (optional): if PyTorch with CUDA is available, runs large matrix multiplies on GPU.
- Reports simple CPU% and RAM usage with psutil (if installed).
- Stops after the given duration or on Ctrl+C.

Install required libraries if you want full features:
  pip install numpy psutil torch   # torch only if you want GPU testing (and have CUDA)
"""

import argparse
import multiprocessing as mp
import os
import signal
import sys
import time
from datetime import datetime, timedelta

# Optional imports
try:
    import numpy as np
except Exception:
    print("This script requires numpy. Install with: pip install numpy")
    sys.exit(1)

try:
    import psutil
except Exception:
    psutil = None  # we'll still run, but monitoring will be limited

# Try import torch for GPU test
try:
    import torch
    _HAS_TORCH = True
except Exception:
    torch = None
    _HAS_TORCH = False

# -- Safety defaults --
DEFAULT_DURATION = 30   # seconds
DEFAULT_CPU_WORKERS = max(1, mp.cpu_count() - 1)  # leave one core free by default
DEFAULT_MATRIX_SIZE = 800  # matrix multiplier size for work (tweak as needed)
DEFAULT_GPU_MATRIX_SIZE = 4096  # larger for GPU if available
DEFAULT_MONITOR_INTERVAL = 2.0  # seconds


def cpu_worker_loop(matrix_size: int, stop_time: float, worker_id: int):
    """
    CPU-heavy worker: repeatedly multiply random matrices inside a loop
    until stop_time (timestamp).
    Keep allocations re-used to avoid noisy GC overhead.
    """
    # Try to make arrays on float32 to be faster and reduce memory pressure
    a = np.random.rand(matrix_size, matrix_size).astype(np.float32)
    b = np.random.rand(matrix_size, matrix_size).astype(np.float32)
    # Warmup multiply once
    c = a @ b
    iter_count = 0
    try:
        while time.time() < stop_time:
            # Do a few multiplications per loop to reduce Python overhead
            c = a @ b
            # small in-place shuffle to change data a bit to avoid caching optimizations
            a += (np.roll(a, 1, axis=0) - 0.5) * 0.000001
            iter_count += 1
    except Exception as e:
        # If any numerical or memory error occurs, print and exit worker
        print(f"[CPU worker {worker_id}] Exception: {e}")
    finally:
        # Print final count for this worker
        print(f"[CPU worker {worker_id}] finished, iterations: {iter_count}")


def gpu_worker_loop(matrix_size: int, stop_time: float, device_index: int, worker_id: int):
    """
    GPU-heavy worker using PyTorch (CUDA).
    Repeats large matrix multiplications on the specified CUDA device.
    """
    if not _HAS_TORCH:
        print(f"[GPU worker {worker_id}] PyTorch not available; skipping GPU work.")
        return

    try:
        dev = torch.device(f"cuda:{device_index}")
        # Pre-allocate tensors on GPU
        a = torch.randn((matrix_size, matrix_size), device=dev, dtype=torch.float32)
        b = torch.randn((matrix_size, matrix_size), device=dev, dtype=torch.float32)
        # Warmup
        c = a @ b
        torch.cuda.synchronize(dev)
        iter_count = 0
        while time.time() < stop_time:
            c = a @ b
            # occasionally modify a a bit
            a.add_(0.000001)
            iter_count += 1
            # Make sure operations complete periodically
            if iter_count % 10 == 0:
                torch.cuda.synchronize(dev)
    except Exception as e:
        print(f"[GPU worker {worker_id}] Exception: {e}")
    finally:
        print(f"[GPU worker {worker_id}] finished, iterations: {iter_count if 'iter_count' in locals() else 0}")


def monitor_loop(duration: float, interval: float):
    """
    Basic monitor loop printing CPU% and memory usage periodically.
    Uses psutil if available.
    """
    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            now = datetime.now().strftime("%H:%M:%S")
            if psutil:
                cpu_pct = psutil.cpu_percent(interval=None)
                mem = psutil.virtual_memory()
                load = os.getloadavg() if hasattr(os, "getloadavg") else ("N/A",) * 3
                line = (
                    f"[{now}] CPU%: {cpu_pct:.1f} | Mem: {mem.percent:.1f}% "
                    f"({mem.used // (1024**2)}MB/{mem.total // (1024**2)}MB) | "
                    f"load1:{load[0]:.2f}"
                )
            else:
                line = f"[{now}] psutil not available - no system metrics."
            print(line)
            # sleep but exit early if time's up
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[Monitor] Stopping monitoring (Ctrl+C).")


def parse_args():
    p = argparse.ArgumentParser(description="Controlled CPU/GPU workload runner (safe defaults).")
    p.add_argument("--duration", "-d", type=int, default=DEFAULT_DURATION,
                   help=f"Total run duration in seconds (default: {DEFAULT_DURATION})")
    p.add_argument("--cpu-workers", type=int, default=DEFAULT_CPU_WORKERS,
                   help=f"Number of CPU worker processes to spawn (default: {DEFAULT_CPU_WORKERS})")
    p.add_argument("--matrix-size", type=int, default=DEFAULT_MATRIX_SIZE,
                   help=f"Matrix size (N) for CPU worker matrices NxN (default: {DEFAULT_MATRIX_SIZE})")
    p.add_argument("--gpu", action="store_true", help="Enable GPU workload (requires PyTorch with CUDA)")
    p.add_argument("--gpu-matrix-size", type=int, default=DEFAULT_GPU_MATRIX_SIZE,
                   help=f"Matrix size for GPU workload (default: {DEFAULT_GPU_MATRIX_SIZE})")
    p.add_argument("--monitor-interval", type=float, default=DEFAULT_MONITOR_INTERVAL,
                   help=f"Seconds between monitor prints (default: {DEFAULT_MONITOR_INTERVAL})")
    return p.parse_args()


def main():
    args = parse_args()

    # Safety checks / info
    print("=== Controlled Workload Runner ===")
    print("READ THIS: Use only on systems you own. Start with small durations.")
    print(f"Start time: {datetime.now().isoformat()}")
    print(f"Duration: {args.duration}s, CPU workers: {args.cpu_workers}, CPU matrix: {args.matrix_size}")
    if args.gpu:
        if not _HAS_TORCH:
            print("GPU flag provided but PyTorch not available. GPU workload will be skipped.")
            args.gpu = False
        else:
            if not torch.cuda.is_available():
                print("PyTorch found but no CUDA device available. GPU workload will be skipped.")
                args.gpu = False
            else:
                print(f"GPU matrix size: {args.gpu_matrix_size}, CUDA devices: {torch.cuda.device_count()}")

    # Compute stop time
    stop_time = time.time() + args.duration

    # Set OMP_NUM_THREADS and related env vars if desired (optional).
    # NOTE: many BLAS libs (MKL/OpenBLAS) will use multiple threads; if you want each worker to
    # use 1 thread, set OMP_NUM_THREADS=1 before launching. We leave defaults to let BLAS decide.
    # os.environ["OMP_NUM_THREADS"] = "1"

    # Start monitor in a separate process/thread so it prints while workers run
    monitor_proc = mp.Process(target=monitor_loop, args=(args.duration, args.monitor_interval), daemon=True)
    monitor_proc.start()

    # Launch CPU workers
    cpu_procs = []
    for i in range(args.cpu_workers):
        p = mp.Process(target=cpu_worker_loop, args=(args.matrix_size, stop_time, i), daemon=False)
        p.start()
        cpu_procs.append(p)
        time.sleep(0.1)  # small stagger to avoid simultaneous heavy startup

    # Optionally launch GPU workers: we'll create one GPU worker per GPU device (or 1 if single)
    gpu_procs = []
    if args.gpu:
        cuda_count = torch.cuda.device_count()
        # Do not spawn more GPU workers than devices
        for idx in range(cuda_count):
            p = mp.Process(target=gpu_worker_loop,
                           args=(args.gpu_matrix_size, stop_time, idx, idx),
                           daemon=False)
            p.start()
            gpu_procs.append(p)
            time.sleep(0.1)

    # Wait until stop_time or until KeyboardInterrupt
    try:
        remaining = stop_time - time.time()
        while remaining > 0:
            time.sleep(min(1.0, remaining))
            remaining = stop_time - time.time()
    except KeyboardInterrupt:
        print("\n[Main] KeyboardInterrupt received. Attempting graceful shutdown...")
    finally:
        # Ask all child procs to terminate
        for p in cpu_procs + gpu_procs:
            if p.is_alive():
                p.terminate()
        # Give them a moment, then join
        for p in cpu_procs + gpu_procs:
            p.join(timeout=2.0)

        if monitor_proc.is_alive():
            monitor_proc.terminate()
            monitor_proc.join(timeout=1.0)

        print("All workers stopped. End time:", datetime.now().isoformat())
        print("Done.")

if __name__ == "__main__":
    main()
