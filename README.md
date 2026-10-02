# Material Codex

Biblioteca de referência de materiais da Factory Toolbox. Pesquisa por material, liga, fórmula ou CAS, filtros por família e propriedade, comparação de até quatro fichas, CSV e impressão em PDF.

- Site: https://guizlass-afk.github.io/MaterialCodex/
- Portal: https://guizlass-afk.github.io/FactoryToolbox/
- Diretório canônico compartilhado: `Z:\Projetos\Material Codex`.
- 12 idiomas com bandeiras, leitura RTL em árabe e temas claro/escuro. Preferências armazenadas apenas no navegador.

## Catálogo inicial

60 fichas, 466 propriedades documentadas diretamente em fontes, em seis famílias: metais/ligas, polímeros, cerâmicas, gases, líquidos criogênicos e compósitos. O catálogo é inicial e não pretende cobrir todos os materiais existentes. Há fichas com propriedades ausentes: ausência nunca significa zero.

Fontes: Outokumpu (Core/Supra), Hydro (6061), Copper Development Association (C11000), Ovako (C45/42CrMo4), TIMET (Ti-6Al-4V), Curbell Plastics, CoorsTek e Air Liquide. Cada ficha e cada propriedade apontam para a fonte. Não se usa conteúdo remoto em tempo de execução.

Graus, produtos, tratamentos e métodos são preservados. Valores típicos, limites mínimos/máximos e faixas têm rótulos distintos. As normas mencionadas são as citadas nas fichas consultadas, sem promessa de atendimento à edição normativa atual. A ficha TIMET é histórica (2000). Propriedades de um produto comercial não são generalizadas para todos os materiais com a mesma base química.

A composição contém os constituintes disponibilizados pela fonte, podendo omitir traços e aditivos. Não constitui certificado químico. Fórmula/base polimérica não informa proporção de aditivos. Os resultados não estabelecem equivalência entre graus ou normas. Em polímeros, a densidade relativa publicada não é convertida silenciosamente em massa específica.

## Cálculos e unidades

- Peso específico: `gamma [kN/m³] = density [kg/m³] × 9.80665 / 1000`, gravidade convencional.
- Condutividade elétrica: `sigma [S/m] = 1 / resistivity [ohm·m]`.
- Quando só há IACS: `sigma [S/m] = IACS [%] × 580000`, usando 100% IACS = 58 MS/m; referência CDA ligada junto à fórmula.
- Recíprocos invertem a ordem dos extremos e o sentido de desigualdades. Condições e qualificadores de origem são mantidos.
- Valores calculados são separados dos 466 valores do catálogo. A precisão de exibição não equivale à incerteza de medição.
- Não são misturadas condições para inferir propriedades ausentes. Flexão não é tração; módulo de flexão não é módulo de Young; líquido criogênico não é gás a 25 °C.

O CSV usa UTF-8 com BOM, números canônicos com ponto decimal, unidades, condições, qualificadores, fonte e data. Inclui composição e fórmulas explicativas dos cálculos; não é uma planilha XLSX com fórmulas executáveis. Células textuais que possam ser interpretadas como fórmulas são protegidas. Campos ausentes não são exportados como zero.

## Desenvolvimento e verificação

Aplicação estática, sem build JavaScript e sem dependências de terceiros em execução. Sirva esta pasta com um servidor HTTP estático.

```powershell
python scripts/build_catalog.py
python scripts/build_i18n.py
python -m http.server 8080
```

`materials.json` e `materials.js` são gerados de `scripts/build_catalog.py`. `i18n.js` é gerado de `i18n-source.json`. Adicione novos dados somente após conferir fonte, condição e unidade; não preencha lacunas por estimativa não rotulada.

Testes: Python, Playwright e Google Chrome instalado.

```powershell
python tests/test_app.py
```

Cobertura: todas as fichas, referências de cálculo independentes, limites e conversões, busca/CAS, filtros combinados, comparação persistida, download CSV, 12 idiomas, quatro larguras, teclado, RTL, temas e impressão. Capturas de tela são gravadas no diretório temporário do sistema.

## Direitos

Código original: todos os direitos reservados, conforme `LICENSE`. Valores factuais são acompanhados das fontes; marcas, nomes comerciais e documentos vinculados pertencem aos respectivos titulares. As folhas técnicas originais não são redistribuídas.
