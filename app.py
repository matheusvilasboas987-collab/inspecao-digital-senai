import streamlit as st
import smtplib
from email.message import EmailMessage
from datetime import datetime

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="SENAI - Inspeção Digital",
    page_icon="⚙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS com regras de cor PRETA para os Expanders
SENAI_STYLE = """
<style>
    :root {
        --senai-blue-dark: #003366;
        --senai-blue-button: #004588;
        --senai-bg-card: #002244;
        --senai-border: #ffffff;
    }

    /* Trava o fundo da tela para não permitir rolagem */
    html, body, .stApp {
        background-color: var(--senai-blue-dark) !important;
        font-family: 'Segoe UI', Roboto, sans-serif;
        color: #ffffff !important;
    }

    #MainMenu, footer, header {visibility: hidden;}

    ::-webkit-scrollbar {
        display: none;
    }

    /* Reduz espaçamentos do bloco principal do Streamlit */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 450px !important;
    }

    /* Cabeçalho do topo compacto */
    .login-header-text {
        color: white !important;
        text-align: center;
        margin-bottom: 12px;
    }

    .login-header-text h1 {
        font-size: 26px;
        font-weight: 700;
        margin: 2px 0 2px 0;
        color: #ffffff !important;
    }

    .login-header-text p {
        font-size: 13px;
        color: #ffffff !important;
        margin: 0;
    }

    /* Rótulos e Textos em Geral na Cor Branca */
    label, p, span, h1, h2, h3, h4, h5, h6, .stMarkdown, div[data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }

    /* Caixa Única com fundo escuro e fontes brancas */
    div.stContainer {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 24px !important;
        padding: 20px 18px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Campos de Entrada */
    .stTextInput {
        margin-bottom: 5px !important;
    }

    .stTextInput > label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        padding: 8px 12px !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        height: 42px !important;
    }

    /* Botão Principal Entrar */
    div.stButton > button {
        background-color: var(--senai-blue-button) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 10px 15px !important;
        transition: all 0.2s ease-in-out !important;
        margin-top: 5px;
    }

    div.stButton > button:hover {
        background-color: #001122 !important;
    }

    /* REGRA ESPECÍFICA DE COR PRETA PARA OS EXPANDERS DA TELA 3 */
    .stExpander {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
        margin-bottom: 10px !important;
    }

    /* Título/Cabeçalho do Expander na cor PRETA */
    .streamlit-expanderHeader, 
    details summary,
    details summary p,
    details summary span,
    details summary div {
        color: #000000 !important;
        background-color: #f1f5f9 !important;
        border-radius: 8px !important;
        font-weight: 800 !important;
    }

    /* Ícone de seta do expander na cor preta */
    details summary svg {
        fill: #000000 !important;
        color: #000000 !important;
    }

    /* Conteúdo interno do Expander totalmente na cor PRETA */
    div[data-testid="stExpanderDetails"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 12px !important;
        border-radius: 0 0 8px 8px !important;
    }

    div[data-testid="stExpanderDetails"] * {
        color: #000000 !important;
    }

    /* BARRA FIXA NO TOPO PARA TELAS INTERNAS */
    .senai-internal-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: var(--senai-blue-dark);
        color: #ffffff !important;
        padding: 14px;
        border-radius: 0 0 16px 16px;
        text-align: center;
        font-weight: 800;
        font-size: 18px;
        margin-bottom: 15px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
</style>
"""

st.markdown(SENAI_STYLE, unsafe_allow_html=True)

if "tela" not in st.session_state:
    st.session_state.tela = "login"

def navegar(tela):
    st.session_state.tela = tela

