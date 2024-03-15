import socket
import pyaudio

# Configurações de conexão
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# Configurações de áudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def enviar_audio(s, stream):
    while True:
        data = stream.read(CHUNK)
        s.sendall(data)

def receber_audio(s, stream):
    while True:
        data = s.recv(CHUNK)
        stream.write(data)

def main():
    # Inicializa o socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))

    # Inicializa o PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    # Inicia as threads para enviar e receber áudio
    enviar_thread = threading.Thread(target=enviar_audio, args=(s, stream))
    receber_thread = threading.Thread(target=receber_audio, args=(s, stream))
    enviar_thread.start()
    receber_thread.start()

    enviar_thread.join()
    receber_thread.join()

    # Fecha a conexão e a stream do PyAudio
    s.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    main()
