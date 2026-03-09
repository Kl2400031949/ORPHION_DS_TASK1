import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import  matplotlib
matplotlib.use("Agg")   
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


df = pd.read_csv(r"C:\Users\kpran\Downloads\Orphion\population.csv")


if "Country Name" in df.columns:
    df = df.rename(columns={"Country Name": "Country"})
elif "REF_AREA" in df.columns:
    df = df.rename(columns={"REF_AREA": "Country"})


year_cols = [col for col in df.columns if col.isdigit()]
df[year_cols] = df[year_cols].apply(pd.to_numeric, errors='coerce')

pdf_path = fr"C:\Users\kpran\Downloads\Orphion\population_report_{timestamp}.pdf"
pdf = PdfPages(pdf_path)

plt.figure(figsize=(8,6))
sns.histplot(df['2024'], bins=30, kde=True, color="skyblue")
plt.title("Distribution of Female Population 65+ (% in 2024)")
plt.xlabel("Percentage of Female Population")
plt.ylabel("Frequency")
plt.savefig(fr"C:\Users\kpran\Downloads\Orphion\hist_population_2024_{timestamp}.png")
pdf.savefig()
plt.close()

top10 = df.nlargest(10, '2024')
plt.figure(figsize=(10,6))
sns.barplot(
    x="Country",
    y="2024",
    data=top10,
    dodge=False,
    color="skyblue") 
plt.title("Top 10 Countries by Female Population 65+ (% in 2024)")
plt.xticks(rotation=45)
plt.savefig(fr"C:\Users\kpran\Downloads\Orphion\top10_population_2024_{timestamp}.png")
pdf.savefig()
plt.close()


if "India" in df["Country"].values:
    india = df[df["Country"]=="India"].melt(
        id_vars=["Country"], var_name="Year", value_name="Population"
    )
    plt.figure(figsize=(10,6))
    sns.lineplot(x="Year", y="Population", data=india, marker="o")
    plt.title("India: Female Population 65+ (% of female population, 1960–2024)")
    plt.xticks(rotation=45)
    plt.savefig(fr"C:\Users\kpran\Downloads\Orphion\india_population_trend_{timestamp}.png")
    pdf.savefig()
    plt.close()

plt.figure(figsize=(12,8))
sns.heatmap(df[year_cols].corr(), annot=False, cmap="coolwarm")
plt.title("Correlation Between Year Columns")
plt.savefig(fr"C:\Users\kpran\Downloads\Orphion\heatmap_correlation_{timestamp}.png")
pdf.savefig()
plt.close()


pdf.close()