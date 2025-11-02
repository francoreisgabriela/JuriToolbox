# ⚖️ JuriToolbox — Prazos, ANPP e Dosimetria (Streamlit)

**JuriToolbox** é um app educacional em Streamlit com três módulos práticos para estudantes e profissionais do Direito:

1. **Calculadora de Prazos Processuais (CPC/CPP)**  
   - Conta **dias úteis** (CPC) ou **corridos** (CPP).  
   - Upload de **feriados** em CSV (uma coluna `date` em `YYYY-MM-DD`).  
   - Exclui o dia do começo, prorroga se cair em dia não útil (opcional no CPP).  
   - Gera **linha do tempo** de cada dia até o vencimento.

2. **Elegibilidade ao ANPP (art. 28-A do CPP)**  
   - Checklist guiado (pena mínima, violência/grave ameaça, confissão, reincidência, etc.).  
   - Explica **por que** o caso é elegível ou não, com parecer sintético.

3. **Dosimetria Simplificada (art. 59 do CP)**  
   - Ajuste da **pena-base** entre mínimo e máximo com fatores judiciais.  
   - Causas de diminuição/agravamento **ilustrativas**.  
   - Gera um **rascunho de fundamentação** em texto.

> **Aviso**: ferramenta **didática**. Não substitui análise jurídica do caso concreto nem consultoria profissional.

---

## 🧰 Tecnologias
- Python 3.10+
- Streamlit
- pandas
- python-dateutil

---

## 📦 Instalação (local)

```bash
# 1) Clone o repositório
git clone https://github.com/<seu-usuario>/juritoolbox.git
cd juritoolbox

# 2) Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Instale dependências
pip install -r requirements.txt

# 4) Rode o app
streamlit run app.py
