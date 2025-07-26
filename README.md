# preemie-weight
Little tool to track and plot weight development of preemies, compared to the Fenton percentile curves for premature babies.

## Installation

To install the preemie-weight tool, first clone the repository:

```bash
git clone https://github.com/your-repo/preemie-weight.git
cd preemie-weight
```

Now, install the required dependencies.

### Using Python Virtual Environment

1. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   ```

2. **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

### Using System Package Manager

Alternatively, you can install the required packages using your system's package manager. For example, on Ubuntu:

```bash
sudo apt-get update
sudo apt-get install python3-matplotlib
```

Make sure to activate the virtual environment if you choose the first method before running the script.

## Usage

To use the tool, run the `add_weight.py` script to add weight data and `plot_weight.py` to generate plots.

### Adding Weight Data

Run the following command to add weight data:

```bash
python add_weight.py --file FILE_NAME DATE WEIGHT
```

Replace `DATE` with the date of the weight measurement and `WEIGHT` with the weight in kilograms. If these arguments are not provided, the script will ask for the values interactively.
Optionally, specify `FILE_NAME` for a different filename than default (`weight.csv`). The files are stored under `data/`.

### Plotting Weight Data

Run the following command to plot weight data:

```bash
python plot_weight.py --due-date DUE_DATE
```

Replace `DUE_DATE` with the due date of the baby in YYYY-MM-DD format.
