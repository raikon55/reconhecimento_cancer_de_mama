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
    - [ ] Oferecer uma opção para diminuir a resolução da região para 64 x 64 ou 32 x 32 pixels exibindo o resultado;
    - [ ] Oferecer uma opção para diminuir a quantização da região para 256, 32 ou 16 tons de cinza, exibindo o resultado;
    - [ ] Oferecer opção para equalizar a região selecionada.

### Desenvolvimento

Para alcançar o objetivo do trabalho, foi escolhido a biblioteca
[Pillow](https://python-pillow.org/) que tem como foco a manipulação e processamento de imagens.
Para a criação da interface gráfica, será usada a biblioteca [PySide6](https://doc.qt.io/qtforpython-6) pela facilidade de implementação.
