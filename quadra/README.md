# Monitoramento de Bolas em Quadra de Vôlei com Visão Computacional

## 1. Introdução

Este projeto propõe o uso de **técnicas de visão computacional** para monitorar, por meio de um **vídeo gravado**, a posição da **bola de vôlei** em relação à área delimitada da quadra. A detecção é baseada na coloração predominante da bola (amarelo), e o sistema determina, em tempo real durante a reprodução do vídeo, se a bola está **dentro** ou **fora** da quadra. Este tipo de aplicação pode ser útil para análises táticas e à arbitragem esportiva.

## 2. Objetivo

Desenvolver um sistema que analise automaticamente um vídeo de uma partida de vôlei, detectando a bola e verificando se ela está fora da quadra. O sistema deve apresentar visualmente o status ("BOLA DENTRO" ou "BOLA FORA") sobre o vídeo.

## 3. Metodologia

### 3.1 Definição da Região da Quadra

A área da quadra é definida manualmente no código como uma **região retangular**. Os valores das coordenadas foram obtidos manualmente a partir de um quadro estático do vídeo:

```python
QUADRA = [
    [583, 395, 2629, 1315]
]
```

Esses valores representam, respectivamente, a posição x, y, a largura (w) e a altura (h) da quadra.

### 3.2 Processamento do Quadro

Cada quadro do vídeo é processado por meio da função `processa_frame(img)`, que executa as seguintes etapas:

1. **Conversão para escala de cinza**: simplifica a imagem reduzindo a quantidade de dados.
2. **Limiar adaptativo**: gera uma imagem binária onde as áreas de interesse (diferenças de intensidade) são realçadas.
3. **Filtro de mediana**: reduz ruídos preservando bordas.
4. **Dilatação**: destaca áreas brancas (contornos ou objetos), facilitando a detecção posterior.

Três versões intermediárias da imagem são retornadas: cinza, threshold e dilatada.

### 3.3 Detecção da Bola

A função `verifica_bola_fora(img, quadra)` identifica se a bola está fora da área da quadra. O processo segue os seguintes passos:

* Conversão da imagem para o espaço de cor HSV.
* Aplicação de uma máscara para tons de **amarelo**, correspondente à bola.
* Extração de contornos e cálculo do **círculo mínimo envolvente** para identificar a bola.
* Se o centro da bola estiver fora da região da quadra, exibe “BOLA FORA!”.
* Caso nenhuma bola seja detectada no quadro, o sistema também assume que está fora da quadra.

### 3.4 Exibição do Status

A função `exibe_status(img, fora)` desenha uma tarja preta no canto superior esquerdo do vídeo e exibe o status da jogada:

* **“BOLA DENTRO”**, em verde.
* **“BOLA FORA”**, em vermelho.

## 4. Execução do Sistema

O vídeo é carregado e processado quadro a quadro com `cv2.VideoCapture`. A cada ciclo:

* O quadro é processado.
* A presença da bola é verificada.
* O status é exibido sobre o vídeo.

## 5. Requisitos

* Python 3
* Bibliotecas:

  * OpenCV (`opencv-python`)
  * NumPy

Instalação recomendada:

```bash
pip install opencv-python numpy
```

Como inicializar o projeto:

Rode o comando:
   python quadra/main.py

A execução pode ser encerrada a qualquer momento com a tecla `q`.

## 6. Considerações Finais

Este projeto demonstra como é possível utilizar técnicas simples de visão computacional para resolver um problema comum no contexto esportivo.