# Função para envio de e-mail via SMTP com fotos em anexo
def enviar_email(assunto, corpo_html, anexos_fotos=None):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    EMAIL_REMETENTE = "0001089021@senaimgaluno.com.br"
    SENHA_REMETENTE = "yose hbax ikfy cujc"

    DESTINATARIOS = [
        "0001089021@senaimgaluno.com.br",
        "0001157432@senaimgaluno.com.br"
    ]

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = ", ".join(DESTINATARIOS)
    msg.set_content("Mensagem enviada via App de Inspeção Digital SENAI.")
    msg.add_alternative(corpo_html, subtype='html')

    if anexos_fotos:
        for item_id, dados_foto in anexos_fotos.items():
            if dados_foto and "bytes" in dados_foto:
                foto_bytes = dados_foto["bytes"]
                foto_nome = dados_foto.get("nome", f"foto_item_{item_id}.jpg")
                ext = foto_nome.split('.')[-1].lower() if '.' in foto_nome else 'jpg'
                subtipo = "png" if ext == "png" else "jpeg"
                
                msg.add_attachment(
                    foto_bytes,
                    maintype='image',
                    subtype=subtipo,
                    filename=f"Evidencia_Item_{item_id}.{ext}"
                )

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
        server.send_message(msg)
        server.quit()
        return True, "E-mail enviado com sucesso!"
    except Exception as e:
        return False, str(e)

# SVG do Logo SENAI Ajustado
SENAI_LOGO_WHITE_SVG = """
<div style="text-align: center; margin-top: 5px; margin-bottom: 0px; margin-left: 25px;">
    <svg width="340" height="90" viewBox="0 0 360 95" fill="none" xmlns="http://www.w3.org/2000/svg">
        <text x="30" y="78" font-family="'Arial Black', 'Helvetica Neue', sans-serif" font-size="94" font-weight="900" font-style="italic" fill="#FFFFFF" letter-spacing="-4">SENAI</text>
    </svg>
    <div style="color: #ffffff; font-size: 12px; font-weight: 500; margin-top: -12px; opacity: 0.95; padding-right: 25px;">
        Serviço Nacional de Aprendizagem Industrial
    </div>
</div>
"""

# ==================== TELA 1: LOGIN ====================
if st.session_state.tela == "login":
    st.markdown(SENAI_LOGO_WHITE_SVG, unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="login-header-text">
            <h1>Inspeção Digital</h1>
            <p>Plataforma de inspeção de máquinas da oficina</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # CAIXA ÚNICA COM TEXTOS EM BRANCO
    with st.container():
        usuario_input = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
        senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")

        if st.button("Entrar", use_container_width=True):
            st.session_state.usuario_logado = usuario_input if usuario_input else "Operador SENAI"
            navegar("lista_maquinas")
            st.rerun()

        st.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.2);">
                <div style="display: flex; align-items: center; gap: 10px; width: 100%; margin-left: 25px;">
                    <div style="font-size: 20px; color: #ffffff;">⚙️</div>
                    <div style="font-size: 11px; color: #ffffff; font-weight: 600; line-height: 1.2;">
                        Segurança, qualidade e eficiência começam com a inspeção.
                    </div>
                </div>
                <div style="text-align: center; margin-top: 35px; margin-bottom: 5px; font-weight: 900; color: #ffffff; font-size: 38px; letter-spacing: 3px; line-height: 1.0;">
                    MMI
                    <div style="font-weight: 800; color: #ffffff; font-size: 28px; margin-top: 4px;">2026</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==================== TELA 2: MÁQUINAS DA OFICINA ====================
elif st.session_state.tela == "lista_maquinas":
    st.markdown('<div class="senai-internal-header">Oficina Mecânica - Máquinas</div>', unsafe_allow_html=True)

    maquinas = [
        {"id": "torno", "nome": "Torno ROMI T 240", "imagem": "torno_romi_t240.png"},
        {"id": "esmeril", "nome": "Moto Esmeril", "imagem": "esmeril.png"},
        {"id": "fresadora", "nome": "Fresadora Ferramenteira", "imagem": "fresadora.png"},
        {"id": "injetora", "nome": "Injetora de Plástico", "imagem": "injetora.png"},
        {"id": "solda", "nome": "Cabine de Solda", "imagem": "cabine_solda.png"}
    ]

    for item in maquinas:
        with st.container():
            col_img, col_btn = st.columns([3, 1], vertical_alignment="center")
            
            with col_img:
                try:
                    st.image(item["imagem"], use_container_width=True)
                except Exception:
                    st.warning(f"Imagem `{item['imagem']}` não encontrada.")
                
            with col_btn:
                if st.button("Ver máquina >", key=item["id"], use_container_width=True):
                    if item["id"] == "torno":
                        navegar("detalhes_maquina")
                        st.rerun()

