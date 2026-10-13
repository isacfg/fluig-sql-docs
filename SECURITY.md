# Segurança

As ferramentas deste repositório fazem validação estática; não executam consultas nem gerenciam acesso ao banco. O catálogo usa o schema de instalação do Fluig 1.8.2 e não é uma garantia de autorização ou de segurança das queries de uma aplicação.

## Relatar uma vulnerabilidade

Para falhas nos scripts ou no validador que possam expor dados ou permitir que uma query perigosa seja aceita como correta, use **Security → Report a vulnerability** no GitHub, quando disponível. Se a opção não estiver disponível, abra uma issue apenas solicitando um canal privado ao mantenedor `@isacfg`; aguarde esse canal antes de compartilhar detalhes.

Inclua a versão/commit, comportamento observado, impacto e um exemplo mínimo com dados sintéticos. Não publique credenciais, dados de produção ou informações pessoais em issues.

Problemas do produto Fluig devem ser encaminhados ao fornecedor pelos canais de suporte correspondentes. Este projeto não recebe nem corrige vulnerabilidades do produto.

## Escopo de manutenção

Correções das ferramentas são aplicadas à branch `main`. Não há versões antigas das ferramentas com manutenção separada, nem prazo de resposta garantido. Correções de documentação e falsos positivos sem impacto sensível podem ser reportados nas issues comuns.
