import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

conn = sqlite3.connect("ecommerce.db")

# ── Colour palette ──────────────────────────────────────────────
DARK_BG   = "#0d1117"
CARD_BG   = "#161b22"
ACCENT    = "#58a6ff"
GREEN     = "#3fb950"
PURPLE    = "#bc8cff"
ORANGE    = "#f0883e"
TEXT      = "#e6edf3"
SUBTEXT   = "#8b949e"
BORDER    = "#30363d"

BAR_COLORS = [ACCENT, GREEN, PURPLE, ORANGE, "#ff7b72"]

def style_ax(ax, title):
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, color=TEXT, fontsize=11, fontweight="bold", pad=10)
    ax.tick_params(colors=SUBTEXT, labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
    ax.xaxis.label.set_color(SUBTEXT)
    ax.yaxis.label.set_color(SUBTEXT)
    ax.grid(axis="y", color=BORDER, linewidth=0.5, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)

# ══════════════════════════════════════════════════════════════════
# SCREENSHOT 1 — Revenue by Month (line chart)
# ══════════════════════════════════════════════════════════════════
df1 = pd.read_sql_query("""
    SELECT strftime('%b %Y', o.order_date) AS month,
           strftime('%Y-%m', o.order_date) AS sort_key,
           ROUND(SUM(p.price * oi.quantity), 2) AS total_revenue,
           COUNT(DISTINCT o.order_id) AS total_orders
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'completed'
    GROUP BY sort_key ORDER BY sort_key
""", conn)

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)

x_idx = range(len(df1))
ax.fill_between(x_idx, df1["total_revenue"], alpha=0.15, color=ACCENT)
ax.plot(x_idx, df1["total_revenue"], color=ACCENT, linewidth=2.5, marker="o",
        markersize=7, markerfacecolor=DARK_BG, markeredgecolor=ACCENT, markeredgewidth=2)
ax.set_xticks(list(x_idx))
ax.set_xticklabels(df1["month"])

for i, (x, y) in enumerate(zip(x_idx, df1["total_revenue"])):
    ax.annotate(f"£{y:,.0f}", (x, y), textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=7.5, color=TEXT, fontweight="bold")

style_ax(ax, "📈  Total Revenue by Month — Completed Orders")
ax.set_xlabel("Month", fontsize=9)
ax.set_ylabel("Revenue (£)", fontsize=9)
plt.xticks(rotation=35, ha="right")
plt.tight_layout(pad=1.5)
plt.savefig("screenshots/01_revenue_by_month.png", dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.close()
print("✅ Screenshot 1 saved")

# ══════════════════════════════════════════════════════════════════
# SCREENSHOT 2 — Top 5 Products (horizontal bar)
# ══════════════════════════════════════════════════════════════════
df2 = pd.read_sql_query("""
    SELECT p.name AS product_name, p.category,
           SUM(oi.quantity) AS units_sold,
           ROUND(SUM(p.price * oi.quantity), 2) AS total_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY p.product_id ORDER BY total_revenue DESC LIMIT 5
""", conn)

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)

bars = ax.barh(df2["product_name"], df2["total_revenue"],
               color=BAR_COLORS, edgecolor=BORDER, linewidth=0.5, height=0.55)

for bar, val in zip(bars, df2["total_revenue"]):
    ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height()/2,
            f"£{val:,.0f}", va="center", ha="left", color=TEXT, fontsize=9, fontweight="bold")