# ==================== TELA 3: DETALHES DA MÁQUINA ====================
elif st.session_state.tela == "detalhes_maquina":
    if "historico_manutencao" not in st.session_state:
        st.session_state.historico_manutencao = [
            {"data": "12/07/2026", "tipo": "Preventiva", "descricao": "Troca do fluido de corte e ajuste das correias.", "tecnico": "Carlos Silva"},
            {"data": "15/03/2026", "tipo": "Corretiva", "descricao": "Troca do fusível do painel e alinhamento do contraponto.", "tecnico": "Roberto Lima"},
            {"data": "10/01/2026", "tipo": "Preventiva", "descricao": "Lubrificação geral dos barramentos e reaperto do mandril.", "tecnico": "Carlos Silva"}
        ]

    if "catalogo_pecas" not in st.session_state:
        st.session_state.catalogo_pecas = [
            {"codigo": "R808-PL200", "nome": "Placa Universal 3 Castanhas Ø200mm (Passagem Ø55mm)", "categoria": "Fixação", "estoque": 2, "status": "Em Estoque"},
            {"codigo": "R808-PL250", "nome": "Placa Universal 3 Castanhas Ø250mm (Passagem Ø76mm)", "categoria": "Fixação", "estoque": 1, "status": "Em Estoque"},
            {"codigo": "R808-CM4-60", "nome": "Ponto Fixo CM-4 x 60º (Eixo Árvore / Cabeçote Móvel)", "categoria": "Árvore / Cabeçote", "estoque": 6, "status": "Em Estoque"},
            {"codigo": "R808-COR-TRAP", "nome": "Jogo de Correias Trapezoidais de Transmissão", "categoria": "Transmissão", "estoque": 5, "status": "Em Estoque"},
            {"codigo": "R808-REC-JOGO", "nome": "Jogo de Engrenagens do Recâmbio (Passo/Avanço)", "categoria": "Transmissão", "estoque": 1, "status": "Crítico"},
            {"codigo": "R808-MIC-SEG", "nome": "Micro-switch Duplo Canal (Proteção Móvel da Placa)", "categoria": "Elétrica/Segurança", "estoque": 2, "status": "Em Estoque"},
            {"codigo": "R808-FILT-LUB", "nome": "Filtro de Sucção da Bomba de Refrigeração de Corte", "categoria": "Lubrificação/Corte", "estoque": 8, "status": "Em Estoque"}
        ]

    if st.button("← Voltar para lista"):
        navegar("lista_maquinas")
        st.rerun()

    st.markdown('<div class="senai-internal-header">Torno ROMI T 240</div>', unsafe_allow_html=True)

    try:
        st.image("torno_romi_t240.png", use_container_width=True)
    except Exception:
        st.warning("Imagem `torno_romi_t240.png` não encontrada.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. MANUAL DO USUÁRIO
    with st.expander("📖 Manual do Usuário", expanded=False):
        st.markdown("<span style='color: #000000 !important;'>Consulte ou faça o download do manual técnico do equipamento.</span>", unsafe_allow_html=True)
        try:
            with open("manual_torno_romi_t240.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📄 Baixar Manual em PDF",
                    data=pdf_file,
                    file_name="Manual_Torno_ROMI_T240.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        except FileNotFoundError:
            st.info("💡 Adicione o arquivo `manual_torno_romi_t240.pdf` na pasta raiz do projeto para liberar o download.")

    # 2. HISTÓRICO DE MANUTENÇÃO
    with st.expander("⏱️ Histórico de Manutenção", expanded=False):
        for item in st.session_state.historico_manutencao:
            cor_badge = "#004588" if item["tipo"] == "Preventiva" else "#e30613"
            st.markdown(
                f"""
                <div style="background-color: #f8fafc; border: 1px solid #d1d5db; border-left: 4px solid {cor_badge}; border-radius: 6px; padding: 10px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #000000 !important;">
                        <span style="color: #000000 !important;">📅 <b>{item['data']}</b></span>
                        <span style="background-color: {cor_badge}; color: white !important; padding: 2px 6px; border-radius: 4px; font-weight: bold;">{item['tipo']}</span>
                    </div>
                    <div style="font-size: 14px; margin-top: 6px; color: #000000 !important;">{item['descricao']}</div>
                    <div style="font-size: 11px; color: #333333 !important; margin-top: 4px;">👨‍🔧 Técnico: {item['tecnico']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        with st.form("form_historico", clear_on_submit=True):
            st.markdown("<b style='color: #000000 !important;'>➕ Registrar Nova Manutenção:</b>", unsafe_allow_html=True)
            nova_data = st.date_input("Data do serviço").strftime("%d/%m/%Y")
            novo_tipo = st.selectbox("Tipo de Manutenção", ["Preventiva", "Corretiva", "Preditiva"])
            nova_desc = st.text_input("Descrição do serviço realizado", placeholder="Ex: Substituição do óleo da caixa de engrenagens")
            novo_tecnico = st.text_input("Nome do Técnico/Responsável", placeholder="Ex: João Souza")
            
            if st.form_submit_button("Salvar no Histórico", use_container_width=True):
                if nova_desc and novo_tecnico:
                    st.session_state.historico_manutencao.insert(0, {
                        "data": nova_data, "tipo": novo_tipo, "descricao": nova_desc, "tecnico": novo_tecnico
                    })
                    st.toast("Manutenção registrada com sucesso!", icon="✅")
                    st.rerun()

    # 3. CÓDIGOS E PEÇAS DE REPOSIÇÃO
    with st.expander("📦 Códigos e Peças de Reposição", expanded=False):
        termo_busca = st.text_input("🔍 Buscar por nome ou código...", placeholder="Ex: Placa, R808-CM4, Correia", key="busca_peca")
        
        pecas_filtradas = st.session_state.catalogo_pecas
        if termo_busca:
            pecas_filtradas = [p for p in pecas_filtradas if termo_busca.lower() in p["nome"].lower() or termo_busca.lower() in p["codigo"].lower()]

        for peca in pecas_filtradas:
            st.markdown(
                f"""
                <div style="background-color: #f8fafc; border: 1px solid #d1d5db; border-radius: 6px; padding: 10px; margin-bottom: 8px;">
                    <div style="font-size: 14px; font-weight: bold; color: #004588 !important;">{peca['nome']}</div>
                    <div style="font-size: 12px; color: #000000 !important; margin-top: 2px;">Código: <code style="color: #000000 !important;">{peca['codigo']}</code> | Categoria: {peca['categoria']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        with st.form("form_requisicao", clear_on_submit=True):
            st.markdown("<b style='color: #000000 !important;'>🛒 Enviar Solicitação ao Almoxarifado:</b>", unsafe_allow_html=True)
            peca_selecionada = st.selectbox("Selecione a peça cadastrada", [f"{p['codigo']} - {p['nome']}" for p in st.session_state.catalogo_pecas])
            qtd_pedida = st.number_input("Quantidade solicitada", min_value=1, max_value=20, value=1)
            obs_pedido = st.text_input("Observação / Motivo da troca", placeholder="Ex: Substituição preventiva em aula prática")
            
            if st.form_submit_button("Enviar Requisição por E-mail", use_container_width=True):
                usuario_atual = st.session_state.get("usuario_logado", "Operador SENAI")
                data_hora_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
                
                assunto_req = f"🛒 Solicitação de Peça: {peca_selecionada.split(' - ')[0]} - Torno ROMI T 240"
                corpo_req_html = f"""
                <h2>📦 SENAI - Solicitação de Peça / Almoxarifado</h2>
                <p><b>Equipamento:</b> Torno ROMI T 240</p>
                <p><b>Solicitante:</b> {usuario_atual}</p>
                <p><b>Data e Horário:</b> {data_hora_atual}</p>
                <hr>
                <h3>Item Solicitado:</h3>
                <ul>
                    <li><b>Peça/Código:</b> {peca_selecionada}</li>
                    <li><b>Quantidade:</b> {qtd_pedida} unidade(s)</li>
                    <li><b>Motivo/Observação:</b> {obs_pedido if obs_pedido else 'Não informado'}</li>
                </ul>
                <hr>
                <p style="font-size: 11px; color: #777;">E-mail disparado automaticamente via App Inspeção Digital SENAI.</p>
                """
                
                sucesso, msg_err = enviar_email(assunto_req, corpo_req_html)
                if sucesso:
                    st.success("✉️ Solicitação enviada por e-mail com sucesso ao almoxarifado!")
                else:
                    st.error(f"⚠️ Falha no disparo do e-mail: {msg_err}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Iniciar inspeção", use_container_width=True):
        st.session_state.item_checklist_atual = 0
        st.session_state.respostas_checklist = {}
        navegar("checklist")
        st.rerun()

# ==================== TELA 4: CHECKLIST ====================
elif st.session_state.tela == "checklist":
    perguntas_checklist = [
        {"id": 1, "titulo": "Limpeza e Organização", "pergunta": "O equipamento apresenta condições gerais de limpeza e organização adequadas?"},
        {"id": 2, "titulo": "Sistema de Lubrificação", "pergunta": "O sistema de lubrificação está funcionando corretamente e com nível adequado?"},
        {"id": 3, "titulo": "Vazamentos de Óleo/Flutuantes", "pergunta": "Há vazamentos de óleo ou fluido hidráulico/refrigerante no equipamento?"},
        {"id": 4, "titulo": "Condição do Mandril", "pergunta": "O mandril está em boas condições e apresenta fixação adequada da peça?"},
        {"id": 5, "titulo": "Castanhas do Mandril", "pergunta": "As castanhas do mandril apresentam desgaste ou danos excessivos?"},
        {"id": 6, "titulo": "Proteções de Segurança", "pergunta": "Os dispositivos de proteção e portas de segurança estão funcionando corretamente?"},
        {"id": 7, "titulo": "Parada de Emergência", "pergunta": "O botão de parada de emergência está funcionando corretamente?"},
        {"id": 8, "titulo": "Sistema de Refrigeração", "pergunta": "O sistema de refrigeração (fluido de corte) está funcionando adequadamente?"},
        {"id": 9, "titulo": "Guias, Barramentos e Fusos", "pergunta": "Guias, barramentos e fusos apresentam condições adequadas, sem desgaste ou danos aparentes?"},
        {"id": 10, "titulo": "Painel Elétrico e Conexões", "pergunta": "O painel elétrico, cabos e conexões aparentes apresentam condições adequadas, sem danos ou aquecimento anormal?"}
    ]

    total_itens = len(perguntas_checklist)

    if "item_checklist_atual" not in st.session_state:
        st.session_state.item_checklist_atual = 0
    if "respostas_checklist" not in st.session_state:
        st.session_state.respostas_checklist = {}

    idx = st.session_state.item_checklist_atual

    if st.button("← Voltar"):
        if idx > 0:
            st.session_state.item_checklist_atual -= 1
            st.rerun()
        else:
            navegar("detalhes_maquina")
            st.rerun()

    if idx < total_itens:
        item = perguntas_checklist[idx]
        progresso = (idx + 1) / total_itens

        st.markdown('<div class="senai-internal-header">Checklist de Inspeção - Torno ROMI T 240</div>', unsafe_allow_html=True)

        st.caption(f"Progresso: Item {idx + 1} de {total_itens} ({int(progresso * 100)}%)")
        st.progress(progresso)

        st.markdown(
            f"""
            <div style="background-color: rgba(255,255,255,0.1); border-left: 6px solid #ffffff; padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid rgba(255,255,255,0.2);">
                <span style="font-size: 11px; color: #ffffff; font-weight: bold; text-transform: uppercase;">{item['titulo']}</span>
                <h4 style="margin: 5px 0 0 0; color: #ffffff;">{item['id']}. {item['pergunta']}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Garante inicialização da resposta do item
        if item['id'] not in st.session_state.respostas_checklist:
            st.session_state.respostas_checklist[item['id']] = {"status": None, "obs": "", "foto": None}

        status_atual = st.session_state.respostas_checklist[item['id']].get("status", None)
        
        col_ok, col_nok = st.columns(2)
        with col_ok:
            btn_ok = st.button("✅ OK", use_container_width=True, type="primary" if status_atual == "OK" else "secondary")
            if btn_ok:
                st.session_state.respostas_checklist[item['id']]["status"] = "OK"
                st.rerun()

        with col_nok:
            btn_nok = st.button("❌ N/OK", use_container_width=True, type="primary" if status_atual == "N/OK" else "secondary")
            if btn_nok:
                st.session_state.respostas_checklist[item['id']]["status"] = "N/OK"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("📝 Observações e Evidência em Foto", expanded=(status_atual == "N/OK")):
            obs_existente = st.session_state.respostas_checklist[item['id']].get("obs", "")
            observacao = st.text_area("Detalhes da inconformidade ou nota:", value=obs_existente, placeholder="Digite aqui se encontrar algum problema...", height=90)
            
            st.markdown("**📸 Evidência em Foto:**")
            foto_capturada = st.file_uploader(
                "Tirar foto pela câmera ou escolher da galeria", 
                type=["jpg", "png", "jpeg"], 
                key=f"file_{item['id']}"
            )

            # SALVAMENTO IMEDIATO DA FOTO NA MEMÓRIA QUANDO TIRADA
            if foto_capturada is not None:
                st.session_state.respostas_checklist[item['id']]["foto"] = {
                    "bytes": foto_capturada.getvalue(),
                    "nome": foto_capturada.name
                }

            # EXIBE PRÉVIA DA FOTO JÁ CARREGADA/SALVA
            foto_salva = st.session_state.respostas_checklist[item['id']].get("foto")
            if foto_salva and "bytes" in foto_salva:
                st.image(foto_salva["bytes"], caption="✅ Foto salva com sucesso!", width=220)

        st.markdown("<br>", unsafe_allow_html=True)

        # TRAVA OBRIGATÓRIA DE RESPOSTA
        if st.button("💾 Salvar e Próximo Item →", use_container_width=True):
            if status_atual is None:
                st.warning("⚠️ Você precisa responder se o item está OK ou N/OK antes de avançar!")
            else:
                st.session_state.respostas_checklist[item['id']]["obs"] = observacao
                st.session_state.item_checklist_atual += 1
                st.rerun()

    else:
        st.markdown('<div class="senai-internal-header">Relatório Final de Inspeção</div>', unsafe_allow_html=True)
        
        usuario_atual = st.session_state.get("usuario_logado", "Operador SENAI")
        data_hora_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

        st.markdown(
            f"""
            <div style="background-color: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; font-size: 13px; color: #ffffff; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.3);">
                <b>👤 Inspetor:</b> {usuario_atual}<br>
                <b>📅 Data/Hora:</b> {data_hora_atual}<br>
                <b>⚙️ Equipamento:</b> Torno ROMI T 240
            </div>
            """,
            unsafe_allow_html=True
        )

        total_ok = 0
        total_nok = 0
        fotos_para_anexar = {}

        for item in perguntas_checklist:
            resp = st.session_state.respostas_checklist.get(item['id'], {"status": "OK", "obs": "", "foto": None})
            stts = resp.get("status", "OK")
            obs = resp.get("obs", "")
            foto_dados = resp.get("foto", None)
            
            if foto_dados and "bytes" in foto_dados:
                fotos_para_anexar[item['id']] = foto_dados
            
            if stts == "OK":
                total_ok += 1
                cor_status = "#28a745"
            else:
                total_nok += 1
                cor_status = "#e30613"

            st.markdown(
                f"""
                <div style="background-color: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-left: 5px solid {cor_status}; padding: 10px; border-radius: 6px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; font-weight: bold; color: #ffffff;">
                        <span>{item['id']}. {item['titulo']}</span>
                        <span style="color: {cor_status};">{stts}</span>
                    </div>
                    <div style="font-size: 12px; color: #e0e0e0; margin-top: 4px;">{item['pergunta']}</div>
                    {f'<div style="font-size: 12px; color: #e30613; margin-top: 4px;"><b>Obs:</b> {obs}</div>' if obs else ''}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if foto_dados and "bytes" in foto_dados:
                st.image(foto_dados["bytes"], caption=f"Evidência do item {item['id']}", width=200)

        col_stat1, col_stat2 = st.columns(2)
        col_stat1.metric("Itens Conformes (OK)", f"{total_ok}", delta=f"{int(total_ok/total_itens*100)}%")
        col_stat2.metric("Inconformidades (N/OK)", f"{total_nok}", delta_color="inverse")

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🏁 Finalizar e Enviar Relatório por E-mail", use_container_width=True):
            assunto_rep = f"📋 Relatório de Inspeção: Torno ROMI T 240 - {data_hora_atual}"
            
            corpo_rep_html = f"""
            <h2>⚙️ SENAI - Relatório de Inspeção Digital</h2>
            <p><b>Equipamento:</b> Torno ROMI T 240</p>
            <p><b>Inspetor / Técnico:</b> {usuario_atual}</p>
            <p><b>Data e Horário:</b> {data_hora_atual}</p>
            <hr>
            <h3>📋 Detalhes dos Itens Inspecionados:</h3>
            <ul>
            """

            for item in perguntas_checklist:
                resp = st.session_state.respostas_checklist.get(item['id'], {"status": "OK", "obs": "", "foto": None})
                stts = resp.get("status", "OK")
                obs = resp.get("obs", "")
                tem_foto = resp.get("foto", None) is not None
                cor = "green" if stts == "OK" else "red"
                
                corpo_rep_html += f"""
                <li>
                    <b>{item['id']}. {item['titulo']}</b> - <span style="color:{cor}; font-weight:bold;">{stts}</span><br>
                    <small>{item['pergunta']}</small><br>
                    {f'<i>Observação: {obs}</i><br>' if obs else ''}
                    {f'📷 <b>Evidência em foto anexada ao e-mail</b><br>' if tem_foto else ''}
                </li><br>
                """

            corpo_rep_html += """
            </ul>
            <hr>
            <p style="font-size: 11px; color: #777;">Relatório gerado e enviado automaticamente pela Plataforma de Inspeção Digital SENAI.</p>
            """

            sucesso, msg_status = enviar_email(assunto_rep, corpo_rep_html, anexos_fotos=fotos_para_anexar)
            
            if sucesso:
                st.success("✉️ Relatório e foto(s) enviados com sucesso para 0001089021@senaimgaluno.com.br!")
            else:
                st.error(f"⚠️ Erro no envio: {msg_status}. Verifique as credenciais no código.")
                
            navegar("lista_maquinas")
            st.rerun()
