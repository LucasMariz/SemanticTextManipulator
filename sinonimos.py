import spacy
import requests
import random
from bs4 import BeautifulSoup
import requests
import json

class Token:
    def __init__(self, text, pos_tag):
        self.text = text
        self.pos_tag = pos_tag

# modelo de língua portuguesa
nlp = spacy.load("pt_core_news_sm")

# tokeniza e classifica gramaticalmente um texto
def analise_lexica(texto):
    doc = nlp(texto)
    tokens = []
    for token in doc:
        # Verifica se o token é pontuação
        if token.is_punct:
            continue
        if token.pos_ == 'DET' or not token.is_stop:
            tokens.append(Token(token.text, token.pos_))
    return tokens


def obter_sinonimos(palavra):
    url = f"http://www.sinonimos.com.br/{palavra}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        sinonimos_container = soup.find_all('a', class_='sinonimo')
        sinonimos = [sinonimo.get_text() for sinonimo in sinonimos_container]
        print(f"Sinônimos encontrados para '{palavra}': {sinonimos}")  # Debug: imprime sinônimos encontrados
        return sinonimos
    print(f"Falha ao buscar sinônimos para '{palavra}', status code: {response.status_code}")  # Debug: imprime falha
    return []

def aplicar_regras_de_modificacao(tokens):
    tokens_modificados = []
    for token in tokens:
        if token.pos_tag in ['NOUN', 'ADJ']:  # Aplica sinônimos a substantivos e adjetivos
            sinonimos = obter_sinonimos(token.text)
            if sinonimos:
                sinonimo_escolhido = random.choice(sinonimos)
                token_modificado = Token(sinonimo_escolhido, token.pos_tag)
                tokens_modificados.append(token_modificado)
                continue
        tokens_modificados.append(token)
    return tokens_modificados


def consume(expected_tag, tokens):
    if tokens and tokens[0].pos_tag == expected_tag:
        return tokens.pop(0)
    else:
        raise Exception(f"Expected {expected_tag} but got {tokens[0].pos_tag if tokens else 'no tokens left'}")

def parse_sintagma_nominal(tokens):
    if tokens and tokens[0].pos_tag == 'DET':
        det = consume('DET', tokens)  # Consome o artigo
        if tokens and tokens[0].pos_tag == 'NOUN':
            noun = consume('NOUN', tokens)  # Consome o substantivo
            return [det, noun]
    elif tokens and tokens[0].pos_tag == 'NOUN':
        return [consume('NOUN', tokens)]  # Consome substantivo sem artigo
    return []

def parse_sintagma_verbal(tokens):
    if tokens and tokens[0].pos_tag == 'VERB':
        verb = consume('VERB', tokens)  # Consome o verbo
        # Agora permite que siga um NOUN ou outro VERB, dependendo da estrutura desejada
        if tokens and tokens[0].pos_tag in ['NOUN', 'VERB', 'PRON']:
            following = consume(tokens[0].pos_tag, tokens)  # Consome o próximo token que pode ser NOUN ou VERB
            return [verb, following]
        return [verb]
    return []

def reorganizar_sentenca(sn, sv):
    # Reorganiza alternando a ordem dos sintagmas
    return sv + sn

def parse_sentenca_com_modificacao(tokens):
    sn = parse_sintagma_nominal(tokens)
    sv = parse_sintagma_verbal(tokens) if tokens else []
    # Reorganiza a sentença invertendo a ordem dos sintagmas
    sentenca_reorganizada = reorganizar_sentenca(sn, sv)
    # Aplica as modificações de sinônimos na sentença reorganizada
    return aplicar_regras_de_modificacao(sentenca_reorganizada)



def google_search(query, api_key, cse_id, num=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': cse_id,
        'key': api_key,
        'num': num
    }
    response = requests.get(url, params=params)
    result_data = response.json()
    print("Response from Google Search:", result_data)  # Debug: imprime a resposta completa
    if 'items' in result_data:
        return [(item['title'], item['link']) for item in result_data['items']]
    else:
        return []




# Exemplo de uso
texto = "O professor aprova o projeto."
tokens = analise_lexica(texto)
print("Tokens antes da modificação:", [(token.text, token.pos_tag) for token in tokens])

try:
    modified_sentence = parse_sentenca_com_modificacao(tokens)
    print("Sentença Modificada:")
    # Cria a string modificada a partir dos tokens modificados
    modified_text = ' '.join([token.text for token in modified_sentence])
    print(modified_text)

    # realiza uma pesquisa no Google
    api_key = "AIzaSyCTP8dIaNgNlz15fOXOxdmosBuQeFSFZl0"
    cse_id = "5177675503cfc4173"
    search_results = google_search(modified_text, api_key, cse_id)
    print("Search Results:", search_results)
    for title, link in search_results:
        print(f"Title: {title}\nLink: {link}\n")
except Exception as e:
    print(str(e))
