import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="Advanced Number Generator",
    page_icon="📊",
    layout="wide"
)
st.title("📊 Whole Number to Fraction Generator")
st.markdown("""
Enter **5 whole numbers**. Each number will be **divided by 1000** to create fractions, and then **40 simulated values** will be generated from the same distribution.  
All values are displayed in **0.001 format** for clarity.
""")

# ----------------- Input Section -----------------
st.header("🔢 Input Whole Numbers")
cols = st.columns(5)
input_numbers = []

for i, col in enumerate(cols):
    num = col.number_input(
        f"Number {i+1}", 
        min_value=0, 
        step=1, 
        format="%d", 
        key=f"num{i}"
    )
    input_numbers.append(num)

# Convert numbers to fractions
fractions = [n / 1000 for n in input_numbers]

# ----------------- Generate Values -----------------
if st.button("✨ Generate Values"):
    if len(fractions) < 5:
        st.warning("Please enter all 5 numbers.")
    else:
        # Calculate mean & std
        mean_val = np.mean(fractions)
        std_val = np.std(fractions, ddof=1)

        st.success(f"✅ Mean: **{mean_val:.4f}**, Standard Deviation: **{std_val:.4f}**")

        # Generate 40 values
        generated_values = np.random.normal(loc=mean_val, scale=std_val, size=40)
        generated_values = [round(val, 4) for val in generated_values]  # 0.001 format

        # ----------------- Display Table -----------------
        df = pd.DataFrame(generated_values, columns=["Generated Values"])
        st.header("📋 Generated 40 Values")
        st.dataframe(df, use_container_width=True)

        # ----------------- Distribution Plot -----------------
        st.header("📈 Distribution of Generated Values")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(generated_values, bins=10, kde=True, color='skyblue', ax=ax)
        ax.axvline(mean_val, color="red", linestyle="--", label=f"Mean = {mean_val:.4f}")
        ax.set_xlabel("Values")
        ax.set_ylabel("Frequency")
        ax.legend()
        st.pyplot(fig)

        # ----------------- Download Option -----------------
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download as CSV", data=csv, file_name="generated_values.csv", mime="text/csv")
