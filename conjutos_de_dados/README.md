# Conjuto de Dados de testes neuropsicológicos em Português do Brasil com de unidades de informação

Os dados destes conjunto de dados foram coletados junto a participantes de estudos e pesquisas clinicas ou acadêmicas,  mediante leitura e assinatura de Termo de Consentimento Livre e Esclarecido, tendo a pesquisa sido avaliada e aprovada pelos Comitês de Éticas em Pesquisas das instituições à que se encontram vinculadas. Declara-se que os conjunto de dados com os dados dos participantes estão sendo disponibilizado com total sigilo da identidade dos participantes, não contendo seus nomes ou números de documentos, ou qualquer outra informação que permita sua identificação individual não garanta o sigilo da identidade dos participantes. Os presentes conjunto de dados tem o objetivo único e exclusivo de servir de fonte para pesquisas e/ou estudos acadêmicos, para fins clínicos, ou de mesma natureza, sendo explicitamente vedado o seu uso para finalidades comerciais ou outras que não especificados neste documento, outros fins que não estes, sob pena de aplicação das punições previstas em lei. O usuário dos dados aqui contidos declara conhecimento e concordância com estas condições, sob pena de responsabilização e aplicação das penalidades previstas em lei.  Portanto, seu uso por terceiros pode apenas ser feito com os mesmos fins, quais sejam de pesquisa e clínicos, sendo indevido outro fim (**Licença CC-BY-SA-NC**).

## História da Carteira - ABCD (Arizona Battery for Communication Disorders)
O ABCD é uma bateria de teste padronizada para avaliação e triagem abrangentes da demência. Inclui 17 subtestes que avaliam a expressão lingüística, a compreensão lingüística, a memória episódica verbal através da lembrança imediata / atrasada de histórias, construção visuoespacial e status mental.

O subteste que é importante para o nosso estudo é a avaliação da memória episódica, composta pela recontagem imediata e tardia de uma história memorizada, a História da Carteira. Esta história foi traduzida e adaptada para o português do Brasil por Danielle Rüegg, Isabel Maranhão de Carvalho, Leticia Lessa Mansur e Márcia Radanovic, e foi aplicada e coletada pela equipe coordenada pela professora Leticia Lessa Mansur na Faculdade de Medicina da Universidade de São Paulo a 23 idosos com CCL e 12 adultos saudáveis; totalizando 70 narrativas. Este teste possui 17 unidades de informação, com possíveis alternativas, sendo 17 a sua pontuação máxima. 

Esse conjunto de dados consiste em 70 narrativas de falantes do português do Brasil, 12 controle e 23 MCI amnéstico (aMCI) diagnosticados na Faculdade de Medicina da Universidade de São Paulo. Foi aplicado e coletado pela equipe coordenada pela **Professora Dra. Leticia Lessa Mansur** da Faculdade de Medicina da Universidade de São Paulo. A tabela abaixo apresenta as estatísticas do conjunto de dados.


| Grupo | Pacientes | Narrativa |<p>Média Sentenças<br>value  (Desvio Padrão)</p>  | <p>Média de palavras por sentença <br> (Desvio Padrão) </p> |
|------|------|------|------|------|
| MCI | 23 | 46 | 8,17 (1,92) | 60,76 (17,39) |
| Controle |12 | 24 | 7,67 (2,06) | 58,96 (14,73)|

O conjunto está disponivel no arquivo `abcd_dataset.csv`, onde cada linha é uma sentença do reconto, a coluna *ínviduo* contém um indentificador único para o ínviduo, a coluna *reconto* indica se a narrativa é imediatamente (1) ou depois de 30 minutos (2), a coluna *grupo* indica qual grupo o paciente pertence (CCL ou Controle), a coluna *sentença* contém a *sentença* que foi segmentada manualmente, e as demais colunas indicam se a unidade de informação foi recordada ou não.

## História da Lucia - BALE
A BALE (Bateria de Avaliação da Linguagem no Envelhecimento) é uma bateria padronizada com normas para os idosos saudáveis analfabetos da população brasileira, com baixa (2 a 8 anos de escolaridade) e alta (9 anos ou mais), de 60 a 90 anos.
O BALE fornece à academia e à clínica tarefas padronizadas e validadas, preenchendo uma lacuna importante em termos de tarefas validadas para o português do Brasil, especialmente no nível do discurso. Foi concebido pela adaptação de outras tarefas, de acordo com critérios psicolinguísticos, incluindo imaginação, frequência, animação, extensão, entre outros, como questões culturais. Consiste em 10 tarefas linguísticas, avaliando desde o nível da palavra, na tarefa de nomeação, por exemplo, até o nível do discurso. Um de seus diferenciais é avaliar o discurso em quatro tipos de textos narrativos, principalmente no nível da produção, mas também com a compreensão textual implícita. Essa bateria foi escolhida porque seu objetivo é permitir sua administração a idosos analfabetos e / ou com baixa escolaridade, que representam a maioria da amostra de idosos atendidos pelo sistema público de saúde no Brasil. 

Esse conjunto de dados consiste em 69 narrativas de falantes do português do Brasil, 53 controle, 23 MCI amnéstico (aMCI), 11 com Doença de Alzheimer diagnosticados na Faculdade de Medicina da Universidade de São Paulo. O conjunto de dados foi coletado pela equipe coordenada pela **Professora Dra. Lilian Cristine Hübner**, da Escola de Humanidades da Pontifícia Universidade Católica (PUC) do Rio Grande do Sul, PUCRS. A tabela abaixo apresenta as estatísticas do conjunto de dados

| Grupo | Pacientes | Narrativa |<p>Média Sentenças<br>value  (Desvio Padrão)</p>  | <p>Média de palavras por sentença <br> (Desvio Padrão) </p> |
|------|------|------|------|------|
| AD  | 11 |11 | 6,09 (2,63) |  36,18 (17,10) | 
| MCI | 5 | 5 | 6,00 (1,00) | 36,40 (5,68) |
| Controle | 53 | 53 | 7,68 (2,67) | 52,06 (19,18)|

O conjunto está disponivel no arquivo `bale_dataset.csv`, onde cada linha é uma sentença do reconto, a coluna *ínviduo* contém um indentificador único para o ínviduo, a coluna *grupo* indica qual grupo o paciente pertence (CCL ou Controle), a coluna *sentença* contém a sentença que foi segmentada manualmente, e as demais colunas indicam se a unidade de informação foi recordada ou não.
