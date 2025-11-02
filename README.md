# ⚖️ JuriToolbox — ANPP e Dosimetria (Streamlit)

App **jurídico educacional** feito em Python + Streamlit.  
Inclui dois módulos:

1. **Elegibilidade ao ANPP (art. 28-A CPP)**  
   - Checklist simplificado com requisitos: pena mínima, violência, confissão, reincidência etc.  
   - Indica se o caso é elegível ou não, com justificativa automática.

2. **Dosimetria Simplificada (art. 59 CP)**  
   - Ajuste de pena-base por circunstâncias judiciais.  
   - Minorantes e majorantes com percentuais ilustrativos.  
   - Geração automática de rascunho de fundamentação.

> ⚠️ **Uso acadêmico**. Não substitui a análise jurídica de casos concretos.

---

## 🧰 Instalação e execução local

```bash
git clone https://github.com/<seu-usuario>/juritoolbox.git
cd juritoolbox
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
