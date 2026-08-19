import html
import streamlit as st
from tools import analyze_tokens

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="BPE Tokenizer Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ÖZEL CSS ---
st.markdown(
    """
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    
    div[data-testid="metric-container"] {
        background-color: #1E2127;
        border: 1px solid #2B303B;
        padding: 15px 20px;
        border-radius: 12px;
    }
    
    /* Token Kartları */
    .token-card {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        background-color: #1E2127;
        border: 1px solid #3B82F6;
        border-radius: 8px;
        padding: 6px 12px;
        margin: 4px;
        min-width: 55px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .token-text {
        color: #10B981;
        font-family: 'Fira Code', monospace;
        font-weight: bold;
        font-size: 15px;
        white-space: pre;
    }
    
    .token-id {
        color: #9CA3AF;
        font-size: 11px;
        margin-top: 2px;
        font-family: sans-serif;
    }
    
    /* Metin kutusunu biraz daha belirgin yap */
    .stTextArea textarea {
        background-color: #1E2127 !important;
        color: #FAFAFA !important;
        border: 1px solid #3B82F6 !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("✨ BPE Tokenizer Studio")
st.markdown(
    "Sıfırdan eğittiğimiz BPE modelinin metin parçalama yeteneğini inceleyin."
)
st.divider()

with st.sidebar:
    st.header("⚙️ Sistem Durumu")
    st.success("✅ Model Aktif")
    st.info("Kullanılan Sözlük: `merges.json`")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📝 Metin Girişi")
    
    # METİN UZUNLUĞU VE KUTU BOYUTU BURADA ARTIRILDI
    user_input = st.text_area(
        "Analiz edilecek metni girin:",
        height=600,  # Kutu yüksekliği devasa yapıldı
        max_chars=500000, # Yarım milyon karaktere kadar izin verildi
        placeholder="Örn: Merhaba dünya! BPE algoritması çalışıyor.\n(Uzun paragraflar veya makaleler yapıştırabilirsiniz.)",
    )

    analyze_btn = st.button(
        "🚀 Tokenleri Analiz Et", use_container_width=True, type="primary"
    )

with col2:
    st.subheader("📊 Analiz Raporu")

    if analyze_btn and user_input.strip():
        try:
            with st.spinner("Analiz ediliyor..."):
                report = analyze_tokens(user_input)

            # --- 1. METRİK SATIRI ---
            m1, m2, m3 = st.columns(3)
            m1.metric(
                label="Karakter / Bayt",
                value=f"{report['character_count']} / {report['byte_size']}",
            )
            m2.metric(
                label="Token Sayısı", value=report["compressed_token_count"]
            )
            m3.metric(
                label="Sıkıştırma Oranı", value=report["compression_ratio"]
            )

            st.write("")  # Boşluk satırı

            # --- 2. METRİK SATIRI (MALİYET DAHİL) ---
            m4, m5, m6 = st.columns(3)
            m4.metric(
                label="Tahmini API Maliyeti",
                value=report["estimated_cost_usd"],
            )
            m5.metric(label="Model Sözlüğü", value="merges.json")
            m6.metric(label="Performans", value="Optimum")

            st.divider()

            # --- DETAYLI TOKEN KARTLARI GÖRSELLEŞTİRMESİ ---
            st.subheader("🧩 Parçalanan Tokenler (Metin & ID)")

            token_cards_html = ""
            for item in report["tokens_detailed"]:
                tid = item["id"]
                ttext = item["text"]

                # Görünmez karakterleri görünür simgelere dönüştüren kod
                display_text = (
                    ttext.replace(" ", "␣")
                    .replace("\n", "↵")
                    .replace("\t", "⇥")
                )
                if not display_text:
                    display_text = "∅"

                token_cards_html += f"<div class='token-card'><span class='token-text'>{html.escape(display_text)}</span><span class='token-id'>ID: {tid}</span></div>"

            st.markdown(
                f"<div style='display: flex; flex-wrap: wrap;'>{token_cards_html}</div>",
                unsafe_allow_html=True,
            )

            with st.expander("Geliştirici Formatı (JSON Output)"):
                st.json(report)

        except FileNotFoundError:
            st.error(
                "🚨 Hata: `merges.json` dosyası bulunamadı! Lütfen önce `python train.py` komutunu çalıştırın."
            )
        except Exception as e:
            st.error(f"Beklenmeyen bir hata oluştu: {str(e)}")

    elif analyze_btn and not user_input.strip():
        st.warning("Lütfen analiz etmek için bir metin girin.")
    else:
        st.info("👈 Analizi başlatmak için sol tarafa metin girin.")