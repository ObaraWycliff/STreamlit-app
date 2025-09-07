import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# App title & description
st.set_page_config(page_title="Stat Generator", page_icon="📊", layout="centered")
st.title("📊 Mean & Standard Deviation Generator")
st.write("Enter **5 values (3 decimal places)** and generate **40 simulated values** with the same distribution.")

# Input section
st.header("🔢 Input Values")
cols = st.columns(5)
values = []

for i, col in enumerate(cols):
    val = col.number_input(f"Value {i+1}", format="%.3f", step=0.001, key=f"val{i}")
    values.append(val)

# Only process if all 5 values are entered
if st.button("✨ Generate Values"):
    if any(v == 0 for v in values):  
        st.warning("Please enter all 5 values (non-zero).")
    else:
        # Mean & Std
        mean_val = np.mean(values)
        std_val = np.std(values, ddof=1)

        st.success(f"✅ Mean: **{mean_val:.3f}**,  Standard Deviation: **{std_val:.3f}**")

        # Generate values
        generated_values = np.random.normal(loc=mean_val, scale=std_val, size=40)
        generated_values = [round(val, 3) for val in generated_values]

        # Convert to DataFrame
        df = pd.DataFrame(generated_values, columns=["Generated Values"])

        # Show table
        st.header("📋 Generated 40 Values")
        st.dataframe(df, use_container_width=True)

        # Plot chart
        st.header("📈 Distribution of Generated Values")
        fig, ax = plt.subplots()
        ax.hist(generated_values, bins=10, edgecolor="black")
        ax.axvline(mean_val, color="red", linestyle="--", label=f"Mean = {mean_val:.3f}")
        ax.legend()
        st.pyplot(fig)

        # Download option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download as CSV", data=csv, file_name="generated_values.csv", mime="text/csv")
