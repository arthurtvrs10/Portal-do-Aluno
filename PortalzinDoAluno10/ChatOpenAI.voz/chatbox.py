import json
import os
import sounddevice as sd
import speech_recognition as sr
import numpy as np
from scipy.io.wavfile import write
import tempfile

def carregar_faq():
    if os.path.exists("faq.json"):
        with open("faq.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def salvar_faq(faq):
    with open("faq.json", "w", encoding="utf-8") as f:
        json.dump(faq, f, ensure_ascii=False, indent=4)

def ouvir():
    print("Gravando... Fale agora!")
    fs = 44100  # Taxa de amostragem
    duration = 5  # Duração em segundos
    recognizer = sr.Recognizer()

    try:
        # Grava o áudio
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()

        # Cria um arquivo temporário para salvar o áudio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
            tmpfile_name = tmpfile.name
            write(tmpfile_name, fs, recording)

            print(f"Áudio gravado em: {tmpfile_name}")

            # Usando o arquivo temporário para reconhecimento de fala
            with sr.AudioFile(tmpfile_name) as source:
                print("Reconhecendo...")
                audio = recognizer.record(source)  # Lê o áudio do arquivo
                texto = recognizer.recognize_google(audio, language="pt-BR")
                print("Você disse:", texto)
                return texto
    except Exception as e:
        print(f"Erro no reconhecimento de voz: {e}")
        return ""

def treinar_bot(faq):
    print("Modo de treinamento iniciado. Digite ou diga 'sair' para sair.")
    while True:
        # Pergunta pode ser digitada ou falada
        escolha = input("Você quer usar voz ou texto? (Digite 'voz' ou 'texto'): ").strip().lower()

        if escolha == "voz":
            pergunta = ouvir()
        else:
            pergunta = input("Digite a pergunta: ").strip()

        if pergunta.lower() == "sair":
            break

        # Resposta pode ser digitada ou falada
        escolha_resposta = input("Você quer usar voz ou texto? (Digite 'voz' ou 'texto'): ").strip().lower()
        
        if escolha_resposta == "voz":
            resposta = ouvir()
        else:
            resposta = input("Digite a resposta: ").strip()

        if not pergunta or not resposta:
            print("Pergunta ou resposta inválida! Tente novamente.")
            continue

        faq[pergunta] = resposta
        print("Treinamento concluído!")
    salvar_faq(faq)

def chatbot(faq):
    print("Chatbot: Olá! Sou seu assistente virtual. Pergunte algo ou digite 'sair' para encerrar.")
    while True:
        escolha = input("Você quer usar voz ou texto? (Digite 'voz' ou 'texto'): ").strip().lower()

        if escolha == "voz":
            entrada_usuario = ouvir()
        else:
            entrada_usuario = input("Você: ").strip()

        if entrada_usuario.lower() in ["sair", "tchau", "adeus"]:
            print("Chatbot: Até logo! Espero ter ajudado.")
            break
        elif entrada_usuario in faq:
            print(f"Chatbot: {faq[entrada_usuario]}")
        else:
            print("Chatbot: Hmm, eu ainda não sei responder isso. Você pode me ensinar?")
            treinar_bot(faq)

def principal():
    faq = carregar_faq()
    while True:
        print("\nEscolha uma opção:")
        print("1. Iniciar chat")
        print("2. Treinar chatbot")
        print("3. Sair")
        escolha = input("Escolha: ").strip()

        if escolha == "1":
            chatbot(faq)
        elif escolha == "2":
            treinar_bot(faq) 
        elif escolha == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    principal()

def realizar_acao(entrada):
    entrada = entrada.lower().stript()

    if "pesquisar" in entrada  and "no youtube" not in entrada:
        query = entrada.replace("pesquisar", "").strip()
        webbrowser.open(f"https://www.google.com/search?q=(query)")


    if "pesquisar" in entrada  and "no youtube" not in entrada:
        query = entrada.replace("pesquisar", "").strip()
        webbrowser.open("https://www.instagram.com")
        return "Abrindo o instagram"


