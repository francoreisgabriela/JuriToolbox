# ⚖️ JuriToolbox — Prazos, ANPP e Dosimetria (Streamlit)

App educacional em **Streamlit** com 3 módulos:
1. **Calculadora de prazos** (CPC dias úteis / CPP corridos, com opção de prorrogar e upload de feriados).
2. **Elegibilidade ao ANPP (art. 28-A CPP)** — checklist didático.
3. **Dosimetria simplificada (art. 59 CP)** — pena-base + minorantes/majorantes ilustrativas e rascunho de fundamentação.

> **Aviso**: ferramenta **pedagógica**. Não substitui análise do caso concreto.

## Como rodar localmente
```bash
git clone https://github.com/<seu-usuario>/juritoolbox.git
cd juritoolbox
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
