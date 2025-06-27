import pandas as pd
from pathlib import Path

# Testdata som liknar dina tabeller
test_data = [
    ["Test", "Date Started", "Acceptance Criteria", "Result"],
    ["USP <661.2> Physicochemical Test: Absorbance", "18Jul2023", "NMT 0.20", "1.30 ✘"],
    ["USP <661.2> Physicochemical Test: Total Organic Carbon", "18Jul2023", "The difference in TOC concentrations between Solution C1 and a suitable blank is NMT 8 mg/L.", "✘ 14 mg/L"]
]

print("=== GAMMAL METOD (med problem) ===")
# Gammal metod - inkluderar headers i data
df_old = pd.DataFrame(test_data)
print("DataFrame med numeriska kolumnnamn:")
print(df_old)
print(f"DataFrame columns: {df_old.columns.tolist()}")

print("\n=== NY METOD (förbättrad) ===")
# Ny metod - separerar headers från data
if test_data:
    headers = test_data[0]
    data = test_data[1:]
    df_new = pd.DataFrame(data, columns=headers)
    print("DataFrame med beskrivande kolumnnamn:")
    print(df_new)
    print(f"DataFrame columns: {df_new.columns.tolist()}")

# Spara som CSV
output_path = Path("test_output")
output_path.mkdir(exist_ok=True)

# Test med ny metod
if test_data:
    headers = test_data[0]
    data = test_data[1:]
    df_new = pd.DataFrame(data, columns=headers)
    df_new.to_csv(output_path / "test_table_improved.csv", index=False)

print("\nCSV-fil skapad: test_output/test_table_improved.csv")
print("Kontrollera att index-kolumnen är borta!") 