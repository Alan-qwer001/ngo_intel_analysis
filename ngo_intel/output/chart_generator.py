import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class ChartGenerator:
    def __init__(self, output_dir=""):
        self.output_dir = output_dir or "chart_assets"
        os.makedirs(self.output_dir, exist_ok=True)

    def chart_trend(self, years, totals, fn="chart_trend.png"):
        fig, ax = plt.subplots(figsize=(8, 4.5))
        bars = ax.bar(years, totals, color=["#4A90D9", "#2E6DA4", "#D9534F"][:len(years)], width=0.5)
        for b, v in zip(bars, totals):
            ax.text(b.get_x()+b.get_width()/2., b.get_height()+15, v, ha="center", va="bottom")
        ax.set_title("Total Expenditure Trend")
        plt.tight_layout()
        fig.savefig(os.path.join(self.output_dir, fn), dpi=200, bbox_inches="tight")
        plt.close()
        return fn

    def chart_radar(self, categories, scores, fn="chart_radar.png"):
        import numpy as np
        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
        N = len(categories)
        angles = [n/float(N)*2*np.pi for n in range(N)] + [0]
        sp = scores + scores[:1]
        ax.plot(angles, sp, "o-", linewidth=2, color="#2980B9", markersize=8)
        ax.fill(angles, sp, alpha=0.25, color="#3498DB")
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=11)
        ax.set_ylim(0, 10)
        ax.set_title("7S Assessment", pad=20)
        plt.tight_layout()
        fig.savefig(os.path.join(self.output_dir, fn), dpi=200, bbox_inches="tight")
        plt.close()
        return fn