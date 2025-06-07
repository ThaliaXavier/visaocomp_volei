import cv2
import numpy as np

QUADRA = [
    [583, 395, 2629, 1315] 
]


DELAY = 10

def processa_frame(img):
    """
    Destaca as áreas de interesse.
    """
    img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_threshold = cv2.adaptiveThreshold(img_cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    img_blur = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.int8)
    img_dil = cv2.dilate(img_blur, kernel)
    return [img_dil, img_cinza, img_threshold]

def verifica_bola_fora(img, quadra):
    """
    Verifica se a bola amarela está fora da área da quadra.
    Se nenhuma bola for detectada, ela está fora.
    """
    
    quadra = quadra[0]
    x, y, w, h = quadra

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    amarelo_claro = np.array([20, 100, 100])
    amarelo_escuro = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, amarelo_claro, amarelo_escuro)

    contornos, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    bola_naodetectada = False

    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 50:
            bola_naodetectada = True
            (cx, cy), raio = cv2.minEnclosingCircle(contorno)
            centro = (int(cx), int(cy))
            cv2.circle(img, centro, int(raio), (0, 255, 255), 2)

           
            if not (x <= cx <= x + w and y <= cy <= y + h):
                cv2.putText(img, 'BOLA FORA!', (100, 100), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 4)
                return True 

    if not bola_naodetectada:
        cv2.putText(img, 'BOLA FORA', (100, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 3)
        return True

    return False  



def exibe_status(img, fora):
    
    cv2.rectangle(img, (90, 0), (500, 60), (0, 0, 0), -1)
    status = 'BOLA FORA' if fora else 'BOLA DENTRO'
    cor = (0, 0, 255) if fora else (0, 255, 0)
    cv2.putText(img, status, (100, 45), cv2.FONT_HERSHEY_DUPLEX, 1.5, cor, 4)



def main():
    video_path = 'quadra/volei.mp4'
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"Erro ao abrir o vídeo: {video_path}")
        return

    while True:
        check, img = video.read()
        if not check:
            break
        img_dil, img_cinza, img_threshold = processa_frame(img)

        img_cinza_small = cv2.resize(img_cinza, (0, 0), fx=0.5, fy=0.5)
        img_threshold_small = cv2.resize(img_threshold, (0, 0), fx=0.5, fy=0.5)
        img_dil_small = cv2.resize(img_dil, (0, 0), fx=0.5, fy=0.5)

    
        fora = verifica_bola_fora(img, QUADRA)
        exibe_status(img, fora)


        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Video', 910, 510)  
        cv2.imshow('Video', img)

        cv2.namedWindow('Cinza', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Cinza', 480, 270)
        cv2.imshow('Cinza', img_cinza_small)

        cv2.namedWindow('Threshold', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Threshold', 480, 270)
        cv2.imshow('Threshold', img_threshold_small)

        cv2.namedWindow('Dilatada', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Dilatada', 480, 270)
        cv2.imshow('Dilatada', img_dil_small)


        if cv2.waitKey(DELAY) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