style_ax(ax, "🏆  Top 5 Products by Revenue")
ax.set_xlabel("Total Revenue (£)", fontsize=9)
ax.invert_yaxis()
ax.set_xlim(0, df2["total_revenue"].max() * 1.2)
ax.tick_params(axis="y", colors=TEXT, labelsize=9)
plt.tight_layout(pad=1.5)
plt.savefig("screenshots/02_top_products.png", dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.close()
print("✅ Screenshot 2 saved")

# ══════════════════════════════════════════════════════════════════
# SCREENSHOT 3 — Customer Retention (donut chart)
# ══════════════════════════════════════════════════════════════════
df3 = pd.read_sql_query("""
    SELECT
        CASE WHEN order_count = 1 THEN 'One-time buyer'
             WHEN order_count BETWEEN 2 AND 3 THEN 'Returning buyer'
             ELSE 'Loyal buyer' END AS customer_segment,
        COUNT(*) AS number_of_customers
    FROM (
        SELECT customer_id, COUNT(order_id) AS order_count
        FROM orders WHERE status = 'completed' GROUP BY customer_id
    ) GROUP BY customer_segment ORDER BY number_of_customers DESC
""", conn)

fig, (ax_pie, ax_text) = plt.subplots(1, 2, figsize=(10, 5),
                                       gridspec_kw={"width_ratios": [1, 1]})
fig.patch.set_facecolor(DARK_BG)
ax_pie.set_facecolor(DARK_BG)
ax_text.set_facecolor(DARK_BG)

colors_pie = [ACCENT, GREEN, PURPLE]
wedges, texts, autotexts = ax_pie.pie(
    df3["number_of_customers"], labels=None, autopct="%1.0f%%",
    colors=colors_pie, startangle=90, pctdistance=0.75,
    wedgeprops={"edgecolor": DARK_BG, "linewidth": 3, "width": 0.55}
)
for at in autotexts:
    at.set_color(DARK_BG); at.set_fontsize(10); at.set_fontweight("bold")

ax_pie.set_title("🔄  Customer Retention Segments", color=TEXT, fontsize=11,
                 fontweight="bold", pad=14)

for i, (seg, count, color) in enumerate(zip(df3["customer_segment"],
                                             df3["number_of_customers"], colors_pie)):
    ax_text.text(0.05, 0.75 - i*0.25, f"● {seg}", color=color,
                 fontsize=11, fontweight="bold", transform=ax_text.transAxes)
    ax_text.text(0.05, 0.75 - i*0.25 - 0.10, f"  {count} customers",
                 color=SUBTEXT, fontsize=9, transform=ax_text.transAxes)

ax_text.axis("off")
ax_text.set_title("Key Insight", color=TEXT, fontsize=11, fontweight="bold", pad=14)

insight = "Returning + Loyal buyers\nrepresent your highest\nlifetime value customers."
ax_text.text(0.05, 0.12, insight, color=SUBTEXT, fontsize=9,
             transform=ax_text.transAxes, linespacing=1.6)

plt.tight_layout(pad=1.5)
plt.savefig("screenshots/03_customer_retention.png", dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.close()
print("✅ Screenshot 3 saved")

# ══════════════════════════════════════════════════════════════════
# SCREENSHOT 4 — Revenue by Category (bar chart)
# ══════════════════════════════════════════════════════════════════
df4 = pd.read_sql_query("""
    SELECT p.category,
           ROUND(SUM(p.price * oi.quantity), 2) AS total_revenue,
           SUM(oi.quantity) AS units_sold
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY p.category ORDER BY total_revenue DESC
""", conn)

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)

bars = ax.bar(df4["category"], df4["total_revenue"],
              color=BAR_COLORS[:len(df4)], edgecolor=BORDER, linewidth=0.5, width=0.5)

for bar, val in zip(bars, df4["total_revenue"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
            f"£{val:,.0f}", ha="center", va="bottom", color=TEXT,
            fontsize=9, fontweight="bold")

style_ax(ax, "📦  Revenue by Product Category")
ax.set_xlabel("Category", fontsize=9)
ax.set_ylabel("Total Revenue (£)", fontsize=9)
ax.tick_params(axis="x", colors=TEXT, labelsize=9)
plt.tight_layout(pad=1.5)
plt.savefig("screenshots/04_revenue_by_category.png", dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.close()
print("✅ Screenshot 4 saved")

conn.close()
print("\n🎉 All screenshots generated in screenshots/ folder!")
