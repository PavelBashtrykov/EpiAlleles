# Installation

## Clone Repository

```bash
git clone <repository-url>
cd EpiAlleles
```

## System Requirements

- Python 3.10.4
- pip or conda

## Install Python 3.10.4

### Using apt (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

### Using Homebrew (macOS)
```bash
brew install python@3.10
```

## Install Dependencies

### Option 1: pip
```bash
pip install -r requirements.txt
```

### Option 2: venv + pip
```bash
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Option 3: conda
```bash
conda create -n allelicmeth python=3.10.4
conda activate allelicmeth
pip install -r requirements.txt
```

## Verify Installation

```bash
python3.10 allelicMeth.py --help
python3.10 run_allelicMeth.py --help
```

## Requirements

- python==3.10.4
- matplotlib==3.5.1
- seaborn==0.11.2
- pandas==1.4.2
- numpy==1.22.3
