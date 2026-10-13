# Índice de tabelas

| Tabela | Domínio | PK | Colunas | Finalidade |
|---|---|---|---|---|
| `ACTIVITY_DIM_CAP` | bpm-analytics-dw | ACTIVITYID, COMPANYID, PROCESSID, PROCESSVERSION | 7 | Dimensão (modelo estrela do CAP, analytics de BPM) com as atividades de cada versão de processo. |
| `ADAPTER` | bpm-integracao | COD_EMPRESA, COD_ADAPTER | 4 | Cadastro de adapters (conectores externos) do Fluig; cada adapter aponta para um caminho de implementação e é referenciado por APLICATIVO. |
| `ADHOC_PROCES` | bpm-workflow | COD_EMPRESA, NUM_PROCES, NUM_SEQ | 7 | Tarefas ad hoc (atividades avulsas criadas em tempo de execução) vinculadas a um estado/atividade de uma instância de processo. |
| `ADHOC_PROCES_WORKFLOW` | bpm-workflow | COD_EMPRESA, NUM_PROCES_PAI, NUM_SEQ_PROCES_PAI, NUM_PROCES | 5 | Relaciona a instância de processo pai (e seu estado) às instâncias de sub-processo geradas para tarefas ad hoc. |
| `AMBIEN_PROGRESS` | bpm-integracao | COD_EMPRESA, COD_AMBIEN_PROGRES | 3 | Cadastro de ambientes/bibliotecas Progress (ProgressLib) usados para integração com sistemas Datasul/Progress. |
| `ANEXO_PROCES` | bpm-workflow | COD_EMPRESA, NUM_PROCES, NUM_SEQ_ANEXO | 25 | Anexos (documentos do GED) vinculados a instâncias de processo de workflow, com histórico de onde/por quem foram incluídos. |
| `APLICATIVO` | bpm-integracao | COD_EMPRESA, COD_APLICAT | 5 | Cadastro de aplicativos externos executáveis (linha de comando) que o Fluig dispara através de um adapter. |
| `APONT_TAR_PROCES` | bpm-workflow | COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, CD_MATRICULA, NUM_SEQ_TRANSF, NUM_SEQ_APONT | 8 | Apontamentos de esforço (tempo gasto) registrados por usuários em tarefas de instâncias de processo. |
| `APROVACAO` | ged-documentos | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, NUM_NIV_APROVAC | 10 | Registro da aprovação de um documento do GED por um aprovador em um nível de aprovação (resultado, data, observação, assinatura). |
| `APROVADOR` | ged-documentos | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, IDI_TIP_APRVDOR, CD_MATRICULA, NUM_NIV_APROVAC | 7 | Define os aprovadores (usuário ou grupo) designados para cada nível de aprovação de uma versão de documento do GED. |
| `AREA_DEST` | ecm-documents | COD_EMPRESA, COD_AREA | 6 | Cadastro legado de áreas de destino (destinatários/áreas organizacionais) do módulo de documentos, com responsável e servidor de execução. |
| `ASSUNTO` | ecm-documents | COD_EMPRESA, CD_ASSUNTO | 6 | Assuntos (tópicos) de classificação de documentos; define se preenchimento é obrigatório e se há e-mail ao eliminar/atualizar. |
| `ASSUNTO_FAVORITO` | ecm-documents | COD_EMPRESA, CD_ASSUNTO, CD_MATRICULA | 3 | Assuntos marcados como favoritos por usuário. |
| `CALEND_GLOBAL` | calendario-feriados | ID | 6 | Feriados globais da empresa (entidade FDNHoliday). Cada linha é um feriado de um calendário identificado por COD_FER_CALEND, fixo (dia/mês) ou de um ano específico. |
| `CAMPO_CUSTOM` | ecm-documents | COD_EMPRESA, COD_CAMPO_CUSTOM | 4 | Definição de campos customizados (metadados extras) que podem ser associados a documentos. |
| `COLAB_SUBSTTO` | bpm-workflow | COLLEAGUE_REPLACEMENT_ID | 9 | Configuração de substituição de usuário (delegação): quem é substituído, quem substitui, período e quais tipos de tarefa (GED/workflow) são delegados. |
| `COLAB_SUBSTTO_PROCESSO` | bpm-workflow | COLLEAGUE_PROCESS_ID | 6 | Lista de processos (definições) aos quais uma substituição de usuário se aplica. |
| `COMPON_GRAF_PROCES` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_COMPON_GRAF | 8 | Componentes gráficos (nós do diagrama) de uma versão de definição de processo, com posição e tipo. |
| `CONFIGUR_GRAF_COMPART` | bpm-cap | IDI_TIP_COMPART, CD_MATRICULA, COD_EMPRESA, NUM_SEQ_GRAF, DES_VAL_COMPART | 5 | Compartilhamento de configurações de gráficos CAP (Controle e Acompanhamento de Processos) com usuários, grupos ou papéis. |
| `CONFIGUR_GRAF_USUAR_CAP` | bpm-cap | CD_MATRICULA, COD_EMPRESA, NUM_SEQ | 54 | Configuração de gráficos do CAP (Controle e Acompanhamento de Processos) por usuário: quais métricas/séries exibir, processo analisado e frequência de snapshot. |
| `CONFIGUR_OBRIG_ASSUNTO` | ecm-documents | COD_EMPRESA, CD_ASSUNTO, NUM_SEQ | 6 | Destinatários (usuário/grupo/todos) para os quais o assunto é obrigatório, por sequência. |
| `CONFIGUR_SEGUR_DOCTO` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_SEQ | 11 | Lista de permissões/restrições de segurança por documento e versão: quem (usuário, grupo ou todos) tem qual nível de acesso. |
| `CONHECIMENTO` | ecm-documents | COD_EMPRESA, CD_MATRICULA, NR_DOCUMENTO, NR_VERSAO | 10 | Registro de ciência/consulta de documentos por colaborador: primeira e última visualização de uma versão. |
| `CONTROL_LICENC` | foundation-licenciamento | NUM_SEQ | 4 | Controle de licenciamento do produto: chaves de licença inicial e de emergência e CNPJ licenciado. |
| `DEFAULT_PROPRIED_DOCTO` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NOM_ATRIBUTO | 6 | Propriedades padrão (atributo/valor/formato) associadas a uma versão de documento. |
| `DEF_PROCES` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES | 22 | Definição (cabeçalho) de processo de workflow BPM: dados comuns a todas as versões, como categoria, prazos, notificações e gestor. |
| `DIAGNOSIS_PROCESS_LOG` | bpm-workflow | ID | 9 | Log de auditoria das ações de diagnóstico em processos e instâncias, como troca de versão de script e reenvio. |
| `DOCTO_ALOCAD` | ecm-documents | COD_EMPRESA, NUM_DOCTO_ORIG, NUM_VERS_ORIG, NUM_DOCTO_DEST | 12 | Check-out/alocação de documentos: documento de origem alocado a um colaborador gerando um documento de destino (cópia de trabalho), usado também em edição WebDAV. |
| `DOCTO_ANOTACAO_COLAB` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, NR_ANOTACAO | 11 | Anotações de colaboradores sobre páginas de um documento (posição X/Y, threads via anotação pai). |
| `DOCTO_APLICAT` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, COD_APLICAT | 4 | Associação de documento a aplicativos (N:M documento-aplicativo). |
| `DOCTO_CAMPO_CUSTOM` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, COD_CAMPO_CUSTOM, NR_VERSAO | 5 | Valor de cada campo customizado por versão de documento. |
| `DOCTO_COMENT` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, DTT_CRIAC | 8 | Comentários de colaboradores em uma versão de documento. |
| `DOCTO_CONTDO` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NOM_ARQ_FISIC | 5 | Conteúdo binário (arquivo físico) de uma versão de documento quando armazenado no banco. |
| `DOCTO_DESTAQ_COLAB` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA | 5 | Marcação de "curtir/destacar" um documento por colaborador (DocumentEnjoy). |
| `DOCTO_NOTIF` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, CD_MATRICULA | 3 | Inscrição de colaborador para notificações de alterações em um documento. |
| `DOCTO_OBS_COLAB` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA, DTT_CRIAC | 6 | Observações de colaboradores sobre uma versão de documento. |
| `DOCTO_RANKING` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA | 5 | Nota de avaliação (ranking) dada por colaborador a uma versão de documento. |
| `DOCTO_RELACDO` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_DOCTO_RELACDO | 4 | Relação entre documentos: uma versão de documento aponta para outros documentos relacionados. |
| `DOCTO_SOCIAL` | ecm-documents | COD_EMPRESA, COD_APELIDO, TP_PASTA | 6 | Mapeia pastas sociais (espaços/comunidades) para pastas de documentos, por alias e tipo de pasta. |
| `DOCTO_TAG` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, COD_TAG | 4 | Associação de tags a versões de documento. |
| `DOCUMENTO` | ecm-documents | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO | 75 | Tabela central do ECM: cada linha é uma VERSÃO de um item da árvore de documentos do GED (pasta, arquivo, fichário de formulário, ficha, anexo de processo, link externo etc.), distinguido por TP_DOCUMENTO. |
| `DOCUMENT_ACCUSOFT_METRICS` | ecm-documents | id | 6 | Registro de métricas de uso do visualizador Accusoft (PrizmDoc) por tipo de arquivo: cada linha é um evento de conversão/visualização. |
| `DOC_PROCES` | bpm-workflow | COD_EMPRESA, COD_DOC_PROCES, NUM_VERS | 9 | Diagramas BPMN (XML) publicados de processos, uma linha por versão. |
| `ECM_ABSTRACT_FORM_ITEM` | ecm-metadata-forms | ID | 12 | Tabela base (@Inheritance TABLE_PER_CLASS) dos itens do formulário de metadados do ECM; contém os atributos comuns a todos os tipos de item. |
| `ECM_BUTTON_FORM_ITEM` | ecm-metadata-forms | HTML_ID, METADATAFORM_ID | 18 | Itens do tipo button dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai. |
| `ECM_COLLABORATION` | ecm-collaboration | COLLABORATION_ID | 14 | Sessão de colaboração externa (edição online em app de terceiros, ex. Office365/Google) vinculada a uma versão de documento do ECM. Criada ao iniciar a colaboração. |
| `ECM_COLLABORATION_APP` | ecm-collaboration | ID | 8 | Cadastro dos aplicativos externos de colaboração (provedores de edição online) habilitados por tenant. |
| `ECM_COLLABORATION_GUEST` | ecm-collaboration | COLLABORATION_GUEST_ID | 11 | Participantes (convidados) de uma colaboração externa, com permissão no serviço externo. |
| `ECM_DATE_FIELD_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 19 | Itens do tipo date field dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai. |
| `ECM_DIVIDER_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 15 | Itens do tipo divider dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai. |
| `ECM_DOCTO_LANGUAGE` | ecm-metadata-forms | ID | 4 | Idiomas disponíveis para documentos por tenant (ECM). |
| `ECM_DYNAMIC_TABLE_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 20 | Itens do tipo dynamic table dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai. |
| `ECM_EVALUATION_FIELD_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 19 | Itens do tipo evaluation field dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai. |
| `ECM_EXTERNAL_LINK_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 14 | Itens do tipo external link dos formulários de metadados do ECM (subclasse JPA TABLE_PER_CLASS de AbstractMetadataFormItem); repete as colunas comuns do pai. |
| `ECM_FIXED_TABLE_COLUMN` | ecm-metadata-forms | ID | 6 | Colunas de um item tabela fixa do formulário de metadados. |
| `ECM_FIXED_TABLE_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 13 | Itens do tipo tabela fixa (grid de colunas e linhas pré-definidas) dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_FIXED_TABLE_ROW` | ecm-metadata-forms | ID | 7 | Valores (células) das linhas de um item de tabela fixa de formulário de metadados: cada linha guarda o valor de uma coluna (COLUMN_HTML_ID) em uma linha (ROW_ID). |
| `ECM_IMAGE_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 20 | Itens do tipo imagem dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_LABEL_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 16 | Itens do tipo rótulo de texto estático dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_LIST_FIELD_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 20 | Itens do tipo campo de lista/seleção (combo, lista, checkbox, radio) dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_METADATA_FORM` | ecm-metadata-forms | ID | 8 | Cabeçalho de um formulário de metadados do ECM Fluig (tipo de documento com campos configuráveis, 'metadata form'). Uma linha por versão do formulário, ligada a um documento ECM. |
| `ECM_METADATA_FORM_TRANSLATE` | ecm-metadata-forms | ID | 6 | Traduções (pt, en, es) de textos de um formulário de metadados, indexadas por chave de string. |
| `ECM_NUMBER_FIELD_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 22 | Itens do tipo campo numérico dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_SECTION_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 16 | Itens do tipo seção (agrupador visual com título) dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_TAB_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 15 | Itens do tipo contêiner de abas dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_TAB_ITEM` | ecm-metadata-forms | ID | 6 | Abas individuais de um item de abas (TabMetadataFormItem) em formulário de metadados: título e ordem de cada aba. |
| `ECM_TEXT_AREA_FIELD_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 20 | Itens do tipo campo de texto longo (textarea) dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_TEXT_FIELD_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 22 | Itens do tipo campo de texto curto com máscara dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_TITLE_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 16 | Itens do tipo título dos formulários de metadados (ECM Metadata Form) do Fluig. Uma linha por item posicionado em um formulário. |
| `ECM_UPLOAD_FILE_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 18 | Subclasse (JPA TABLE_PER_CLASS) de ECM_ABSTRACT_FORM_ITEM para itens de upload de arquivo em formularios de metadados do ECM. Cada linha e um campo de anexo de um formulario. |
| `ECM_ZOOM_DISPLAY_FIELD` | ecm-metadata-forms | ID | 7 | Campos do dataset exibidos na janela de pesquisa de um item Zoom de formulario de metadados (colunas de exibicao/pesquisa). |
| `ECM_ZOOM_FIELD_FORM_ITEM` | ecm-metadata-forms | METADATAFORM_ID, HTML_ID | 25 | Subclasse de ECM_ABSTRACT_FORM_ITEM para itens Zoom (selecao de registro de um dataset) em formularios de metadados do ECM. |
| `ECM_ZOOM_FILTER_FIELD` | ecm-metadata-forms | ID | 5 | Filtros fixos (campo=valor) aplicados ao dataset consultado por um item Zoom de formulario de metadados. |
| `ECM_ZOOM_OUTPUT_FIELD` | ecm-metadata-forms | ID | 5 | Mapeia um campo (DISPLAY_KEY) do dataset do zoom para outro item do formulario (HTML_ID) que sera preenchido quando um registro e selecionado. |
| `ECM_ZOOM_USER_FORM_ITEM` | ecm-metadata-forms | HTML_ID, METADATAFORM_ID | 26 | Subclasse de ECM_ABSTRACT_FORM_ITEM para itens Zoom de usuario (selecao de usuarios) em formularios de metadados do ECM. |
| `ESTADO_PROCES` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ | 50 | Estado/atividade (nó do fluxo BPM) de uma versão de definição de processo: tarefas, gateways, eventos, subprocessos e fim, com prazos, notificações, atribuição e posição no diagrama (entidade ProcessState). |
| `ESTADO_PROCES_COND` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ, NUM_SEQ_ORD_FORMUL | 10 | Condições de decisão (saídas) associadas a um estado automático/gateway: expressão ou mapa de regras que determina o estado de destino (entidade ConditionProcessState). |
| `ESTADO_PROCES_SCRIPT` | bpm-workflow | COD_EMPRESA, NUM_SEQ_CONDITION, COD_DEF_PROCES, NUM_SEQ, NUM_VERS | 6 | Script de condição (nome de arquivo/identificador) associado a um estado de evento condicional (ProcessStateConditionScript). |
| `ESTADO_PROCES_SERVICE` | bpm-workflow | PROCESS_STATE_SERVICE_ID | 10 | Configuração de serviço (integração) executado por um estado de tarefa de serviço: nome do serviço, tentativas e frequência (ProcessStateService). |
| `ESTADO_PROCES_SIGNAL` | bpm-workflow | COD_EMPRESA, NUM_SEQ_CONDITION, COD_DEF_PROCES, NUM_SEQ, NUM_VERS | 6 | Vínculo entre um estado de evento condicional/sinal e um sinal BPMN (ProcessStateConditionSignal). |
| `ESTADO_PROCES_TRIGGER` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ, NUM_SEQ_TRIGGER | 12 | Gatilhos (timers/eventos) de um estado: agendamento, frequência e valor de disparo para eventos iniciais/intermediários de timer (ProcessStateTrigger). |
| `EVENT_FICHA` | bpm-workflow | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, COD_EVENT | 6 | Script de evento (JavaScript) de um formulário/ficha, por documento e versão (CardEvent). |
| `EVENT_GERAL` | bpm-workflow | COD_EMPRESA, COD_EVENT | 3 | Eventos globais (scripts JavaScript) disponíveis a todo o ambiente do tenant, ex.: eventos globais de workflow (GlobalEvent). |
| `EVENT_PROCES` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, COD_EVENT, SCRIPT_VERSION | 8 | Scripts de evento (JavaScript) de uma versão de processo, com histórico de versões do script (WorkflowProcessEvent). |
| `FACT_ACTIVITY_COST_CAP` | bpm-analytics-dw | ACTIVITYID, COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID | 31 | Fato de custo, esforço e prazo por atividade, dia e usuário (planejado/baseline vs realizado), separado por tarefas abertas, concluídas e canceladas. |
| `FACT_ACTIVITY_VOLUME_CAP` | bpm-analytics-dw | ACTIVITYID, COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID | 17 | Fato de volume de tarefas por atividade, dia e usuário: abertas/concluídas/canceladas, dentro/fora do prazo. |
| `FACT_FLOW_VOLUME_CAP` | bpm-analytics-dw | COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, SOURCEACTIVITY, TARGETACTIVITY, USERSEQUENCE, YEARID | 14 | Fato de volume de transições entre atividades (fluxos normais vs retornos) por dia e usuário. |
| `FACT_PROCES_COST_CAP` | bpm-analytics-dw | COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID | 23 | Fato de custo/esforço por processo, dia e usuário (baseline vs realizado) para processos abertos, concluídos e cancelados. |
| `FACT_PROCES_VOLUME_CAP` | bpm-analytics-dw | COMPANYID, DAYID, MONTHID, PROCESSID, PROCESSVERSION, USERSEQUENCE, YEARID | 14 | Fato de volume de processos por dia e usuário: em aberto/concluídos dentro e fora do prazo, cancelados e aberturas. |
| `FAVORITOS` | ecm-lists-filters | COD_EMPRESA, CD_MATRICULA, NR_DOCUMENTO | 3 | Documentos marcados como favoritos por usuário. |
| `FAVORITOS_PROCES` | ecm-lists-filters | COD_EMPRESA, CD_MATRICULA, COD_DEF_PROCES | 3 | Processos (definições) marcados como favoritos por usuário. |
| `FDN_ACCESSLOG` | seguranca-auditoria | ACCESSLOG_ID | 9 | Log de acessos (login/logout) à plataforma Fluig por usuário, com IP do cliente, IP do servidor e agente. Recebe uma linha por evento de acesso. |
| `FDN_ALERT` | foundation-alert | ID | 8 | Alerta/notificacao da central de alertas do Fluig destinado a um usuario (receiver), ligado a um tipo de evento, a um objeto e a um local. |
| `FDN_ALERTACTION` | foundation-alert | ID | 10 | Acoes executaveis associadas a um alerta (ex.: aprovar, abrir link), com descricao i18n e integracao opcional via JMS/HTTP. |
| `FDN_ALERTAPPSENDER` | foundation-alert | ID | 8 | Aplicacao/canal emissor de alertas registrado por tenant (ex.: central Fluig, e-mail, mobile), com JNDI do destino de entrega. |
| `FDN_ALERTCONFIG` | foundation-alert | ID | 6 | Preferencia de recebimento de alertas: para um tenant/usuario, evento e canal, define se o alerta e recebido (ligado/desligado/bloqueado). |
| `FDN_ALERTEVENTTYPE` | foundation-alert | ID | 14 | Catalogo de tipos de evento de alerta (ex.: tarefa atribuida) por tenant e modulo, com chaves i18n e regras de agrupamento/remocao. |
| `FDN_ALERTMETADATA` | foundation-alert | ID | 4 | Pares chave/valor extras anexados a um alerta (parametros usados para montar a mensagem/link). |
| `FDN_ALERTMODULE` | foundation-alert | ID | 4 | Modulo/aplicacao do Fluig que agrupa tipos de evento de alerta, por tenant. |
| `FDN_ALERTOBJECT` | foundation-alert | ID | 8 | Objeto de negocio (documento, tarefa, etc.) referenciado por um alerta, tanto como alvo (OBJECT_ID) quanto como local (PLACE_ID). |
| `FDN_ALERTSENDER` | foundation-alert | ID | 5 | Registra quem enviou/originou um alerta (usuario remetente) e por qual via. |
| `FDN_API_BLOCKER` | seguranca-api | API_BLOCKER_ID | 3 | Padrões de URL/API bloqueados pelo filtro bloqueador de APIs do Fluig, com exceções. Cada linha é um padrão de bloqueio. |
| `FDN_AUTHORIZECLIENTDATA` | oauth-integracao | AUTHORIZECLIENTDATA_ID | 23 | Configuração de cliente de autenticação/autorização para consumir serviços externos (credenciais, URLs e tokens OAuth), por tenant e código. |
| `FDN_BUNDLEVALUE` | i18n | BUNDLE_VALUE_ID | 5 | Valores traduzidos de resource bundles (i18n) por bundle, chave e locale. Cada linha é uma tradução de uma chave. |
| `FDN_CATEGORY` | permissoes-categorias | CATEGORY_ID | 9 | Categorias hierárquicas usadas para agrupar recursos (FDN_RESOURCE) no modelo de permissões. Cada linha é uma categoria, possivelmente filha de outra. |
| `FDN_CATEGORY_RESOURCE` | permissoes-categorias | CATEGORY_RESOURCE_ID | 4 | Tabela de associação entre categorias (FDN_CATEGORY) e recursos (FDN_RESOURCE). Cada linha vincula um recurso a uma categoria. |
| `FDN_DATASETHISTORY` | datasets | DATASET_HISTORY_ID | 11 | Histórico de versões de datasets customizados (implementação JavaScript). Cada linha é uma versão de um dataset. |
| `FDN_DIGITALSIGNATURE` | assinatura-digital | DIGITAL_SIGNATURE_ID | 4 | Configuração de assinatura digital por tenant: tipo de assinatura e número de licenças. Uma linha por tenant licenciado. |
| `FDN_DOWNLOADNOTIFY` | volumes-sites | DOWNLOADNOTIFY_ID | 3 | Usuários a notificar quando um item da fila de download de site (FDN_SITEDOWNLOADQUEUE) concluir. Liga item da fila a usuário. |
| `FDN_FLUIG_SERVER` | integracao-servidores | ID | 3 | Servidores Fluig cadastrados (outras instâncias Fluig conectadas), cada um com credenciais OAuth em FDN_AUTHORIZECLIENTDATA. |
| `FDN_GROUP` | foundation-identity-access | GROUP_ID | 6 | Grupo de usuários do Fluig (de usuários, cloud ou comunidade), por tenant. Usado em permissões, papéis e agrupamento de usuários. |
| `FDN_GROUPDATA` | foundation-identity-access | GROUPDATA_ID | 4 | Propriedades chave/valor adicionais de um grupo (FDN_GROUP). |
| `FDN_GROUPUSERROLE` | foundation-identity-access | GROUPUSERROLE_ID | 6 | Tabela de associação de membros de grupo: liga um grupo a um usuário (LOGIN), a um papel (ROLE_CODE) ou a um subgrupo (CHILD_GROUPCODE). |
| `FDN_IDENTITYPARTNER` | foundation-identity-access | ID | 11 | Parceiro de identidade/licenciamento do tenant: guarda credenciais de cliente, licença e quantidade de usuários licenciados. |
| `FDN_INTEGRATION` | integracao-eventos | INTEGRATION_ID | 3 | Componentes de integração registrados (bean/EJB por nome JNDI) que recebem eventos de integração, ordenados por prioridade. |
| `FDN_INTEGRATIONEVENT` | integracao-eventos | INTEGRATIONEVENT_ID | 4 | Eventos de integração que cada integração (FDN_INTEGRATION) declara tratar. Cada linha é um nome de evento. |
| `FDN_INTEGRATIONLISTENEREVT` | integracao-eventos | INTEGRATION_LISTENER_EVT_ID | 5 | Listeners externos registrados para eventos de integração, com informações de conexão síncrona e assíncrona. |
| `FDN_JAASUSERGROUP` | seguranca | JAAS_USERGROUP_ID | 3 | Associação login-grupo JAAS usada pela camada de segurança do app server. |
| `FDN_LITERAL` | i18n | LITERAL_ID | 8 | Literais (textos da interface) por produto e locale, com valor original e valor customizado pelo cliente. |
| `FDN_LOCAL` | calendario-feriados | ID | 8 | Locais (unidades/filiais) com coordenadas geográficas, raio e fuso horário, usados para associar feriados e usuários. Pode haver um local padrão por empresa. |
| `FDN_LOCALHOLIDAY` | calendario-feriados | ID | 4 | Associação entre local (FDN_LOCAL) e feriado global (CALEND_GLOBAL): feriados que valem para cada local. |
| `FDN_LOCALUSER` | calendario-feriados | ID | 4 | Associação de usuários a locais (FDN_LOCAL). Cada linha vincula um código de usuário a um local. |
| `FDN_LOCK` | concorrencia-lock | TENANT_ID, FEATURE_TYPE, ITEM_ID | 4 | Locks distribuídos de recursos: indica que um item de uma funcionalidade está bloqueado por uma instância/sessão (UUID). |
| `FDN_OAUTHAPP` | oauth-provider | OAUTH_APP_ID | 7 | Aplicação (consumidor) OAuth registrada no Fluig, com consumer key/secret e provedor. |
| `FDN_OAUTHAPPDATA` | oauth-provider | OAUTH_APP_DATA_ID | 4 | Propriedades extras chave/valor de uma aplicação OAuth. |
| `FDN_OAUTHAPPTOKEN` | oauth-provider | OAUTH_APP_TOKEN_ID | 9 | Tokens OAuth (request/access) emitidos para uma aplicação OAuth, com data de criação e expiração. |
| `FDN_OAUTHAPPUSER` | oauth-provider | OAUTH_APP_USER_ID | 4 | Autorização de um usuário (login) a uma aplicação OAuth, ligando ao token emitido. |
| `FDN_OAUTHPROVIDER` | oauth-provider | OAUTH_PROVIDER_ID | 10 | Provedor OAuth (URLs de request/access/autorização e método de assinatura), por tenant. |
| `FDN_PARAMGERAL` | configuracao-parametros | PARAMGERAL_ID | 4 | Parâmetros gerais de configuração em pares chave/valor, por tenant (ou globais quando TENANT_ID é nulo). |
| `FDN_PDATATRACE` | privacy-lgpd | PDATATRACE_ID | 11 | Rastro de acesso/alteração de dados pessoais (LGPD): quem, quando, qual recurso e campos. |
| `FDN_PDATATRACE_CONFIG` | privacy-lgpd | PDATATRACE_CONFIG_ID | 4 | Configuração do rastreamento de dados pessoais por tenant: ativo e retenção em dias. |
| `FDN_PDATA_CLASSIFICATION` | privacy-lgpd | PDATA_CLASSIFICATION_ID | 2 | Catálogo de classificações de dados pessoais (base legal/categoria) usado nas justificativas LGPD. |
| `FDN_PDATA_INFOTYPE` | privacy-lgpd | INFORMATION_TYPE_ID | 2 | Catálogo de tipos de informação de dados pessoais (ex.: identificação, contato) usados em FDN_PERSONALDATA. |
| `FDN_PDATA_JUSTIFICATION` | privacy-lgpd | PDATA_JUSTIFICATION_ID | 4 | Justificativa de tratamento de um dado pessoal cadastrado, associada a uma classificação. |
| `FDN_PERMISSION` | foundation-identity-access | PERMISSION_ID | 8 | Concessão de permissão sobre um recurso (FDN_RESOURCE) a um usuário, grupo ou papel. |
| `FDN_PERMISSION_MAPPING` | foundation-identity-access | PERMISSION_MAPPING_ID | 6 | Mapeamento entre permissões: ter PERMISSION em RESOURCE_CODE implica/concede TO_PERMISSION em TO_RESOURCE_CODE. |
| `FDN_PERSONALDATA` | privacy-lgpd | PERSONALDATA_ID | 14 | Catálogo de dados pessoais por tenant: tabela e campo que contêm dado pessoal, sensibilidade e se permitem anonimização. |
| `FDN_PRODUCT` | foundation-tenancy | PRODUCT_ID | 3 | Catálogo de produtos TOTVS/Fluig que podem ser habilitados para um tenant. |
| `FDN_PUSH` | mobile-push | PUSH_ID | 13 | Registros de dispositivos móveis para notificações push: tokens de acesso, de canal e de dispositivo por usuário OAuth/aplicativo. |
| `FDN_RECENTLY_VIEWED` | acesso-recente | RECENTLY_VIEWED_ID | 9 | Itens vistos recentemente por usuário (documento, instância de processo ou página), para o atalho de recentes. |
| `FDN_REQUEST_NONCE` | seguranca | REQUEST_NONCE_ID | 6 | Nonces de requisições para prevenção de replay e rastreio de status/falha. |
| `FDN_RESOURCE` | foundation-identity-access | RESOURCE_ID | 9 | Recurso protegido por permissão (tela, serviço, documento, método de API etc.), organizado em hierarquia e classificado por tipo. |
| `FDN_RESOURCETYPE` | foundation-identity-access | RESOURCE_TYPE_ID | 4 | Tipos de recurso protegível (categorias de FDN_RESOURCE). |
| `FDN_RESOURCETYPEPERMISSION` | foundation-identity-access | RESOURCE_PERMISSION_ID | 4 | Catálogo das permissões possíveis para cada tipo de recurso. |
| `FDN_RESTORE_PERMISSION_MAPPING` | foundation-identity-access | ID | 4 | Backup em XML das permissões de um recurso, usado para restaurar permissões. |
| `FDN_ROLE` | foundation-identity-access | ROLE_ID | 5 | Papel (role) de segurança do tenant, atribuído a usuários e grupos. |
| `FDN_ROLEDATA` | foundation-identity-access | ROLEDATA_ID | 4 | Propriedades chave/valor adicionais de um papel (FDN_ROLE). |
| `FDN_SERVER_INFO` | infraestrutura-servidor | DATA_ID | 5 | Informações de diagnóstico publicadas por instâncias do servidor Fluig (nome, IP e valor da informação) em data de inserção. |
| `FDN_SERVICE_OPERATION` | foundation-dataservice | OPERATION_ID | 9 | Operação de serviço de dados (Data Service) configurável por tenant: descritor e implementação de uma operação de um serviço. |
| `FDN_SITE` | volumes-sites | SITE_ID | 9 | Sites (servidores/sites de volume) usados na replicação e download de arquivos, com URL, limites de cópia e stream e tentativas máximas. |
| `FDN_SITEDOWNLOADQUEUE` | volumes-sites | QUEUE_ID | 16 | Fila de downloads de arquivos de documentos entre sites. Cada linha é uma transferência de uma versão de documento para o site do usuário. |
| `FDN_SITESCHEDULER` | foundation-platform | SITESCHEDULER_ID | 4 | Janelas de agendamento (início/fim) associadas a um site do Fluig; usada por consulta FDNSiteScheduler.findBySite. |
| `FDN_TENANT` | foundation-tenancy | TENANT_ID | 12 | Tenant (empresa/organização) do Fluig; raiz da multi-tenancy, referenciada por quase todas as tabelas. |
| `FDN_TENANTDATA` | foundation-tenancy | TENANTDATA_ID | 5 | Parâmetros/propriedades chave/valor de configuração do tenant. |
| `FDN_TENANTPRODUCT` | foundation-tenancy | TENANTPRODUCT_ID | 3 | Associação tenant-produto: quais produtos (FDN_PRODUCT) estão habilitados em cada tenant. |
| `FDN_UPDATE_HOTFIX` | foundation-platform | id | 4 | Registro de updates/hotfixes aplicados à instalação do Fluig, com código, data de criação e usuário que aplicou. |
| `FDN_USER` | foundation-identity-access | USER_ID | 8 | Pessoa/usuário global do Fluig (dados pessoais independentes de tenant); o vínculo com cada tenant está em FDN_USERTENANT. |
| `FDN_USERDATA` | foundation-identity-access | USERDATA_ID | 7 | Propriedades chave/valor adicionais do vínculo usuário-tenant (perfil e preferências). |
| `FDN_USERLOGGING` | foundation-identity-access | USERLOGGING_ID | 4 | Registro de usuário logado/sessão com data de vencimento (due date), por login e tenant. |
| `FDN_USERMOBILETOKEN` | mobile | USER_IDIDP | 6 | Tokens de acesso/refresh do app mobile por usuário do IdP. |
| `FDN_USERPICTURE` | foundation-identity-access | USERPICTURE_ID | 3 | Foto/avatar do usuário (referência ao arquivo da imagem) por vínculo usuário-tenant. |
| `FDN_USERROLE` | foundation-identity-access | USERROLE_ID | 4 | Atribuição de papéis (FDN_ROLE) a usuários por tenant. |
| `FDN_USERTENANT` | foundation-identity-access | USER_TENANT_ID | 16 | Vínculo do usuário (FDN_USER) com um tenant: contém login, e-mail, senha, estado e identificadores usados na autenticação. |
| `FDN_USERTOKEN` | seguranca | USERTOKEN_ID | 9 | Tokens temporários enviados por e-mail a usuários para liberar recursos (ex.: acesso por link), com limite de uso e status. |
| `FDN_USERTOKENRESOURCE` | seguranca | USERTOKENRESOURCE_ID | 4 | Recursos (hoje apenas URLs) liberados por um token de usuário. |
| `FDN_VOLUME` | foundation-platform | VOLUME_ID | 7 | Volumes de armazenamento de arquivos (GED/documentos) por tenant, com capacidade máxima e espaço usado. |
| `FDN_VOLUMESITE` | foundation-platform | VOLUMESITE_ID | 4 | Associa um volume de armazenamento a um site, informando o caminho físico (STORAGE) usado por esse site naquele volume. |
| `FICHA` | ecm-forms | COD_EMPRESA, NR_FICHA, NR_VERSAO, COD_TABELA, COD_CAMPO | 7 | Valores dos campos das fichas (registros de formulário/fichário): uma linha por campo de cada ficha, versão e tabela do formulário. |
| `FICHARIO` | ecm-forms | COD_EMPRESA, NR_FICHARIO, NR_VERSAO, COD_TABELA | 5 | Definição das tabelas de um fichário (formulário): cada fichário tem uma tabela principal e, opcionalmente, tabelas filhas (pai-e-filho). |
| `FICHARIO_CAMPO` | ecm-forms | COD_EMPRESA, COD_CAMPO, NR_FICHARIO, COD_TABELA, NR_VERSAO | 6 | Definição dos campos de cada tabela de um fichário (formulário): nome e tipo do campo. |
| `FICHARIO_CAMPO_PROCES` | bpm-forms | COD_EMPRESA, COD_CAMPO, COD_DEF_PROCES | 5 | Mapeia campos do formulário a um processo: descrição e posição (slot) de campos exibidos/indexados para a definição de processo. |
| `FIELD` | social-forms | id | 11 | Campo de formulário analisado pela camada social/forms (controle de enquete/formulário social), com tipo, rótulo e obrigatoriedade. Pode ter campo pai (hierarquia). |
| `FILTERS` | ecm-lists-filters | ID | 7 | Filtros salvos pelos usuários nas listas de documentos ou de processos (tarefas), com tipo DOCUMENT ou PROCESS. |
| `FILTER_FIELDS` | ecm-lists-filters | ID | 16 | Campos/critérios e opções de exibição (cor, fonte, largura, visibilidade) de um filtro salvo. |
| `FILTER_GROUP` | ecm-lists-filters | ID | 6 | Compartilhamento de um filtro com grupo, papel ou usuário, com permissão. |
| `FILTER_ORDER` | ecm-lists-filters | ID | 4 | Critérios de ordenação de um filtro salvo, apontando para um FILTER_FIELDS. |
| `FLOW_DIM_CAP` | bpm-analytics-dw | COMPANYID, PROCESSID, PROCESSVERSION, SOURCEACTIVITY, TARGETACTIVITY | 8 | Dimensão de fluxos (transições origem->destino entre atividades) de cada versão de processo. |
| `FLUIG_AUDIT` | audit | AUDIT_ID | 10 | Trilha de auditoria de ações de usuários sobre recursos do Fluig (criar, editar, remover etc.). |
| `FLUIG_AUDIT_CONFIG` | audit | AUDIT_CONFIG_ID | 4 | Configuração de auditoria por tenant: habilita/desabilita e define retenção em dias. |
| `FLUIG_METRIC` | monitoring-metrics | METRIC_ID | 4 | Métricas de uso agregadas por dia: nome da métrica e contagem. |
| `FLUIG_RUNTIMEDATA_PROCESS_MNGR` | bpm-workflow | DATA_KEY | 2 | Armazenamento chave/valor de dados de runtime do gerenciador de processos (BPM); sem entidade JPA no código. |
| `FORM_DATASET` | bpm-workflow | FORM_DATASET_ID | 5 | Associa um formulário (documento/versão) a datasets usados por ele (FormDataset). |
| `HISTOR_ACES` | bpm-workflow | COD_EMPRESA, CD_MATRICULA, DAT_ACES, NR_DOCUMENTO | 4 | Histórico de acessos de usuários a documentos por dia (AccessLog). |
| `HISTOR_CONVER` | bpm-workflow | COD_EMPRESA, NUM_SEQ_CONVER | 8 | Histórico de conversões de instâncias de processo de uma versão de definição para outra (ConversionHistory). |
| `HISTOR_CONVER_ESTADO` | bpm-workflow | COD_EMPRESA, NUM_SEQ_CONVER, NUM_SEQ_ESTADO | 4 | Mapeamento de estados na conversão: estado de origem x estado de destino por conversão (ConversionHistoryState). |
| `HISTOR_PROCES` | bpm-workflow | COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO | 17 | Histórico de movimentações de uma instância de processo: cada passagem entre estados, com datas, links seguidos, thread e versão da definição (ProcessHistory). |
| `HISTOR_TRANSF_PENDCIA` | bpm-workflow | COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, CD_MATRICULA, NUM_SEQ_TRANSF, SEQ_MOVTO | 9 | Histórico de transferências de pendências (tarefas) entre usuários (PendencyTransferHistory). |
| `I18N_BUNDLE` | i18n | BUNDLE_ID | 2 | Bundle de internacionalização: agrupador de locales e literais traduzidos identificado por código. |
| `I18N_LITERAL_TRANSLATED` | i18n | LITERAL_TRANSLATED_ID | 5 | Tradução de um literal (chave) para um locale específico. |
| `I18N_LOCALE` | i18n | LOCALE_ID | 4 | Locales (idiomas) disponíveis em um bundle, com indicação do padrão. |
| `I18N_RELATED_BUNDLE` | i18n | RELATED_BUNDLE_ID | 3 | Lista os bundles relacionados (por código) a um bundle, para herança/fallback de literais. |
| `ICONE` | bpm-workflow | COD_EMPRESA, NR_ICONE | 6 | Cadastro de ícones associados a extensões/tipos MIME de arquivos exibidos no GED (Icon). |
| `LINK_DOCTO_VIRTUAL` | ecm-documents | COD_EMPRESA, NR_DOCTO_PAI_CORREN, NR_DOCUMENTO | 5 | Links virtuais (atalhos): um documento aparece em uma pasta adicional sem ser copiado. |
| `LINK_PROCES` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_LINK | 17 | Link (transição/seta) entre dois estados do fluxo de uma versão de processo, com rótulos, tipo e flags de fluxo (ProcessLink). |
| `LINK_PROCES_ASSOC` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_LINK | 6 | Associação de um link do processo a um componente gráfico (nota, documento, banco de dados) do diagrama (ProcessLinkAssoc). |
| `LINK_PROCES_BEND` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ_LINK, NUM_SEQ_CURV | 7 | Pontos de curva (dobras) do desenho de um link no diagrama (ProcessLinkBend). |
| `LIN_PROCES` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ | 12 | Raias (swimlanes), pools e grupos do diagrama de uma versão de processo (SwimLane). |
| `LOCK_RESOURCE` | document-management | COD_EMPRESA, TOKEN_ID | 7 | Trava (lock) de recurso por usuário/sessão para edição exclusiva (LockResource). |
| `LOG_ACESSO` | security-audit | COD_EMPRESA, CD_MATRICULA, DAT_CLIEN_SERVID, DES_CLIEN_IP | 6 | Log de acessos (login/logout/timeout/erro) de usuários, com IPs de cliente e servidor (LogAccess). |
| `LOG_COP_CONTROLAD` | ecm-documentos | NUM_PROTOC, COD_EMPRESA | 11 | Log de emissao de copias controladas (impressao controlada) de documentos do GED. Cada linha registra protocolo, documento/versao, area, emissor e impressora. |
| `LS_METRIC` | monitoring-metrics | METRIC_ID | 4 | Cabeçalho de métricas de uso do License Server por tenant, identificando rotina e sub-rotina medidas. |
| `LS_METRIC_DETAIL` | monitoring-metrics | METRIC_DETAIL_ID | 7 | Medições individuais (código, valor, instante) de métricas do License Server, com marca de processamento. |
| `MAILEVENTTEMPLATE` | mail | id | 6 | Mapeia eventos de e-mail do Fluig a templates por tenant, dialeto (idioma) e nome de template, com assunto. |
| `MARCA_DAGUA` | ecm-documents | COD_EMPRESA, NR_MARCA_DAGUA | 18 | Cadastro de marcas d'água (texto, fonte, cor, alinhamento) aplicáveis a documentos na visualização/download. |
| `MECAN_ATRIBUIC` | bpm-workflow | COD_EMPRESA, COD_MECAN_ATRIBUIC | 9 | Cadastro de mecanismos de atribuicao do workflow (quem recebe a tarefa de uma atividade). Inclui mecanismos padrao e customizados com classes de configuracao/controle. |
| `MENTION` | social | id | 8 | Menção (@usuário) feita em um objeto social (post/comentário); liga o autor ao perfil social mencionado. |
| `META_LISTA` | ecm-lists-filters | COD_EMPRESA, COD_LISTA | 6 | Cabeçalho de meta-lista: lista dinâmica de dados definida pelo usuário (tabelas customizadas de metadados do ECM). |
| `META_LISTA_CAMPO` | ecm-lists-filters | COD_EMPRESA, COD_LISTA, NUM_SEQ_CAMPO | 10 | Campos (colunas) de uma meta-lista, com título, tipo, obrigatoriedade e lista estrangeira. |
| `META_LISTA_PERSPECT` | ecm-lists-filters | COD_EMPRESA, COD_LISTA, COD_PERSPECT | 5 | Perspectivas (visões salvas) de uma meta-lista. |
| `META_LISTA_PERSPECT_CAMPO` | ecm-lists-filters | COD_EMPRESA, COD_LISTA, COD_PERSPECT, NUM_SEQ_CAMPO | 7 | Campos incluídos em uma perspectiva da meta-lista, com ordem e indicação de agrupador. |
| `META_LISTA_PERSPECT_FILTRO` | ecm-lists-filters | COD_EMPRESA, COD_LISTA, COD_PERSPECT, COD_FILTRO | 7 | Filtros (campo, condição, valor) aplicados a uma perspectiva de meta-lista. |
| `META_LISTA_REL` | ecm-lists-filters | COD_EMPRESA, COD_LISTA_PAI, COD_LISTA_FILHO | 4 | Relacionamentos mestre-detalhe entre meta-listas. |
| `META_LIST_EVENT` | ecm-lists-filters | COD_EMPRESA, COD_LISTA, COD_EVENT | 4 | Scripts de evento (JavaScript) associados a uma meta-lista. |
| `MOVTO_APROVAC` | ecm-documentos | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_SEQ_ITERAC, NUM_NIV_APROVAC, NUM_SEQ_MOVTO | 15 | Movimentos de aprovacao de documentos do GED: cada acao (analise, aprovacao, assinatura) de um aprovador numa iteracao e nivel de aprovacao de uma versao. |
| `NIVEL_APROVACAO` | ecm-documentos | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, NUM_NIV_APROVAC | 6 | Niveis de aprovacao configurados para uma versao de documento do GED, com modo de aprovacao e descricao do nivel. |
| `PARAM_APLICAT` | bpm-workflow | COD_EMPRESA, COD_APLICAT, NOM_PARAM | 7 | Parametros de configuracao de aplicativos (cadastro APLICATIVO) por tenant: nome, tipo, valor padrao e se pode variar por usuario. |
| `PARAM_APLICAT_USUAR` | bpm-workflow | COD_EMPRESA, CD_MATRICULA, NOM_PARAM, COD_APLICAT | 5 | Valor de parametro de aplicativo especifico de um usuario, sobrepondo o valor padrao de PARAM_APLICAT. |
| `PENDCIA_NOTIF_EMAIL` | bpm-workflow | COD_EMPRESA, NUM_SEQ | 12 | Fila de e-mails de notificacao pendentes de envio (assunto, corpo, remetente, destinatarios e template). |
| `PERIOD_EXPED` | bpm-workflow | COD_EMPRESA, COD_PERIOD_EXPED, NUM_DIA_PERIOD, NUM_SEQ_PERIOD | 6 | Periodos de expediente: faixas de horas uteis por dia da semana, usadas no calculo de prazos de workflow. |
| `POLICYDOCUMENT` | use-policy | id | 5 | Documento de política de uso (termos) em um idioma, com versão de documento, flag de padrão e exigência de consentimento. |
| `POLICYDOCUMENT_POLICYUSER` | use-policy | POLICYDOCUMENT_ID, USERSACCEPTED_ID | 2 | Tabela de junção JPA (@OneToMany usersAccepted) entre documento de política e aceites de usuário. |
| `POLICYUSER` | use-policy | id | 6 | Registro de aceite/resposta de um usuário a uma versão de documento de política de uso. |
| `PREFER_PASTA` | ecm-lists-filters | COD_EMPRESA, NR_DOCUMENTO, NR_VERSAO, CD_MATRICULA | 5 | Preferência de classificação (ordenação) de conteúdo de uma pasta por usuário. |
| `PROCESS_APP_CONFIG` | bpm-workflow | id | 8 | Configuracao de mapeamento de campos de aplicativo por atividade de processo (APP_FIELD/APP_KEY) definida na modelagem do processo. |
| `PROCESS_APP_VALUE` | bpm-workflow | id | 7 | Valores em runtime de campos de aplicativo por instancia e movimentacao de processo. |
| `PROCESS_ATTACHMENT_RULES` | bpm-workflow | id | 9 | Regras de validacao de anexos por atividade de processo (operador, quantidade, nome do anexo e mensagem de erro). |
| `PROCESS_COND_AUTOMATIC_RULES` | bpm-workflow | ID | 11 | Condicoes das regras de transicao automatica de atividade (campo, operador, valor), agrupadas por expressao e ordem. |
| `PROCESS_CUSTOM_TRANSLATE` | bpm-workflow | id | 7 | Traducoes customizadas (chave/descricao) por idioma de uma versao de processo. |
| `PROCESS_DEFINITION_TRANSLATE` | bpm-workflow | id | 7 | Traducao por idioma de descricao, instrucao e categoria da definicao de processo. |
| `PROCESS_ELEMENT_TRANSLATE` | bpm-workflow | id | 13 | Traducao por idioma de elementos (atividades) do processo: nome, rotulos de acao, titulo/descricao de movimentacao e instrucao. |
| `PROCESS_FORM_MAP` | bpm-workflow | FORM_MAP_ID | 9 | Mapeamento de campos de formulario entre processo pai e subprocesso, por atividade. |
| `PROCESS_INSTANCE_MANAGER` | bpm-workflow | id | 5 | Cache de usuarios gestores/participantes associados a uma instancia de processo, com data de cache. |
| `PROCESS_OBSERVATION` | bpm-workflow | OBSERVATION_ID | 14 | Observacoes e historico de anexos de uma instancia de processo, por atividade/thread/movimentacao (informacao, erro, inclusao/alteracao/exclusao de anexo). |
| `PROCESS_VERSION_TRANSLATE` | bpm-workflow | id | 9 | Traducao por idioma e versao de descricao, instrucao, instrucao de versao e categoria do processo. |
| `PROCES_SIGNAL` | bpm-workflow | COD_EMPRESA, COD_SINAL | 3 | Cadastro de sinais (eventos de sinal BPMN) que processos podem emitir e aguardar. |
| `PROCES_SIGNAL_INSTANCE` | bpm-workflow | COD_EMPRESA, COD_SINAL, COD_SINAL_INSTANCE | 8 | Ocorrencias de sinal emitidas por instancias de processo, com dados do sinal e atividade de origem. |
| `PROCES_SIGNAL_RECEIVERS` | bpm-workflow | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ, COD_SINAL, NUM_PROCES, NUM_SEQ_THREAD | 9 | Receptores de sinal: threads de instancias de processo aguardando um sinal em uma atividade de captura. |
| `PROCES_VERSION_DIM_CAP` | bpm-analytics-dw | COMPANYID, PROCESSID, PROCESSVERSION | 9 | Dimensão de versões de processos com a janela de vigência (início/fim em dia/mês/ano). |
| `PROCES_WORKFLOW` | bpm-workflow | COD_EMPRESA, NUM_PROCES | 24 | Instancia (solicitacao) de processo de workflow: dados de abertura, solicitante, prazo, status e vinculo com a versao da definicao e com o formulario. |
| `PROCES_WORKFLOW_ERROR_LOG` | bpm-workflow-erro | ID | 10 | Log de falhas ocorridas em operações assíncronas/de movimentação do workflow (envio, cancelamento, mover, timer etc.), guardando o payload serializado para reprocessamento e o stack trace. |
| `PROFANITY` | social | id | 4 | Configuração do filtro de palavrões da rede social por tenant: liga/desliga e lista de palavras proibidas. |
| `PROPRIED_AVANCAD_PROCES` | bpm-definicao-processo | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, COD_PROPRIED | 5 | Propriedades avançadas (chave/valor) de uma versão de definição de processo, configuradas no modelador. |
| `PROPRIED_EXT` | bpm-process-definition | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ, COD_PROPRIED | 9 | Propriedades estendidas (nome/valor) de estados/atividades de uma definição de processo (BPM), por versão. |
| `QRTZ_BLOB_TRIGGERS` | scheduler-quartz | TRIGGER_GROUP, TRIGGER_NAME | 3 | Tabela padrão do Quartz para triggers de tipo customizado serializados em BLOB. |
| `QRTZ_CALENDARS` | scheduler-quartz | CALENDAR_NAME | 2 | Calendários Quartz serializados que excluem períodos de disparo de triggers. |
| `QRTZ_CRON_TRIGGERS` | scheduler-quartz | TRIGGER_GROUP, TRIGGER_NAME | 4 | Detalhe de triggers do Quartz baseados em expressão cron, 1:1 com QRTZ_TRIGGERS. |
| `QRTZ_FIRED_TRIGGERS` | scheduler-quartz | ENTRY_ID | 12 | Registro transitório de triggers em execução/adquiridos pelos nós do scheduler. |
| `QRTZ_JOB_DETAILS` | scheduler-quartz | JOB_GROUP, JOB_NAME | 9 | Definição dos jobs agendados no Quartz (classe, grupo, nome, dados). Entidade com named queries usadas pelo painel de agendamentos do Fluig. |
| `QRTZ_JOB_LISTENERS` | scheduler-quartz | JOB_GROUP, JOB_LISTENER, JOB_NAME | 3 | Listeners de job registrados por job. |
| `QRTZ_LOCKS` | scheduler-quartz | LOCK_NAME | 1 | Linhas de lock usadas pelo Quartz em modo cluster (SELECT FOR UPDATE) para sincronizar nós. |
| `QRTZ_PAUSED_TRIGGER_GRPS` | scheduler-quartz | TRIGGER_GROUP | 1 | Grupos de triggers pausados. |
| `QRTZ_SCHEDULER_STATE` | scheduler-quartz | INSTANCE_NAME | 4 | Estado/heartbeat de cada instância (nó) do scheduler no cluster. |
| `QRTZ_SIMPLE_TRIGGERS` | scheduler-quartz | TRIGGER_GROUP, TRIGGER_NAME | 5 | Detalhe de triggers Quartz de repetição simples (contagem e intervalo), 1:1 com QRTZ_TRIGGERS. |
| `QRTZ_TRIGGERS` | scheduler-quartz | TRIGGER_GROUP, TRIGGER_NAME | 16 | Triggers do Quartz: quando e qual job disparar, estado e próximos/últimos disparos. |
| `QRTZ_TRIGGER_LISTENERS` | scheduler-quartz | TRIGGER_GROUP, TRIGGER_LISTENER, TRIGGER_NAME | 3 | Listeners de trigger registrados por trigger. |
| `RATING` | rating | ID | 8 | Avaliação (nota) que um usuário deu a um app mobile do Fluig (MY_FLUIG ou MY_APPROVAL), uma linha por usuário e app. |
| `RESET_PASSWORD_TOKEN` | security-oauth-tokens | TOKEN_ID | 4 | Token de redefinição de senha ("esqueci minha senha") emitido para um usuário do tenant. Recebe linha quando o usuário solicita reset. |
| `SEGUR_ANEXO_PROCES` | bpm-definicao-processo | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS, NUM_SEQ | 7 | Regras de segurança de anexos por versão de processo: define quem (mecanismo de atribuição) tem qual nível de acesso aos anexos da solicitação. |
| `SEQ_ECM` | infraestrutura-sequencias | COD_EMPRESA, CD_TABELA | 3 | Tabela de sequências (próximo ID) por empresa e por tabela lógica, usada pelo ECM/workflow para gerar chaves numéricas sem auto-increment. |
| `SERV_DADOS` | integracao-servicos-dados | COD_EMPRESA, NOM_SERV_DADOS | 20 | Cadastro de serviços de dados (data services) externos usados por datasets e integrações: SOAP, Progress, REST e JDBC, com URL e credenciais. |
| `SERV_DATASET` | integracao-datasets | COD_EMPRESA, COD_DATASET | 19 | Cadastro de datasets (fontes de dados consultáveis por formulários/scripts), com implementação JS, builder e configuração de cache/offline. |
| `SESSAO_TOKEN` | security-oauth-tokens | COD_TOKEN | 3 | Tokens de sessão (UUID) associados a um login, com marca do último uso. Usada pela entidade Token do foundation/webdesk. |
| `SINONIMO` | ecm-search | COD_EMPRESA, IND_IDIOMA, COD_TERMO, COD_TERMO_SINONIMO | 4 | Sinônimos de termos do dicionário de busca, por idioma. |
| `SOCIABLE` | social | id | 36 | Tabela única (SINGLE_TABLE) de conteúdos "sociáveis" da rede social: posts, comentários, objetos sociais (links/recomendações) e objetos no-code (formulários). O tipo é dado por SOCIABLETYPE. |
| `SOCIABLEDENOUNCEMENT` | social | id | 7 | Denúncia (de usuário ou por lista negra de palavras) feita contra um conteúdo sociável. |
| `SOCIABLEDENOUNCEMENTHISTORY` | social | id | 6 | Histórico de mudanças de status de uma denúncia, com texto e usuário que agiu. |
| `SOCIABLELIKE` | social | id | 3 | Curtidas: um perfil social curtiu um conteúdo sociável. |
| `SOCIABLESHARE` | social | id | 7 | Compartilhamento de um conteúdo sociável por um perfil, para seguidores, usuário ou comunidade. |
| `SOCIABLEWATCH` | social | id | 5 | Acompanhamento ("seguir") de um conteúdo sociável por um perfil, para notificações. |
| `SOCIAL` | social | id | 17 | Tabela única (SINGLE_TABLE) de perfis sociais: usuários (SocialUser), comunidades, eventos e aplicações, com alias único por tenant. Raiz das FKs da rede social. |
| `SOCIALACCESSTOKEN` | social | id | 8 | Token de acesso (OAuth) armazenado por perfil social para integração com organização externa. Sem entidade JPA localizada. |
| `SOCIALDATA` | social | id | 7 | Pares chave/valor extensíveis associados a um perfil social. |
| `SOCIALFAVORITE` | social | id | 4 | Favoritos: um perfil social favoritou outro perfil/comunidade. |
| `SOCIALFORMCONTROL` | social-forms | id | 6 | Controle de formulário/enquete social vinculado a um documento do ECM, com hash e versão do formulário. |
| `SOCIALFORMEVENT` | social-forms | id | 10 | Regra de evento de formulário social (habilitar/exibir/validar campo conforme condição) por documento e atividade. |
| `SOCIALFORMEVENTDETAIL` | social-forms | id | 5 | Condição individual (operação, tipo e valor) de um evento de formulário social. |
| `SOCIALINVITE` | social | id | 11 | Convite por e-mail para novo usuário ingressar na rede social, com token, status e expiração. |
| `SOCIALINVITEGROUP` | social | id | 3 | Grupos associados a um convite; o convidado entra nesses grupos ao se cadastrar. |
| `SOCIALPOSTUSER` | social | id | 7 | Permissões por usuário em um post (usado em posts privados/personalizados). |
| `SOCIALRELATION` | social | id | 6 | Relação direcionada entre dois perfis sociais (amizade, seguir, participante, moderador). |
| `SOCIALRELATIONCOUNTER` | social | id | 7 | Contadores de relações por perfil e tipo. |
| `SOCIALWIZARDUSER` | social | id | 5 | Controle do assistente (wizard) de boas-vindas social por usuário. Sem entidade JPA; usada pelo war social-wizard-user. |
| `SOCIAL_POSTATTACHMENT` | social |  | 2 | Tabela de junção entre uma postagem social e seus anexos; ambas as pontas apontam para SOCIABLE (entidade base de itens sociais). |
| `SOCIAL_SESSION_TOKEN` | social | SESSION_TOKEN_ID | 6 | Token de sessão por perfil social e aplicação (ex.: apps externas/mobile), com data de expiração. |
| `SOCIAL_TAB_PERMISSION` | social | SOCIAL_TAB_PERMISSION_ID | 6 | Permissão de abas do perfil/comunidade social (hoje só NOCODE_FORMS_APP), com tipo de acesso e flag de ativação. |
| `TAG` | ecm-search | COD_EMPRESA, COD_TAG | 2 | Cadastro de tags (etiquetas) usadas para classificar conteúdo. |
| `TAR_CONHECIMENTO_USUARIO` | bpm-workflow | COD_EMPRESA, NUM_PROCES, CD_MATRICULA, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF | 5 | Registra que um usuário tomou conhecimento (ciência) de uma tarefa de processo transferida/atribuída, por movimentação e sequência de transferência. |
| `TAR_CTRAL` | bpm-tarefas | COD_EMPRESA, COD_TAREFA | 11 | Tabela raiz (herança JOINED, entidade Task) das tarefas do gerenciador de tarefas: um registro por tarefa com dono, prazo e status. Subtipos em TAR_DOCTO, TAR_ESFOR, TAR_PARTIC, TAR_WORKFLOW. |
| `TAR_DOCTO` | bpm-tarefas | COD_EMPRESA, COD_TAREFA | 4 | Subtipo de tarefa (herança JOINED de Task) ligado a um documento específico do GED; base para tarefas de edição e revisão de documento. |
| `TAR_DOCTO_EDIC` | bpm-tarefas | COD_EMPRESA, COD_TAREFA | 3 | Subtipo de TAR_DOCTO para tarefas de edição de documento; guarda o documento de destino da edição. |
| `TAR_DOCTO_REVIS` | bpm-tarefas | COD_EMPRESA, COD_TAREFA | 2 | Subtipo de TAR_DOCTO para tarefas de revisão de documento; sem colunas além da PK. |
| `TAR_ESFOR` | bpm-tarefas | COD_EMPRESA, COD_TAREFA | 2 | Subtipo de Task (EffortRecordedTask) para tarefas de esforço registrado; tabela marcadora sem colunas além da PK. |
| `TAR_PARTIC` | bpm-tarefas | COD_EMPRESA, COD_TAREFA | 2 | Subtipo de Task (ToDoTask) para tarefas to-do/de participação; tabela marcadora sem colunas além da PK. |
| `TAR_PROCES` | bpm-workflow | COD_EMPRESA, NUM_PROCES, NUM_SEQ_MOVTO, NUM_SEQ_TRANSF, CD_MATRICULA | 41 | Atribuição de tarefa de processo a um usuário: uma linha por usuário responsável por uma etapa (movimentação) de uma instância, com status, prazos, avisos de atraso e conclusão. Base da central de tarefas do workflow. |
| `TAR_WORKFLOW` | bpm-tarefas | COD_EMPRESA, COD_TAREFA | 4 | Subtipo de tarefa que liga uma tarefa do gerenciador à movimentação (etapa) de uma instância de processo de workflow. |
| `TEMA_FORMULARIO` | bpm-forms | COD_EMPRESA, NUM_TEMA_FORM | 6 | Temas visuais (arquivos de tema) aplicáveis a formulários. |
| `TEMPLATE_EMAIL` | notificacao-email | COD_EMPRESA, COD_TEMPLATE_EMAIL, COD_DIALETO | 7 | Cadastro de templates de e-mail do Fluig por empresa e idioma (dialeto), apontando o arquivo físico do template; inclui padrão e customizados. |
| `TERMO` | ecm-search | COD_EMPRESA, IND_IDIOMA, COD_TERMO | 4 | Dicionário de termos de busca por idioma, com marcação de termos irrelevantes (stop words). |
| `THREAD_PROCES` | bpm-workflow | COD_EMPRESA, NUM_PROCES, NUM_SEQ_THREAD | 8 | Threads paralelas (fork/join) de uma instância de processo: cada linha representa um ramo paralelo ativo ou finalizado. |
| `TIME_DIM_CAP` | bpm-analytics-dw | COMPANYID, DAYID, MONTHID, YEARID | 7 | Dimensão de tempo (calendário): uma linha por dia com data completa, feriado e dia da semana. |
| `TIPO_DOCUMENTO` | ecm-documents | COD_EMPRESA, CD_TIPO_DOC | 3 | Cadastro de tipos de documento (classificação definida pelo cliente) aplicados a documentos do GED. |
| `USEPOLICY` | use-policy | id | 2 | Política de uso de um tenant; agrega os documentos de política via USEPOLICY_POLICYDOCUMENT. |
| `USEPOLICY_POLICYDOCUMENT` | use-policy | USEPOLICY_ID, DOCUMENTS_ID | 2 | Tabela de junção JPA entre USEPOLICY e seus POLICYDOCUMENT (@OneToMany documents). |
| `USER_DIM_CAP` | bpm-analytics-dw | COMPANYID, USERSEQUENCE | 4 | Dimensão de usuários do CAP com chave substituta USERSEQUENCE, código do usuário e custo por hora. |
| `VAL_HORA_COLAB` | bpm-workflow | COD_EMPRESA, DAT_ATUALIZ, HRA_ATUALIZ, CD_MATRICULA | 7 | Histórico do valor da hora de trabalho de um colaborador, usado para custeio de tarefas/processos; cada linha vale a partir do momento da atualização. |
| `VERBOSE_SCRIPT_LOG` | bpm-workflow | ID | 6 | Registra habilitação do log detalhado (verbose) de scripts para um item (ex.: uma instância de processo) solicitada por um usuário. |
| `VERS_DEF_PROCES` | bpm-process-definition | COD_EMPRESA, COD_DEF_PROCES, NUM_VERS | 16 | Versões de definições de processo (BPM): uma linha por versão publicada/em edição do processo com seu diagrama e opções. |
| `VERS_DEF_PROCES_ALERT` | bpm-process-definition | ID | 8 | Alertas de análise (boas práticas/riscos) gerados para versões de definição de processo. |
| `WCM_APPLICATION` | wcm-portal | APPLICATION_ID | 31 | Catálogo de aplicações do portal WCM em herança single-table: temas, layouts, widgets, componentes (páginas) e aplicações; APPLICATION_TYPE discrimina o tipo. |
| `WCM_APPLICATIONCATEGORY` | wcm-portal | APPLICATION_CATEGORY_ID | 3 | Categoria atribuída a uma aplicação WCM (agrupamento no catálogo de widgets). |
| `WCM_APPLICATIONDATA` | wcm-portal | APPLICATION_DATA_ID | 4 | Par chave/valor de configuração de uma instância de widget em página (por PAGE_WIDGET_ID), compartilhado entre usuários. |
| `WCM_APPLICATIONLOCALE` | wcm-portal | APPLICATION_LOCALE_ID | 3 | Locale (idioma) suportado por uma aplicação WCM. |
| `WCM_APPLICATIONPRODUCT` | wcm-portal | APPLICATION_PRODUCT_ID | 3 | Produto TOTVS ao qual a aplicação WCM está associada (um registro por produto). |
| `WCM_APPLICATIONRESOURCE` | wcm-portal | APPLICATION_RESOURCE_ID | 5 | Recurso estático (ex.: CSS/JS) declarado por uma aplicação WCM, com ordem de carga. |
| `WCM_APPLICATIONSERVICE` | wcm-portal | APPLICATION_SERVICE_ID | 4 | Serviço (EJB/JNDI) exposto à aplicação WCM por nome de variável. |
| `WCM_APPLICATIONUSERDATA` | wcm-portal | APPLICATION_DATA_ID | 5 | Par chave/valor de preferência de widget por usuário (LOGIN) e instância (PAGE_WIDGET_ID). |
| `WCM_APPLICATION_APP_DEPENDENCY` | wcm-portal | id | 6 | Vínculo entre aplicação WCM e uma dependência (WCM_APPLICATION_DEPENDENCY), com flag de ativo. |
| `WCM_APPLICATION_DEPENDENCY` | wcm-portal | ID | 6 | Dependência (biblioteca/recurso por código e tipo) que aplicações WCM podem declarar, por tenant. |
| `WCM_COMPONENTPAGE` | wcm-portal | COMPONENTPAGE_ID | 4 | Associa um componente (aplicação WCM) a uma versão de página. |
| `WCM_CONFIGURATION` | wcm-portal | CONFIGURATION_ID | 7 | Configuração global do portal WCM (layout/tema padrão, URL do servidor, permissões de perfil/espaço). |
| `WCM_LAYOUTSLOT` | wcm-portal | LAYOUT_SLOT_ID | 5 | Slot (região) de um layout WCM onde widgets podem ser colocados. |
| `WCM_MENUITEM` | wcm-portal | MENUITEM_ID | 13 | Item de menu do portal, hierárquico, que aponta para página ou link externo. |
| `WCM_PAGE` | wcm-portal | PAGE_ID | 15 | Página do portal WCM (hierárquica), com tema, URL amigável e flags de exibição. |
| `WCM_PAGEDATA` | wcm-portal | PAGE_DATA_ID | 4 | Par chave/valor de dados de uma versão de página. |
| `WCM_PAGEVERSION` | wcm-portal-pages | ID | 16 | Versão de uma página do portal WCM (título, ícone, layout, autorização, publicação). Cada edição/publicação gera nova versão ligada a WCM_PAGE. |
| `WCM_PAGEWIDGET` | wcm-portal-pages | PAGE_WIDGET_ID | 8 | Posicionamento de um widget (aplicação WCM) em um slot de uma versão de página. |
| `WCM_RESOURCECOMPONENT` | wcm-resources | RESOURCE_COMPONENT_ID | 2 | Catálogo de componentes de recursos estáticos (bibliotecas JS/CSS) identificados por código, que temas/widgets podem referenciar. |
| `WCM_RESOURCECOMPONENTFILE` | wcm-resources | RESOURCE_COMPONENT_FILE_ID | 5 | Arquivos (JS/CSS etc.) pertencentes a um componente de recurso, com tipo, caminho e ordem de carga. |
| `WCM_RESOURCEKIT` | wcm-resources | RESOURCE_KIT_ID | 2 | Catálogo de kits de recursos estáticos (conjuntos de arquivos) identificados por código. |
| `WCM_RESOURCEKITFILE` | wcm-resources | RESOURCE_KIT_FILE_ID | 5 | Arquivos que compõem um kit de recursos, com tipo, caminho e ordem. |
| `WCM_STOREITEM_METRIC` | wcm-store | STOREITEM_METRIC_ID | 8 | Métricas de uso (downloads e visualizações) de itens da loja de componentes WCM, por tenant. |
| `WCM_TENANTAPPLICATION` | wcm-portal-apps | TENANT_APPLICATION_ID | 5 | Habilitação de uma aplicação WCM (widget/tema/layout) para um tenant, com código externo opcional. |
| `WCM_THEME_HISTORY` | wcm-theme | THEME_HISTORY_ID | 9 | Histórico de trocas de tema do portal por tenant (tema anterior e novo) com flags sobre tema responsivo. |