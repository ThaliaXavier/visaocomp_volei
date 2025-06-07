import cv2
import numpy as np

def selecionar_rois(imagem):
    rois = []
    while True:
        img = imagem.copy()
        cv2.namedWindow('ROI', cv2.WINDOW_NORMAL)
        cv2.imshow('ROI', img)
        roi = cv2.selectROI('ROI', img, fromCenter=False, showCrosshair=True)
        if roi == (0, 0, 0, 0):
            break
        rois.append(roi)
        cv2.destroyWindow('ROI')
        print("Pressione 'q' para sair ou qualquer outra tecla para selecionar outra região.")
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    return rois

def capturar_quadro_do_video(caminho_video, numero_quadro):
    cap = cv2.VideoCapture(caminho_video)
    cap.set(cv2.CAP_PROP_POS_FRAMES, numero_quadro)
    ret, quadro = cap.read()
    cap.release()
    return quadro

caminho_video = 'vagas/volei.mp4'

numero_quadro = 100  

quadro = capturar_quadro_do_video(caminho_video, numero_quadro)

rois = selecionar_rois(quadro)

for i, roi in enumerate(rois):
    x, y, largura, altura = roi
    print(f"Região de interesse {i+1}: x={x}, y={y}, largura={largura}, altura={altura}")

    imagem_roi = quadro[y:y+altura, x:x+largura]

    cv2.imshow(f'ROI {i+1}', imagem_roi)
    cv2.waitKey(0)
    cv2.destroyWindow(f'ROI {i+1}')
