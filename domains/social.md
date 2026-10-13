# Domínio: social

21 tabelas. Fonte: DDL MySQL do Fluig 1.8.2 + entidades JPA. Detalhe completo em `schema.json` / `by_table/<TABELA>.json`.

## MENTION

Menção (@usuário) feita em um objeto social (post/comentário); liga o autor ao perfil social mencionado.

**Ciclo de vida:** Linha criada ao salvar conteúdo com @menção. Volume proporcional a posts/comentários.

**Atenção:** Multi-tenant por TENANTID. Objeto mencionante é polimórfico (MENTIONINGCLASS + MENTIONINGID), sem FK.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id da menção; PK. |  |  |
| `CREATIONDATE` | datetime | N | Data/hora de criação da linha (timestamp). |  |  |
| `LASTUPDATEDATE` | datetime | N | Data/hora da última alteração da linha (timestamp). |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `MENTIONINGCLASS` | varchar(255) | N | Nome da classe do objeto que contém a menção (polimórfico, ex.: classe de post/comentário). |  |  |
| `MENTIONINGID` | bigint | N | Id do objeto mencionante (interpretar junto com MENTIONINGCLASS; tipicamente SOCIABLE.ID). |  | SOCIABLE.ID |
| `AUTHOR_ID` | bigint | N | Perfil social (SocialUser) autor da menção. |  | SOCIAL.ID |
| `SOCIAL_ID` | bigint | N | Perfil social mencionado. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(AUTHOR_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Autor da menção (perfil SocialUser)
- `(SOCIAL_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil social que foi mencionado
- `(MENTIONINGID)` → **SOCIABLE** `(ID)` · N:1 · logical-probable/probable — Objeto mencionante (polimórfico via MENTIONINGCLASS); sem FK

**Dicas de consulta:** Para achar o conteúdo: MENTIONINGCLASS (classe) + MENTIONINGID (id na SOCIABLE, quando a classe é um Sociable).

## PROFANITY

Configuração do filtro de palavrões da rede social por tenant: liga/desliga e lista de palavras proibidas.

**Ciclo de vida:** Uma linha por tenant (unique TENANT_ID), criada/alterada pelo administrador.

**Atenção:** Unique em TENANT_ID: no máximo uma linha por tenant.

**PK:** id · **Unique:** (tenant_id)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id da configuração; PK. |  |  |
| `ENABLED` | bit | S | Indica se o filtro de palavrões está ativo no tenant. | 1=ativo; 0=inativo |  |
| `PROFANITY_WORDS` | varchar(4000) | S | Lista de palavras proibidas (até 4000 chars) usada para filtrar posts/comentários. |  |  |
| `TENANT_ID` | bigint | N | Id do tenant; único (uma configuração por tenant). |  | FDN_TENANT.TENANT_ID |

**Dicas de consulta:** Lista de palavras em campo único varchar(4000) (formato do separador não confirmado).

## SOCIABLE

Tabela única (SINGLE_TABLE) de conteúdos "sociáveis" da rede social: posts, comentários, objetos sociais (links/recomendações) e objetos no-code (formulários). O tipo é dado por SOCIABLETYPE.

**Ciclo de vida:** Linhas criadas ao publicar post/comentário/objeto; contadores (curtidas, comentários etc.) incrementados via UPDATE; remoção lógica por REMOVED.

**Atenção:** Herança SINGLE_TABLE: colunas de cada subclasse (SociableNoCodeObject, SocialObject, SociableComment, SocialPost) são NULL nas outras. Soft-delete em REMOVED. Multi-tenant por TENANTID. Discriminador SOCIABLETYPE = nome simples da entidade.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `SOCIABLETYPE` | varchar(128) | N | Discriminador de herança: nome da entidade da linha. | SociableComment=comentário; SocialPost=post; SocialObject=objeto social/recomendação; SociableNoCodeObject=objeto no-code (formulário); (valores confirmados pelas queries/entidades) |  |
| `ID` | bigint | N | Id do conteúdo; PK. |  |  |
| `CREATIONDATE` | datetime | N | Data/hora de criação da linha (timestamp). |  |  |
| `LASTUPDATEDATE` | datetime | N | Data/hora da última alteração da linha (timestamp). |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `CUSTOMDATA` | varchar(1000) | S | Dados customizados em texto livre (até 1000 chars) anexados ao conteúdo. |  |  |
| `EDITIONDATE` | datetime | S | Data/hora da última edição pelo autor (distinta de LASTUPDATEDATE, que muda também com contadores). |  |  |
| `NUMBERCOMMENTS` | integer | N | Contador denormalizado de comentários do conteúdo. |  |  |
| `NUMBERDENOUNCEMENTS` | integer | N | Contador denormalizado de denúncias; conteúdo com valor >0 é filtrado em listagens. |  |  |
| `NUMBERLIKES` | integer | N | Contador denormalizado de curtidas. |  |  |
| `NUMBERSHARES` | integer | N | Contador denormalizado de compartilhamentos. |  |  |
| `NUMBERWATCHERS` | integer | N | Contador denormalizado de seguidores/observadores do conteúdo. |  |  |
| `REMOVED` | bit | N | Remoção lógica do conteúdo. | 1=removido; 0=ativo |  |
| `TAGS` | varchar(255) | S | Tags do conteúdo em texto (varchar 255). |  |  |
| `URL` | varchar(255) | S | URL associada ao conteúdo/anexo. |  |  |
| `NOCODE_EXTERNAL_ID` | varchar(255) | S | (SociableNoCodeObject) Id do objeto externo no app no-code (ex.: documento/formulário). |  |  |
| `NOCODE_APP_ID` | varchar(255) | S | (SociableNoCodeObject) Aplicação no-code de origem. | FORMS=formulários |  |
| `NOCODE_TYPE_ID` | varchar(255) | S | (SociableNoCodeObject) Tipo do objeto no-code. | FORM=formulário |  |
| `NOCODE_TITLE` | varchar(255) | S | (SociableNoCodeObject) Título exibido do objeto no-code. |  |  |
| `COMMENTS` | varchar(700) | S | (SociableComment) Texto do comentário (até 700 chars). |  |  |
| `HASMENTIONS` | bit | S | (SocialPost) Indica que o conteúdo contém @menções (ver MENTION). | 1=sim; 0=não |  |
| `LINK` | varchar(2048) | S | (SocialPost) Link anexado ao post (até 2048 chars). |  |  |
| `SOCIABLE_ID` | bigint | S | (SociableComment) Conteúdo ao qual o comentário pertence. |  | SOCIABLE.ID |
| `DESCRIPTION` | varchar(4000) | S | (SocialObject) Descrição do objeto social (até 4000 chars). |  |  |
| `OBJECTCLASS` | varchar(255) | S | (SocialObject) Classe do objeto externo referenciado (polimórfico). |  |  |
| `OBJECTID` | varchar(255) | S | (SocialObject) Id (texto) do objeto externo referenciado; par com OBJECTCLASS. |  |  |
| `TEXT` | TEXT | S | Texto do post ou objeto social (SocialPost até 10000; SocialObject até 700). |  |  |
| `THUMBURL` | varchar(255) | S | (SocialObject) URL da miniatura. |  |  |
| `TYPE` | integer | S | (SocialPost) Tipo do post, ordinal de SocialPostType. | 0=DEFAULT; 1=RECOMMENDATION |  |
| `VISIBILITY` | integer | S | (SocialPost) Visibilidade, ordinal de SocialPostVisibility. | 0=PUBLIC; 1=PRIVATE; 2=CUSTOM |  |
| `SOCIAL_ID` | bigint | S | Perfil/comunidade social onde o conteúdo foi publicado. |  | SOCIAL.ID |
| `USER_ID` | bigint | S | Perfil social (SocialUser) autor do conteúdo; não é FDN_USER. |  | SOCIAL.ID |
| `LINKEDOBJECT_ID` | bigint | S | (SocialPost) Objeto sociável vinculado ao post (ex.: recomendação). |  | SOCIABLE.ID |
| `HEIGHT` | integer | S | Altura em pixels da mídia/anexo. |  |  |
| `WIDTH` | integer | S | Largura em pixels da mídia/anexo. |  |  |
| `MIMETYPE` | varchar(255) | S | MIME type do anexo. |  |  |

**Relacionamentos (saem desta tabela):**

- `(SOCIAL_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil/comunidade onde foi publicado
- `(USER_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Autor (SocialUser)
- `(SOCIABLE_ID)` → **SOCIABLE** `(ID)` · N:1 · physical-fk/confirmed — Comentário -> conteúdo pai (auto-relação)
- `(LINKEDOBJECT_ID)` → **SOCIABLE** `(ID)` · N:1 · physical-fk/confirmed — Post -> objeto sociável vinculado (auto-relação)

**Dicas de consulta:** Sempre filtrar REMOVED=0, TENANTID e SOCIABLETYPE. Colunas de imagem/arquivo (HEIGHT, WIDTH, MIMETYPE) pertencem a anexos. Conteúdo livre em TEXT/COMMENTS pode ter dados pessoais.

## SOCIABLEDENOUNCEMENT

Denúncia (de usuário ou por lista negra de palavras) feita contra um conteúdo sociável.

**Ciclo de vida:** Linha criada ao denunciar; STATUS evolui na moderação, com histórico em SOCIABLEDENOUNCEMENTHISTORY.

**Atenção:** Sem TENANTID próprio; tenant via SOCIABLE.TENANTID.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id da denúncia; PK. |  |  |
| `CREATIONDATE` | datetime | N | Data/hora da denúncia. |  |  |
| `STATUS` | integer | N | Estado da denúncia, ordinal de SociableDenouncementStatus. | 0=PENDING; 1=ARCHIVED; 2=REVOKED |  |
| `TEXT` | varchar(255) | N | Motivo/texto da denúncia (até 255). |  |  |
| `TYPE` | integer | N | Origem da denúncia, ordinal de SociableDenouncementType. | 0=USER; 1=BLACKLIST |  |
| `SOCIABLE_ID` | bigint | N | Conteúdo denunciado. |  | SOCIABLE.ID |
| `USER_ID` | bigint | S | Perfil social do denunciante (nulo p/ detecção automática). |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(SOCIABLE_ID)` → **SOCIABLE** `(ID)` · N:1 · physical-fk/confirmed — Conteúdo denunciado
- `(USER_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Denunciante (SocialUser)

**Dicas de consulta:** Transições válidas: PENDING->ARCHIVED/REVOKED e ARCHIVED->PENDING. USER_ID é SOCIAL.ID, nulo em denúncia automática.

## SOCIABLEDENOUNCEMENTHISTORY

Histórico de mudanças de status de uma denúncia, com texto e usuário que agiu.

**Ciclo de vida:** Uma linha por transição/ação de moderação.

**Atenção:** Sem TENANTID; tenant via denúncia/conteúdo.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do registro de histórico; PK. |  |  |
| `CREATIONDATE` | datetime | N | Data/hora da ação registrada. |  |  |
| `STATUS` | integer | N | Status da denúncia resultante da ação, ordinal de SociableDenouncementStatus. | 0=PENDING; 1=ARCHIVED; 2=REVOKED |  |
| `TEXT` | varchar(255) | N | Justificativa/comentário da ação. |  |  |
| `DENOUNCE_ID` | bigint | N | Denúncia à qual o histórico pertence. |  | SOCIABLEDENOUNCEMENT.ID |
| `USER_ID` | bigint | N | Perfil social do usuário que executou a ação. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(DENOUNCE_ID)` → **SOCIABLEDENOUNCEMENT** `(ID)` · N:1 · physical-fk/confirmed — Denúncia à qual a ação pertence
- `(USER_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Usuário que agiu

**Dicas de consulta:** Ordenar por CREATIONDATE para a linha do tempo.

## SOCIABLELIKE

Curtidas: um perfil social curtiu um conteúdo sociável.

**Ciclo de vida:** Linha criada ao curtir e removida ao descurtir.

**Atenção:** Unique (SOCIABLE_ID, USER_ID): uma curtida por usuário por conteúdo.

**PK:** id · **Unique:** (sociable_id, user_id)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id da curtida; PK. |  |  |
| `SOCIABLE_ID` | bigint | N | Conteúdo curtido. |  | SOCIABLE.ID |
| `USER_ID` | bigint | N | Perfil social (SocialUser) que curtiu. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(SOCIABLE_ID)` → **SOCIABLE** `(ID)` · N:1 · physical-fk/confirmed — Conteúdo curtido
- `(USER_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Quem curtiu

**Dicas de consulta:** Contador denormalizado em SOCIABLE.NUMBERLIKES.

## SOCIABLESHARE

Compartilhamento de um conteúdo sociável por um perfil, para seguidores, usuário ou comunidade.

**Ciclo de vida:** Linha criada ao compartilhar.

**Atenção:** Sem TENANTID. SOCIAL_ID é o destino quando TYPE é USER/COMMUNITY.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do compartilhamento; PK. |  |  |
| `TEXT` | varchar(700) | S | Texto adicional do compartilhamento (até 10000 no Java, coluna varchar 700). |  |  |
| `TYPE` | integer | S | Tipo de destino, ordinal de SociableShareType. | 0=FOLLOWERS; 1=USER; 2=COMMUNITY |  |
| `URLORIGIN` | varchar(255) | S | URL de origem do conteúdo compartilhado. |  |  |
| `SOCIABLE_ID` | bigint | N | Conteúdo compartilhado. |  | SOCIABLE.ID |
| `SOCIAL_ID` | bigint | S | Perfil/comunidade destino do compartilhamento (nulo se FOLLOWERS). |  | SOCIAL.ID |
| `USER_ID` | bigint | N | Perfil social que compartilhou. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(SOCIABLE_ID)` → **SOCIABLE** `(ID)` · N:1 · physical-fk/confirmed — Conteúdo compartilhado
- `(SOCIAL_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Destino do compartilhamento
- `(USER_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Quem compartilhou

**Dicas de consulta:** Contador em SOCIABLE.NUMBERSHARES.

## SOCIABLEWATCH

Acompanhamento ("seguir") de um conteúdo sociável por um perfil, para notificações.

**Ciclo de vida:** Criada ao seguir; removida ao deixar de seguir.

**Atenção:** Unique (SOCIABLE_ID, USER_ID).

**PK:** id · **Unique:** (sociable_id, user_id)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do acompanhamento; PK. |  |  |
| `CREATIONDATE` | datetime | N | Data/hora em que passou a acompanhar. |  |  |
| `REQUIRED` | bit | N | Acompanhamento obrigatório (não pode ser cancelado pelo usuário). | 1=obrigatório; 0=voluntário |  |
| `SOCIABLE_ID` | bigint | N | Conteúdo acompanhado. |  | SOCIABLE.ID |
| `USER_ID` | bigint | N | Perfil social que acompanha. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(SOCIABLE_ID)` → **SOCIABLE** `(ID)` · N:1 · physical-fk/confirmed — Conteúdo acompanhado
- `(USER_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Observador

**Dicas de consulta:** REQUIRED indica acompanhamento imposto.

## SOCIAL

Tabela única (SINGLE_TABLE) de perfis sociais: usuários (SocialUser), comunidades, eventos e aplicações, com alias único por tenant. Raiz das FKs da rede social.

**Ciclo de vida:** Perfil de usuário criado ao provisionar usuário Fluig; comunidades criadas por usuários.

**Atenção:** Herança SINGLE_TABLE (DTYPE). Multi-tenant: unique (ALIAS, TENANTID). USER_ID/SOCIAL_ID das outras tabelas sociais apontam para SOCIAL.ID, não para FDN_USER.

**PK:** id · **Unique:** (alias, tenantid)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `DTYPE` | varchar(31) | N | Discriminador de herança: entidade da linha (Social ou SocialUser; padrão Hibernate = nome da entidade). | SocialUser=perfil de usuário; Social=comunidade/evento/aplicação |  |
| `ID` | bigint | N | Id do perfil social; PK referenciada pelas demais tabelas sociais. |  |  |
| `CREATIONDATE` | datetime | N | Data/hora de criação da linha (timestamp). |  |  |
| `LASTUPDATEDATE` | datetime | N | Data/hora da última alteração da linha (timestamp). |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `ALIAS` | varchar(255) | N | Identificador/slug único do perfil no tenant. |  |  |
| `APPROVALREQUIRED` | bit | N | Participação exige aprovação (comunidades). | 1=exige aprovação; 0=livre |  |
| `CUSTOMPAGE` | bit | S | Indica que usa página customizada. | 1=sim; 0=não |  |
| `DESCRIPTION` | varchar(255) | S | Descrição do perfil/comunidade. |  |  |
| `FORUMID` | bigint | S | Id do fórum associado (comunidade). |  |  |
| `HIDDEN` | bit | N | Perfil oculto das listagens. | 1=oculto; 0=visível |  |
| `NAME` | varchar(255) | N | Nome exibido do perfil/comunidade. |  |  |
| `PRIVATECONTENT` | bit | N | Conteúdo restrito aos membros. | 1=privado; 0=público |  |
| `STATE` | integer | N | Estado do perfil, ordinal de UserState. | 0=UNCONFIRMED; 1=ACTIVE; 2=BLOCKED; 3=REMOVED |  |
| `TYPE` | integer | N | Tipo do perfil, ordinal de SocialType. | 0=USER; 1=COMMUNITY; 2=EVENT; 3=APPLICATION |  |
| `FOUNDATIONUSERID` | bigint | S | (SocialUser) Id do usuário no foundation Fluig. |  | FDN_USER.USER_ID |
| `USER_ADMIN` | bigint | S | Perfil (SocialUser) administrador da comunidade. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(USER_ADMIN)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Administrador da comunidade (auto-relação)
- `(FOUNDATIONUSERID)` → **FDN_USER** `(USER_ID)` · N:1 · logical-probable/probable — Perfil SocialUser -> usuário foundation; sem FK

**Dicas de consulta:** Para ligar ao usuário Fluig: SOCIAL.FOUNDATIONUSERID (somente DTYPE=SocialUser). Filtrar TYPE e HIDDEN.

## SOCIALACCESSTOKEN

Token de acesso (OAuth) armazenado por perfil social para integração com organização externa. Sem entidade JPA localizada.

**Ciclo de vida:** Provável criação ao autorizar integração; expira em EXPIRESIN.

**Atenção:** Unique (SOCIALID, TENANTID, ORGID). Sem entidade no código: semântica inferida pelos nomes.

**PK:** id · **Unique:** (SOCIALID, TENANTID, ORGID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do registro; PK. |  |  |
| `ACCESSTOKEN` | varchar(255) | N | Token de acesso à organização externa (credencial). |  |  |
| `EXPIRESIN` | datetime | N | Data/hora de expiração do token. |  |  |
| `ORGID` | varchar(255) | N | Id da organização externa à qual o token dá acesso. |  |  |
| `SCOOPE` | varchar(255) | N | Escopo (grafia "scoope") autorizado do token. |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `TOKENTYPE` | varchar(255) | N | Tipo do token (ex.: bearer). |  |  |
| `SOCIALID` | bigint | N | Perfil social dono do token. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(SOCIALID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil dono do token

**Dicas de consulta:** Dado sensível: ACCESSTOKEN é credencial.

## SOCIALDATA

Pares chave/valor extensíveis associados a um perfil social.

**Ciclo de vida:** Linha por (perfil, chave), gravada ao salvar preferências/atributos.

**Atenção:** Unique (SOCIALID, DATAKEY).

**PK:** id · **Unique:** (socialid, datakey)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do dado; PK. |  |  |
| `CREATIONDATE` | datetime | N | Data/hora de criação da linha (timestamp). |  |  |
| `LASTUPDATEDATE` | datetime | N | Data/hora da última alteração da linha (timestamp). |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `DATAKEY` | varchar(128) | N | Chave do atributo (Java key; ver enum SocialDataKey). |  |  |
| `DATAVALUE` | varchar(512) | N | Valor do atributo (até 512). |  |  |
| `SOCIALID` | bigint | N | Perfil social dono do atributo. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(SOCIALID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil dono do atributo

**Dicas de consulta:** Valor limitado a 512 chars. Tenant em TENANTID.

## SOCIALFAVORITE

Favoritos: um perfil social favoritou outro perfil/comunidade.

**Ciclo de vida:** Criada ao favoritar; removida ao desfavoritar.

**Atenção:** Unique (USER_ID, FAVORITEDSOCIAL_ID).

**PK:** id · **Unique:** (user_id, favoritedSocial_id)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do favorito; PK. |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `FAVORITEDSOCIAL_ID` | bigint | N | Perfil/comunidade favoritado. |  | SOCIAL.ID |
| `USER_ID` | bigint | N | Perfil social (SocialUser) que favoritou. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(FAVORITEDSOCIAL_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil favoritado
- `(USER_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Quem favoritou

## SOCIALINVITE

Convite por e-mail para novo usuário ingressar na rede social, com token, status e expiração.

**Ciclo de vida:** Criada ao enviar convite; STATUS atualizado; USERCREATED quando o usuário se cadastra.

**Atenção:** Unique TOKEN. Tenant em TENANTID.

**PK:** id · **Unique:** (token)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id do convite; PK. |  |  |
| `ALIAS` | varchar(255) | N | Alias do perfil/comunidade para o qual se convida. |  |  |
| `EMAIL` | varchar(255) | S | E-mail do convidado (dado pessoal). |  |  |
| `EXPIRATION` | datetime | S | Data/hora de expiração do convite. |  |  |
| `FILENAME` | varchar(255) | S | Nome do arquivo de importação de convites de origem. |  |  |
| `LASTSUBMISSION` | datetime | S | Data/hora do último envio do e-mail. |  |  |
| `QTTSUBMISSION` | integer | S | Quantidade de envios do convite. |  |  |
| `STATUS` | varchar(255) | S | Estado do convite, enum SocialInviteStatus (texto). | INVALID_EMAIL; PENDING; USER_CREATED; EXPIRED; DUPLICATED_INVITE; FAIL_TO_SEND_EMAIL |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `TOKEN` | varchar(255) | S | Token único do convite (credencial). |  |  |
| `USERCREATED` | datetime | S | Data/hora em que o usuário convidado criou a conta. |  |  |

**Dicas de consulta:** Dado pessoal: EMAIL; TOKEN é credencial de aceite.

## SOCIALINVITEGROUP

Grupos associados a um convite; o convidado entra nesses grupos ao se cadastrar.

**Ciclo de vida:** Criada com o convite.

**Atenção:** Sem tenant.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id; PK. |  |  |
| `GROUPID` | varchar(255) | N | Código do grupo Fluig (texto). |  | FDN_GROUP.GROUP_CODE |
| `SOCIALINVITE_ID` | bigint | S | Convite ao qual o grupo pertence. |  | SOCIALINVITE.ID |

**Relacionamentos (saem desta tabela):**

- `(SOCIALINVITE_ID)` → **SOCIALINVITE** `(ID)` · N:1 · physical-fk/confirmed — Convite dono do grupo
- `(GROUPID)` → **FDN_GROUP** `(GROUP_CODE)` · N:1 · logical-probable/probable — Código do grupo do convite; sem FK

## SOCIALPOSTUSER

Permissões por usuário em um post (usado em posts privados/personalizados).

**Ciclo de vida:** Criada ao compartilhar post com usuários específicos.

**Atenção:** Unique (POST_ID, USER_ID).

**PK:** id · **Unique:** (post_id, user_id)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id; PK. |  |  |
| `CREATIONDATE` | datetime | N | Data/hora de criação da linha (timestamp). |  |  |
| `LASTUPDATEDATE` | datetime | N | Data/hora da última alteração da linha (timestamp). |  |  |
| `PERMISSIONS` | varchar(255) | S | Permissões do usuário no post (texto). |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `POST_ID` | bigint | N | Post (SOCIABLE tipo SocialPost). |  | SOCIABLE.ID |
| `USER_ID` | bigint | N | Perfil social com permissão. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(POST_ID)` → **SOCIABLE** `(ID)` · N:1 · physical-fk/confirmed — Post
- `(USER_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Usuário com acesso

## SOCIALRELATION

Relação direcionada entre dois perfis sociais (amizade, seguir, participante, moderador).

**Ciclo de vida:** Criada/atualizada ao seguir, convidar, aprovar ou bloquear.

**Atenção:** Unique (SOCIAL_ID, RELATED_ID, TYPE). Ordinals dos enums.

**PK:** id · **Unique:** (social_id, related_id, type)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id; PK. |  |  |
| `STATUS` | integer | N | Status, ordinal de SocialRelationStatus. | 0=ACCEPTED; 1=REJECTED; 2=PENDING; 3=BLOCKED; 4=NOT_RELATED; 5=ITSELF |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `TYPE` | integer | N | Tipo, ordinal de SocialRelationType. | 0=FRIEND; 1=FOLLOWING; 2=FOLLOWER; 3=PARTICIPANT; 4=MODERATOR; 5=OTHER |  |
| `RELATED_ID` | bigint | N | Perfil alvo. |  | SOCIAL.ID |
| `SOCIAL_ID` | bigint | N | Perfil origem. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(RELATED_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil alvo
- `(SOCIAL_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil origem

**Dicas de consulta:** Relações recíprocas são linhas separadas.

## SOCIALRELATIONCOUNTER

Contadores de relações por perfil e tipo.

**Ciclo de vida:** Atualizada quando relações mudam.

**Atenção:** Unique (SOCIALID, RELATIONTYPE).

**PK:** id · **Unique:** (socialid, relationtype)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id; PK. |  |  |
| `CREATIONDATE` | datetime | N | Data/hora de criação da linha (timestamp). |  |  |
| `LASTUPDATEDATE` | datetime | N | Data/hora da última alteração da linha (timestamp). |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `RELATIONQUANTITY` | integer | N | Quantidade de relações do tipo. |  |  |
| `RELATIONTYPE` | integer | N | Tipo, ordinal de SocialRelationType. | 0=FRIEND; 1=FOLLOWING; 2=FOLLOWER; 3=PARTICIPANT; 4=MODERATOR; 5=OTHER |  |
| `SOCIALID` | bigint | N | Perfil dono do contador. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(SOCIALID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil dono do contador

**Dicas de consulta:** Cache; pode divergir de SOCIALRELATION.

## SOCIALWIZARDUSER

Controle do assistente (wizard) de boas-vindas social por usuário. Sem entidade JPA; usada pelo war social-wizard-user.

**Ciclo de vida:** Linha por usuário/alias ao executar o wizard.

**Atenção:** Sem FK; USERID varchar.

**PK:** id

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `ID` | bigint | N | Id; PK. |  |  |
| `ALIAS` | varchar(255) | N | Alias do perfil/usuário. |  |  |
| `LASTEXECUTEDDATE` | varchar(255) | S | Data da última execução do wizard (texto). |  |  |
| `TENANTID` | bigint | N | Id do tenant (empresa) dono da linha; filtrar sempre por ele. |  | FDN_TENANT.TENANT_ID |
| `USERID` | varchar(255) | S | Id/código do usuário (texto). |  | FDN_USERTENANT.USER_CODE |

**Dicas de consulta:** Datas em varchar.

## SOCIAL_POSTATTACHMENT

Tabela de junção entre uma postagem social e seus anexos; ambas as pontas apontam para SOCIABLE (entidade base de itens sociais).

**Ciclo de vida:** Linha criada ao anexar um item (arquivo/imagem) a uma postagem; removida junto com a postagem ou o anexo.

**Atenção:** Sem PK declarada no DDL; sem coluna de tenant (tenant vem de SOCIABLE).

**PK:** (nenhuma)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| `POST_ID` | bigint | N | ID da postagem social (SOCIABLE.ID) à qual o anexo pertence. |  | SOCIABLE.ID |
| `ATTACHMENT_ID` | bigint | N | ID do item anexado (SOCIABLE.ID) vinculado à postagem. |  | SOCIABLE.ID |

**Relacionamentos (saem desta tabela):**

- `(POST_ID)` → **SOCIABLE** `(ID)` · N:M-via-this-table · physical-fk/confirmed — Postagem dona dos anexos.
- `(ATTACHMENT_ID)` → **SOCIABLE** `(ID)` · N:M-via-this-table · physical-fk/confirmed — Item anexado à postagem.

**Dicas de consulta:** Junte duas vezes com SOCIABLE (alias post/attachment). Não há tenant aqui.

## SOCIAL_SESSION_TOKEN

Token de sessão por perfil social e aplicação (ex.: apps externas/mobile), com data de expiração.

**Ciclo de vida:** Criado/renovado quando um perfil social obtém token para uma aplicação; um registro por (SOCIAL_ID, TENANT_ID, APPLICATION_ID).

**Atenção:** Único por SOCIAL_ID+TENANT_ID+APPLICATION_ID.

**PK:** SESSION_TOKEN_ID · **Unique:** (SOCIAL_ID, TENANT_ID, APPLICATION_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `SESSION_TOKEN_ID` | bigint | N | Chave primária do token de sessão. |  |  |
| `APPLICATION_ID` | varchar(70) | N | Identificador (texto, até 70) da aplicação cliente dona do token; não é o ID numérico de WCM_APPLICATION. |  |  |
| `EXPIRESIN` | datetime | N | Data/hora de expiração do token. |  |  |
| `SESSION_TOKEN` | varchar(255) | N | Valor do token de sessão (sensível). |  |  |
| `TENANT_ID` | bigint | N | Tenant (empresa) do token. |  | FDN_TENANT.TENANT_ID |
| `SOCIAL_ID` | bigint | N | Perfil social dono do token. |  | SOCIAL.ID |

**Relacionamentos (saem desta tabela):**

- `(SOCIAL_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil social dono do token.

**Dicas de consulta:** DADO SENSÍVEL: SESSION_TOKEN. Filtre por TENANT_ID.

## SOCIAL_TAB_PERMISSION

Permissão de abas do perfil/comunidade social (hoje só NOCODE_FORMS_APP), com tipo de acesso e flag de ativação.

**Ciclo de vida:** Criada/atualizada ao configurar permissões de aba de um perfil social.

**Atenção:** Único por TENANT_ID+SOCIAL_ID+TAB_ID.

**PK:** SOCIAL_TAB_PERMISSION_ID · **Unique:** (TENANT_ID, SOCIAL_ID, TAB_ID)

| Coluna | Tipo | Null | Finalidade | Valores | Ref |
|---|---|---|---|---|---|
| 🔑 `SOCIAL_TAB_PERMISSION_ID` | bigint | N | Chave primária. |  |  |
| `TENANT_ID` | bigint | N | Tenant (empresa) da permissão. |  | FDN_TENANT.TENANT_ID |
| `SOCIAL_ID` | bigint | N | Perfil social ao qual a permissão de aba se aplica. |  | SOCIAL.ID |
| `TAB_ID` | varchar(255) | N | Aba controlada (enum SocialTabType, gravado como texto). | NOCODE_FORMS_APP=aba de formulários no-code |  |
| `TAB_PERMISSION_TYPE` | varchar(255) | N | Nível de acesso à aba (enum SocialTabPermissionType, texto). | FREE=livre; PARTIAL=parcial; RESTRICT=restrito |  |
| `TAB_ACTIVE` | bit(1) | N | Indica se a aba está ativa para o perfil. | 1=ativa; 0=inativa |  |

**Relacionamentos (saem desta tabela):**

- `(SOCIAL_ID)` → **SOCIAL** `(ID)` · N:1 · physical-fk/confirmed — Perfil social dono da permissão (jpa-join SocialTabPermission.social).

**Dicas de consulta:** Filtre por TENANT_ID e SOCIAL_ID.
