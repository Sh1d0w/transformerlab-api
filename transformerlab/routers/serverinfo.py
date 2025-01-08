import atexit
import json
import os
import platform
import sys
import subprocess


# Could also use https://github.com/gpuopenanalytics/pynvml but this is simpler
import psutil
import torch
from fastapi import APIRouter
from pynvml import (
    nvmlDeviceGetCount,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetName,
    nvmlDeviceGetUtilizationRates,
    nvmlInit,
    nvmlShutdown,
)

pyTorch_version = torch.__version__
print(f"🔥 PyTorch version: {pyTorch_version}")

# Check for version of flash_attn:
flash_attn_version = ""
try:
    from flash_attn import __version__ as flash_attn_version
    print(f"⚡️ Flash Attention is installed, version {flash_attn_version}")
except ImportError:
    flash_attn_version = "n/a"
    print("🟡 Flash Attention is not installed. If you are running on GPU, install to accelerate inference and training. https://github.com/Dao-AILab/flash-attention")


# Read in static system info
system_info = {
    "cpu": platform.machine(),
    "name": platform.node(),
    "platform": platform.platform(),
    "python_version": platform.python_version(),
    "os": platform.system(),
    "os_alias": platform.system_alias(
        platform.system(), platform.release(), platform.version()
    ),
    "gpu": [],
    "gpu_memory": "",
    "device": "cpu",
    "cuda_version": "n/a",
    "conda_environment": os.environ.get("CONDA_DEFAULT_ENV", "n/a"),
    "conda_prefix": os.environ.get("CONDA_PREFIX", "n/a"),
    "flash_attn_version": flash_attn_version,
    "pytorch_version": torch.__version__,
}

# Determine which device to use (cuda/mps/cpu)
if torch.cuda.is_available():
    system_info["device"] = "cuda"

    # we have a GPU so initialize the nvidia python bindings
    nvmlInit()

    # get CUDA version:
    system_info["cuda_version"] = torch.version.cuda

    print(f"🏄 PyTorch is using CUDA, version {torch.version.cuda}")

elif torch.backends.mps.is_available():
    system_info["device"] = "mps"
    print(f"🏄 PyTorch is using MPS for Apple Metal acceleration")

router = APIRouter(prefix="/server", tags=["serverinfo"])


@router.get("/info")
async def get_computer_information():
    # start with our static system information and add current performance details
    r = system_info
    r.update(
        {
            "cpu_percent": psutil.cpu_percent(),
            "cpu_count": psutil.cpu_count(),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage("/")._asdict(),
            "gpu_memory": "",
        }
    )

    g = []

    try:
        deviceCount = nvmlDeviceGetCount()
        for i in range(deviceCount):
            info = {}

            handle = nvmlDeviceGetHandleByIndex(i)

            # Certain versions of the NVML library on WSL return a byte string,
            # and this creates a utf error. This is a workaround:
            device_name = nvmlDeviceGetName(handle)
            if (device_name.hasattr('decode')):
                device_name = device_name.decode()

            info["name"] = device_name

            memory = nvmlDeviceGetMemoryInfo(handle)
            info["total_memory"] = memory.total
            info["free_memory"] = memory.free
            info["used_memory"] = memory.used

            u = nvmlDeviceGetUtilizationRates(handle)
            info["utilization"] = u.gpu

            # info["temp"] = nvmlDeviceGetTemperature(handle)
            g.append(info)
    except:  # noqa: E722 (TODO: what are the exceptions to chat here?)
        g.append(
            {
                "name": "cpu",
                "total_memory": "n/a",
                "free_memory": "n/a",
                "used_memory": "n/a",
                "utilization": "n/a",
            }
        )

    r["gpu"] = g

    return r


@router.get("/python_libraries")
async def get_python_library_versions():
    # get the list of installed python packages
    packages = subprocess.check_output(
        sys.executable + " -m pip list --format=json", shell=True)

    packages = packages.decode("utf-8")
    packages = json.loads(packages)
    return packages


@router.get("/pytorch_collect_env")
async def get_pytorch_collect_env():
    # run python -m torch.utils.collect_env and return the output
    output = subprocess.check_output(
        sys.executable + " -m torch.utils.collect_env", shell=True
    )
    return output.decode("utf-8")


def cleanup_at_exit():
    if torch.cuda.is_available():
        nvmlShutdown()


atexit.register(cleanup_at_exit)
