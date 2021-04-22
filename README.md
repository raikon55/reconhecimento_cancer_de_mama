Reconhecimento de padrões por textura em imagens mamógraficas
---

Trabalho para disciplina de Processamento de imagens do curso de Engenharia de computação da PUC Minas.

### Contextualização
```
A densidade da mama é comprovadamente relacionada com o risco de desenvolvimento
de câncer, uma vez que mulheres com uma maior densidade mamária podem esconder
lesões, levando o câncer a ser detectado tardiamente. A escala de densidade chamada
BIRADS foi desenvolvida pelo American College of Radiology e informa os radiologistas
sobre a diminuição da sensibilidade do exame com o aumento da densidade da mama.
BI-RADS definem a densidade como sendo quase inteiramente composta por gordura (densidade I),
por tecido fibroglandular difuso (II), por tecido denso heterogênero (III) e por tecido
extremamente denso (IV). A mamografia é a principal ferramenta de rastreio do câncer e
radiologistas avaliam a densidade da mama com base na análise visual das imagens.
```

### Objetivo Geral
```
Implementar um aplicativo que leia imagens de exames mamográficos e possibilite o
reconhecimento automático da densidade da mama, utilizando técnicas de descrição por textura.
```

### Objetivos especifícos

* Primeira parte:
    - [x] Ler e visualizar imagens pelo menos nos formatos PNG e TIFF. As imagens podem ter qualquer resolução e número de tons de cinza
    - [ ] Exibir a imagem em uma janela, com opção de zoom;
    - [ ] Selecionar com o mouse uma região de interesse de 128 x 128 pixels a ser reconhecida. Mostrar o contorno da região na cor azul;
    - [x] Oferecer uma opção para diminuir a resolução da região para 64 x 64 ou 32 x 32 pixels exibindo o resultado;
    - [x] Oferecer uma opção para diminuir a quantização da região para 256, 32 ou 16 tons de cinza, exibindo o resultado;
    - [ ] Oferecer opção para equalizar a região selecionada.

### Desenvolvimento

Para alcançar o objetivo do trabalho, foi escolhido a biblioteca
[Pillow](https://python-pillow.org/) que tem como foco a manipulação e processamento de imagens.
Para a criação da interface gráfica, será usada a biblioteca [PySide6](https://doc.qt.io/qtforpython-6) pela facilidade de implementação.

#### Biblioteca para manipular a imagem através do PIL

A classe ImageHandler é responsável por receber os eventos da interface gráfica, e manipular a o objeto da imagem
carregada em memória.

ImageHandler possui 9 métodos:
 * `get_image(original: bool)`: Responsável por retornar a referência da imagem carregada na interface, ou a referência
  da imagem original, de acordo com o valor passado para `original`(Por padrão, o valor é False)
 * `get_file_path()`: Retorna o caminho do arquivo da imagem
 * `normalize(image: Image)`: Redimensiona a imagem para ser exibida na interface gráfica
 * `zoom_in(region: tuple(0, 0))`: Aplica um zoom de 128x128 pixeis na imagem, de acordo com a
   região informada (Por padrão, a região começa no canto superior esquerdo (0, 0))
 * `zoom_out()`: Remove o zoom aplicado por `zoom_in`
 * `new_resolution(new_size: int)`: Redimensiona a imagem
 * `temporary_image(is_zoom: bool)`: Método auxiliar para aplicar zoom na imagem
 * `get_info()`: Exibe no console informações sobre a imagem que foi carregada. As informadas são:
   - Resolução,
   - Número de colunas,
   - Número de linhas,
   - Tipo do arquivo,
   - Tipo da imagem.
 * `close()`: Fecha todas as imagens abertas