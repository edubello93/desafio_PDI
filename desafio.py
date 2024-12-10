import numpy as np
import cv2 as cv
import os 
from deepface import DeepFace
import datetime
import pyautogui

# o programa capta o video da webcam, salva a imagem de cada frame e
# analisa a principal expressão facial de cada frame com o DeepFace

#abre webcam
cap = cv.VideoCapture(0)
#fecha o programa se a webcam nao abrir
if not cap.isOpened():
    print("Cannot open camera")
    exit()

#Define o codec e cria o objeto VideoWriter
tempo_atual = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
print ("debug: inicio main ", tempo_atual)
fourcc = cv.VideoWriter_fourcc(*'XVID')

#configuração da gravacao do video da webcam: com 20FPS e resolucao 640x480
out = cv.VideoWriter(f'{tempo_atual}.avi', fourcc, 20.0, (640,  480))
quantidade_frames= 0


resolution = (800 , 600)
# Specify video codec
codec = cv.VideoWriter_fourcc(*"XVID")
# Specify name of Output file
filename = "Recording.avi"
# Specify frames rate. We can choose 
# any value and experiment with it
fps = 20.0
 
# Creating a VideoWriter object
outTela = cv.VideoWriter(filename, codec, fps, resolution)


#loop de gravacao
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # se o frame esta sento lido certo, ret é True
 
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    #grava video    
    out.write(frame)

    """
    #GRAVAR A TELA
     # Take screenshot using PyAutoGUI
    img = pyautogui.screenshot()
 
    # Convert the screenshot to a numpy array
    tela = np.array(img)
 
    # Convert it from BGR(Blue, Green, Red) to
    # RGB(Red, Green, Blue)
    tela = cv.cvtColor(tela, cv.COLOR_BGR2RGB)
 
    # Write it to the output file
    outTela.write(tela)
     
    # Optional: Display the recording screen
    cv.imshow('Live', tela)
"""

    cv.imshow('frame', frame)
    #apertar Q para parar a gravação
    if cv.waitKey(1) == ord('q'):
        break
 
# Terminada a gravação, liberar a camera
cap.release()
out.release()
#outTela.release()
cv.destroyAllWindows()


#função pra extrair cada frame do video 
def FrameCapture(path): 
    
    print("inicio framecapture ", datetime.datetime.now())
    # Path da gravação 
    vidObj = cv.VideoCapture(path) 
  
    # contador de frames 
    count = 0
    
    #criar pasta para colocar os frames
    nome_pasta = f"C:/Facul/PDI/DESAFIO/tentativa2/{tempo_atual}"
    os.mkdir(nome_pasta)
    print("pasta dos frames criada")
    #verifica se acabou o video 
    success = 1
    
    while success: 
  
        # objeto vidObj chama a leitura 
        # a funcao extrai os frames 
        success, image = vidObj.read() 
        if success == False:
            break
            
        #salva os frames com o contador no nome do arquivo 
        cv.imwrite(f"{nome_pasta}/frame{count}.jpg", image) 
  
        count += 1
        print(count)
        
    
    print ("Fim da captura de frames")
    Analise(nome_pasta)
    
    
#analisa a expressao dos frames    
def Analise(path):
    print ("Inicio analise dos frames", datetime.datetime.now())
    
    count = 0      
    #loop pra passar pelos arquivos de imagem
    while True:
      
      demography = DeepFace.analyze(img_path=f"{path}/frame{count}.jpg",
      #o deepface consegue analisar idade, genero, raca e emocao.
      #mas aqui só usaremos a emocao
      
      #actions = ['age', 'gender', 'race', 'emotion'],
      actions = ['emotion'],
      enforce_detection= False)
      
      #imprime a emoção dominante de cada frame
      print("Frame:", count, demography[0]['dominant_emotion'])
      count += 1



# Driver Code 
if __name__ == '__main__': 
    print("inicio????")
    print(f'{tempo_atual}.avi')
    # Calling the function 
    FrameCapture(f'{tempo_atual}.avi') 
    Analise()