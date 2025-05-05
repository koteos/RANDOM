import pandas as pd
import matplotlib.pyplot as plt

# Sample data for cash flow over years (replace with your actual data)
data = {
    "Year": [1, 2, 3, 4, 5, 6],
    "Cash Flow": [-150000, -200000, -100000, 50000, 200000, 350000]  # Negative = Investment, Positive = Sales
}

df = pd.DataFrame(data)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(df["Year"], df["Cash Flow"], marker='o', linestyle='-')

# Add labels and title
plt.xlabel("Year")
plt.ylabel("Cash Flow (USD)")
plt.title("Average Robotic Startup Cash Flow vs. Investment and Sales Over Years")
plt.grid(True)
plt.axhline(0, color='red', linestyle='--', linewidth=1)  # Break-even line

# Annotate the break-even point (if applicable with this data)
break_even_year = df[df["Cash Flow"] >= 0]["Year"].min()
if not pd.isna(break_even_year):
    plt.annotate(f'Break-even at Year {int(break_even_year)}',
                 xy=(break_even_year, 0),
                 xytext=(break_even_year + 0.5, -50000),
                 arrowprops=dict(facecolor='black', shrink=0.05))

# Show the plot
plt.xticks(df["Year"]) # Ensure all years are displayed on the x-axis
plt.tight_layout()
plt.show()
