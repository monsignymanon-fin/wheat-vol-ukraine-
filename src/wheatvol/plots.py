import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def save_line(df: pd.DataFrame, x: str, ys: list[str], out: Path, title: str):
    fig, ax = plt.subplots()
    for col in ys:
        ax.plot(df[x], df[col], label=col)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
