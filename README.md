# Portuguese Text Modifier

Este projeto é uma ferramenta de modificação e análise de textos em português que realiza a tokenização, análise gramatical, substituição de sinônimos, reorganização de sentenças e pesquisa de informações relacionadas no Google.

## Funcionalidades

- **Análise Léxica**: Tokeniza e classifica gramaticalmente textos em português.
- **Substituição de Sinônimos**: Substitui substantivos e adjetivos por sinônimos adequados.
- **Reorganização de Sentenças**: Modifica a estrutura da sentença mantendo a coerência gramatical.
- **Integração com a API do Google**: Realiza buscas com base no texto modificado para encontrar informações relacionadas.

## Pré-requisitos

Antes de começar, você precisará:
- Python 3.6 ou superior.
- Biblioteca Spacy e seu modelo de língua portuguesa.
- Biblioteca BeautifulSoup4 para parsing de HTML.
- Biblioteca requests para chamadas de API.

## Instalação

1. Clone o repositório para a sua máquina local:
   ```bash
   git clone https://github.com/seu-usuario/PortugueseTextModifier.git
   ```

2. Instale as dependências necessárias:
   ```bash
   pip install spacy beautifulsoup4 requests
   ```

3. Baixe o modelo de língua portuguesa para o Spacy:
   ```bash
   python -m spacy download pt_core_news_sm
   ```
