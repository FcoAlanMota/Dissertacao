# Dissertacao
Neste repositório estão os algoritmos utilizados em minha dissertação intitulada "LOCALIZAÇÃO E NAVEGAÇÃO DE ROBÔS MÓVEIS INDOOR BASEADAS EM VISÃO COMPUTACIONAL E REDES DE PETRI " e vídeo explicativo.
1. AIP: algoritmo de identificação de portas. Foi anexada ao lado da porta uma baliza no formato de círculo de 10 cm de diâmetro na cor vermelha, bem como um QRcode com comprimento e largura de 10 cm, como está representado na figura.
2. ALM: algoritmo de localização e mapeamento simultâneo. Para os testes de geração do mapa topológico, é necessário que o algoritmo detecte o id de cada porta do ambiente via técnicas de visão computacional, a partir das imagens fornecidas ou, manualmente, o usuário pode fornecer ao ALM, sempre que este solicita, via tela do computador onde o algoritmo está sendo executado, a quantidade de portas e a identificação (id) de cada porta contida no cômodo analisado. Os dados quantidade de portas e id são fornecidos por meio da IDLE Shell Python obedecendo, respectivamente, a seguinte estrutura: k, sendo k = 1, 2, ··· e txy , em que t representa uma transição que liga dois lugares da RP, x é o índice que representa o lugar de saída e y é o índice que representa o lugar de entrada. 
3. Vídeo explicativo: mostra o passo a passo para a geração, via ALM, de um mapa topológico, em formato de rede de Petri, que representa um ambiente explorado. 
