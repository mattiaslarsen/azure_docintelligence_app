import os
import streamlit as st
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from pathlib import Path
from io import BytesIO

load_dotenv()

# Miljökonfiguration
ENVIRONMENTS = {
    "dev": {
        "name": "🟢 Development (F0)",
        "endpoint": os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT_DEV", "https://your-f0-endpoint.cognitiveservices.azure.com/"),
        "key": os.getenv("AZURE_FORM_RECOGNIZER_KEY_DEV", "your-f0-key-here"),
        "description": "F0 - Free tier, 500 pages/month"
    },
    "stage": {
        "name": "🟡 Staging (S0)", 
        "endpoint": os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT_STAGE", "https://standards0northeuropemattias.cognitiveservices.azure.com/"),
        "key": os.getenv("AZURE_FORM_RECOGNIZER_KEY_STAGE", "your-s0-key-here"),
        "description": "S0 - Standard tier, pay per page"
    }
}

def table_to_markdown(table):
    """Konverterar Azure Document Intelligence tabell till markdown-format"""
    # Skapa 2D-array för tabellen
    table_data = []
    for row_idx in range(table.row_count):
        row = []
        for col_idx in range(table.column_count):
            cell = next((c for c in table.cells if c.row_index == row_idx and c.column_index == col_idx), None)
            cell_content = cell.content if cell else ""
            row.append(cell_content)
        table_data.append(row)
    
    if not table_data:
        return ""
    
    # Skapa markdown-tabell
    markdown_table = ""
    
    # Lägg till headers (första raden)
    headers = table_data[0]
    markdown_table += "| " + " | ".join(headers) + " |\n"
    
    # Lägg till separator-rad
    markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    
    # Lägg till data-rader (från andra raden och framåt)
    for row in table_data[1:]:
        markdown_table += "| " + " | ".join(row) + " |\n"
    
    return markdown_table

st.set_page_config(page_title="PDF till Tabell/Text med Azure", layout="centered")

st.title("📄 Azure PDF-analys")

# Miljöväxling
st.sidebar.header("⚙️ Miljökonfiguration")
selected_env = st.sidebar.selectbox(
    "Välj miljö:",
    options=list(ENVIRONMENTS.keys()),
    format_func=lambda x: ENVIRONMENTS[x]["name"],
    index=0 if os.getenv("DEFAULT_ENVIRONMENT") == "dev" else 1
)

# Visa miljöinfo
env_info = ENVIRONMENTS[selected_env]
st.sidebar.info(f"**Aktiv miljö:** {env_info['name']}\n\n{env_info['description']}")

# Kontrollera om miljö är konfigurerad
if not env_info["endpoint"] or env_info["endpoint"].startswith("https://your-"):
    st.sidebar.error("❌ Miljö inte konfigurerad i .env-fil")
elif not env_info["key"] or env_info["key"].startswith("your-"):
    st.sidebar.error("❌ API-nyckel saknas i .env-fil")

pdf_file = st.file_uploader("Välj en PDF-fil", type=["pdf"])
output_dir = st.text_input("Namn på output-mapp", "output")

# Visa filstorleksgränser
st.info("📏 **Filstorleksgränser:** Azure Document Intelligence accepterar max 500 MB per fil")

if pdf_file:
    # Läs filen EN gång och återanvänd
    pdf_bytes = pdf_file.read()
    pdf_stream = BytesIO(pdf_bytes)
    
    # Visa filinfo
    file_size_mb = len(pdf_bytes) / (1024 * 1024)
    st.write(f"📁 **Vald fil:** {pdf_file.name}")
    st.write(f"📊 **Storlek:** {file_size_mb:.2f} MB")
    
    if file_size_mb > 500:
        st.error(f"❌ **Filen är för stor!** Max 500 MB tillåtet, din fil är {file_size_mb:.2f} MB")
        st.stop()
    
    if output_dir:
        with st.spinner("🔍 Läser in och analyserar PDF..."):
            try:
                endpoint = env_info["endpoint"]
                key = env_info["key"]
                
                if not endpoint or not key:
                    st.error(f"❌ **Saknade miljövariabler för {env_info['name']}!** Kontrollera AZURE_FORM_RECOGNIZER_ENDPOINT_{selected_env.upper()} och AZURE_FORM_RECOGNIZER_KEY_{selected_env.upper()}")
                    st.stop()
                
                client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

                poller = client.begin_analyze_document("prebuilt-layout", document=pdf_stream)
                result = poller.result()

                st.write(f"📄 Antal sidor i analysresultat: {len(result.pages)}")

                out_path = Path(output_dir)
                out_path.mkdir(exist_ok=True)

                # Spara text med tabeller integrerade
                with open(out_path / "text.md", "w", encoding="utf-8") as f:
                    # Skriv vanlig text först
                    for page in result.pages:
                        for line in page.lines:
                            f.write(line.content + "\n")
                    
                    # Lägg till tabeller i markdown-format
                    if result.tables:
                        f.write("\n## 📊 Tabeller\n\n")
                        for i, table in enumerate(result.tables):
                            f.write(f"### Tabell {i+1}\n\n")
                            markdown_table = table_to_markdown(table)
                            f.write(markdown_table)
                            f.write("\n")

                # Spara tabeller som CSV också (för bakåtkompatibilitet)
                import pandas as pd
                table_count = 0
                for i, table in enumerate(result.tables):
                    rows = []
                    for row_idx in range(table.row_count):
                        row = []
                        for col_idx in range(table.column_count):
                            cell = next((c for c in table.cells if c.row_index == row_idx and c.column_index == col_idx), None)
                            row.append(cell.content if cell else "")
                        rows.append(row)
                    
                    if rows:
                        # Separera headers från data
                        headers = rows[0] if rows else []
                        data = rows[1:] if len(rows) > 1 else []
                        
                        # Skapa DataFrame med beskrivande kolumnnamn
                        df = pd.DataFrame(data, columns=headers)
                        df.to_csv(out_path / f"table_{i+1}.csv", index=False)
                        table_count += 1

                st.success(f"✅ **Klar!** Text med markdown-tabeller sparad i `{output_dir}/text.md` och {table_count} tabell(er) i `.csv`-filer.")
                
                # Visa preview av text
                with st.expander("📄 Förhandsvisning av text"):
                    with open(out_path / "text.md", "r", encoding="utf-8") as f:
                        text_content = f.read()
                    st.text_area("Extraherad text:", text_content[:1000] + "..." if len(text_content) > 1000 else text_content, height=200)
                
            except Exception as e:
                st.error(f"❌ **Fel vid analys:** {str(e)}")
                if "InvalidContentLength" in str(e):
                    st.error("📏 **Filen är för stor för Azure Document Intelligence.** Prova med en mindre fil eller dela upp den.")
                elif "InvalidRequest" in str(e):
                    st.error("🔍 **Ogiltig begäran.** Kontrollera att filen är en giltig PDF.")
                else:
                    st.error("🔧 **Ett oväntat fel uppstod.** Kontrollera din Azure-konfiguration.")
