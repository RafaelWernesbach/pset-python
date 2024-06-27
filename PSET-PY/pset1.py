# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Rafael Christian Silva Wernesbach
#    Matrícula: 202308237
#    Turma: cc3mb
#    Email: nkmnoff@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    # Abaixo temos a função para adiquirimos o indice do pixel, tem como argumentos x e y que referenciam o pixel em tupla
    def get_pixel(self, x, y): 
        if x < 0: x = 0 # Verifica se a cordenada x do pixel é menor que 0, caso seja, o valor do x < 0 será x
        if y < 0: y = 0 # Verifica se a cordenada y do pixel é menor que 0, caso seja, o valor de y < 0 será y
        if x >= self.largura: x = self.largura - 1 
        """ 
         Verifica se a cordenada x do pixel é maior que a largura maxima da imagem
         Caso sim, o valor de x será redefinido para o maior x possivel tendo em mente que
         o valor de x inicia em 0, e a largura em 1, temos então que x = largura - 1
        """
        if y >= self.altura: y = self.altura - 1
        """  
         Verifica se a cordenada y do pixel é maior que a altura maxima da imagem
         caso sim, o valor de y será redefinido para o maior y possivel tendo em mente que
         o valor de y inicia em 0, e a Altura em 1, temos então que y = Altura - 1
        """
 
        return self.pixels[x + (y * self.largura)] 
        """
        Utilizando a formula x + (y * largura) conseguimos transformar a tupla em um indice linear
        """

    # Abaixo temos a função para atribuimos um novo valor ao pixel, tem como argumentos x, y , c sendo x,y o pixel e c o valor da cor
    def set_pixel(self, x, y, c):
        """  
        Aqui o valor do pixel referenciado pelo indice adiquirido através da formula x + (y * largura)
        será substituido pelo valor de c(nova cor de pixel)
        """
        self.pixels[x + (y * self.largura)] = c

    # Abaixo temos a função para aplicarmos uma nova cor em cada pixel da imagem, tem como argumento uma função qualquer para alterar o valor da cor do pixel
    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura)
        """
        Criamos uma imagem nova com as mesmas dimensões da imagem original, então através
        de 2 loops for percorremos cada pixel da imagem.
        """
        for x in range(resultado.largura):            
            for y in range(resultado.altura):
                """
        Após encontrarmos o pixel em questão, criamos uma variavel chamada cor
        que representa o atual valor do pixel, logo em seguida criamos uma nova cor
        que terá o valor de cor após passar por uma função definida na função de inversão
                """
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)
                """
        Esse novo valor de cor agora entra como argumento(c) na função de set pixel.
        Assim a nova imagem "resultado" é modificada com os novos valores de pixels.
        Após isso essa nova imagem é retornada.
                """

        return resultado
 
    # Abaixo temos a nossa função de correlação que aceita um kernel e uma variavel de controle chamada ajuste como argumento
    def usar_kernel(self, kernel, ajuste):
        im = Imagem.nova(self.largura, self.altura)
        """
        Aqui novamente criamos uma nova imagem chamada de im, utilizamos 2 loops for para encontrar
        o pixel central que sofrerá a convolução
        """
        for x in range(self.largura):
            for y in range(self.altura):
                convolucao = self.calcular_convolucao(kernel, x, y)
                """
        Chamamos a função de convolução e passamos o valor de x, y representando o pixel central
        passamos também o kernel que será utilizado na convolução

        Com o valor da convolução em mãos podemos ir então para a checagem dos ajustes.
                
        Em alguns casos especificados no pset foi instruido para que não fossem realizados
        ajustes nos valores dos pixels de algumas imagens antes das operações especificadas 
        no pdf(como por exemplo a detecção de borda).

        Nesses casos a variavel apresentará necessidade de pular esse ajuste e irá realizar o set pixel em im sem nenhum ajuste
        podendo retornar valores fora da faixa aceitavel, ou valores não inteiros que serão posteriormente corrigidos em suas
        respectivas funções
                """
                if ajuste: 
                    im.set_pixel(x, y, round(convolucao))   
                    convolucao = self.ajustar_pixel(convolucao)
                else: im.set_pixel(x, y, convolucao)
                 
        """
        Então retornamos a a nova imagem agora com o kernel aplicado
        podendo ser diretamente utilizada como resultado nos testes
        ou ser utilizada em futuras operações caso se mostre necessario
        """
        return im
    # Abaixo temos nossa função para calcular a convolução, tem como argumentos x e y(pixe central) e o kernel utilizado
    def calcular_convolucao(self, kernel, x, y):

        convolucao = 0
        """
        Criamos uma variavel chamada convolução que será o resultado da operação
        então atribuimos ela a 0 para garantir que a cada iteração o valor seja calculado corretamente
        através de 2 loops for(c = coluna, l = linha) encontramos o "pixel" do kernel que usaremos.
        """
        for c in range(len(kernel)):
            for l in range(len(kernel)):
                """
        Finalmente então realizamos a operação, o calculo se baseia em somar o valor de x e y do pixel central 
        separadamente com c e l do pixel do kernel em questão, e subtraindo pela metade inteira (sempre arredondada para baixo) 
        da largura ou altura do kernel (como o kernel é quadrado não faz diferença), o resultado dessa operção é o indice do pixel
        no qual o pixel (c,l) está em cima, esse resultado é armazenado na variavel pixel_xy_cl.

        Um exemplo para melhor compreensão é imaginarmos uma imagem 5x5, queremos aplicar um kernel 3x3 nessa imagem, sendo assim
        vamos tomar o pixel central sendo o pixel (2,2) da imagem, ao aplicar o kernel sobre esse pixel temos que o pixel (0,0) do kernel
        estará sobre o pixel 1,1 da imagem, pois 1 - 0/(3 // 2 = 1) = 1(isso vale tanto para o x quanto para o y ja que ambos nesse exemplo
        possuem o mesmo valor).
                """
                
                pixel_xy_cl = self.get_pixel(x + c - (len(kernel) // 2), y + l - (len(kernel) // 2))

                """
        Aqui realizamos a multiplicação do valor do pixel do kernel com o valor do pixel xy cl e adicionando
        esse valor na variavel de convolução, essa operação será realizada até que tenham sido cobertos todos os pixels do kernel,
        então retornamos o valor da convolucao.
                """
                convolucao += kernel[c][l] * pixel_xy_cl
        return convolucao
                         
    # Abaixo temos uma função para criar um kernel capaz de borrar uma imagem, tem como argumentos n que representa as dimensões do kernel
    def fazer_kernel_borrado(self, n):    
        kernel = []
        elemento_do_kernel = 1/(pow(n, 2))
        """
        Acima criamos um array vazio chamado kernel, logo depois criamos uma variavel chamada elemento do kernel,
        essa variavel representa cada elemento do kernel que terá o mesmo valor(1/n^2).

        Logo abaixo temos um loop for que percorre n, criamos então um novo array vazio chamado linha do kernel e adicionamos
        a linha do kernel n vezes dentro do kernel, assim criando uma matriz com as linhas do kernel compostas pelo elemento
        do kernel
        """
        for _ in range(n):
            linha_do_kernel = []
            """
        Novamente abaixo temos outro loop for que também percorre n, porém agora nos adicionamos o elemento do kernel n vezes 
        dentro do array linha do kernel
            """  
            for _ in range(n):
                linha_do_kernel.append(elemento_do_kernel)
            kernel.append(linha_do_kernel)
        """
        Então retornamos um kernel capaz de borrar imagens.
        
        Algumas considerações em relação a essa função:

        Eu optei por fazer uma função separada para a criação de kernels de borragem pois
        no pset temos 2 filtros que necessitam de um kernel borrado, e realizar essas mesmas linhas
        de codigo para cada filtro seria repetitivo. 
        """
        return kernel

    # Abaixo temos uma função de ajuste nos valores de um pixel, tem como argumento somente o valor do pixel
    def ajustar_pixel(self, pixel):
        """
        Essa é uma função bem simples chamada quando se mostra necessario o ajuste nos intervalos de valores
        de um pixel.

        Basicamente como é evidente ela verifica se os valores estão dentro do intervalo de 0 a 255
        caso maior que 255 o pixel é = 255
        caso menor que 0 o pixel é = 0

        Então retorna o valor do pixel
        """
        if pixel > 255: pixel = 255
        if pixel < 0: pixel = 0

        return pixel
    # Abaixo temos a função que aplica ou o filtro de borda ou o filtro de foco, ela recebe 2 kernels a variavel de ajuste e o indicador do filtro como argumentos
    def aplicar_borda_ou_foco(self, kernel_x, kernel_y, ajuste, filtro):
        resultado = Imagem.nova(self.largura, self.altura)
        """
        Aqui criamos uma nova imagem chamada resultado que irá armazenar a imagem resultante do filtro indicado pela variavel "filtro"
        Logo em seguida criamos imagem_kx e ky que armazenarão os resultados da imagem com os kernels x e y aplicados em seus respectivos correspondentes.
        Ao aplicarmos o filtro de foco devemos levar em conta que a imagem_kx na verdade é a propria imagem original, como consta na formula para o mesmo.
        """   
        imagem_kx = self.usar_kernel(kernel_x, ajuste)
        imagem_ky = self.usar_kernel(kernel_y, ajuste)
        """
        Abaixo temos 2 loops for com as variaves x e y que irão percorrer os pixels das imagens kx e ky.
        """
        for x in range(self.largura):
            for y in range(self.altura):
                """
        Aqui temos a verificação através da variavel "Filtro" que irá indicar qual filtro será utilizado na imagem
        sendo o filtro 1 o filtro de bordas e o 2 o filtro de foco.

        Após isso o filtro é aplicado no pixel x,y referente no loop e então é armazenado na variavel xy
                """
                if filtro == 1: 
                    xy = round(math.sqrt(imagem_kx.get_pixel(x, y) ** 2 + imagem_ky.get_pixel(x, y) ** 2))
                if filtro == 2:
                    xy = round(2 * imagem_kx.get_pixel(x,y) - imagem_ky.get_pixel(x, y))
                    """
        Abaixo chamamos a função para ajustar o intervalo dos valores dos pixels como consta na descrição da função de ajuste
        Logo em seguida chamamos a função setpixel para alterar o pixel original da imagem resultado para o novo pixel agora com o filtro aplicado
        e no devido intervalo.
                    """    
                xy = self.ajustar_pixel(xy)
                resultado.set_pixel(x, y, xy)

        return resultado

    # Abaixo temos a função que será chamada quando quisermos aplicar o filtro de inversão
    def invertida(self):
        """
        Chamamos a função aplicar por pixel fornecendo como argumento uma função lambda 255 - c, onde c é o valor do pixel
        o resultado dessa função retornará apresentando o valor inverso do valor de c.
        Ex:
        
         caso c seja 100 a função retorna seu inverso, no caso 155.
        """
        return self.aplicar_por_pixel(lambda c: 255 - c)

        

    # Abaixo temos a função que será chamada quando quisermos aplicar o filtro de desfoque, ela recebe como argumento n que representa as dimensões do kernel
    def borrada(self, n):
        """
        Criamos uma variavel booleana chamada ajusta que definirá dentro da função "usar_kernel" a necessidade
         do ajuste previo ou não dos intervalos do pixel utilizando a função "ajustar_pixel"

         No caso do filtro de desfoque esse ajuste pode ser feito com antecedencia, ja que o valor dos pixels do mesmo não serão utilizados
         em operações futuras.
        """
        ajuste = True
        """
        Abaixo criamos nosso kernel e igualamos o mesmo ao retorno da função "fazer_kernel_borrado" fornecendo n como as dimensões do kernel

        Então retornamos o resultado de "usar_kernel" com o kernel de desfoque e a variavel de ajuste como argumentos.
        """
        kernel = self.fazer_kernel_borrado(n)
        return self.usar_kernel(kernel, ajuste)

    # Abaixo temos a função que será chamada quando quisermos aplicar o filtro de desfoque, ela recebe como argumento n que representa as dimensões do kernel
    def focada(self, n):
        """
        Assim como a função de desfoque criamos aqui a variavel de ajuste, porém agora ela carrega o valor de falso, o que sinaliza que o ajuste deverá ser feito
        posteriormente, e não na função "usar_kernel"

        Criamos também uma nova variavel chamada filtro que indica o filtro a ser utilizado na função "aplicar_borda_ou_foco"
        o valor 2 representa que a operação a ser realizada deve ser referente ao filtro de foco

        E por ultimo criamos 2 kernels, um sendo um kernel de desfoque e outro um kernel identidade, como foi orientado no pdf do pset,
        o filtro de foco é uma operação entre a imagem original e a imagem borrada
        """
        filtro = 2
        ajuste = False

        kernel = self.fazer_kernel_borrado(n)

        identidade = [[0, 0, 0],
                      [0 ,1, 0],
                      [0, 0, 0]]

        """
        Por fim chamamos a função "aplicar_borda_ou_foco" e retornamos seu resultado.
        """

        return self.aplicar_borda_ou_foco(identidade, kernel, ajuste, filtro)

    def bordas(self):
        """
        Novamente criamos aqui a variavel de ajuste, carregando o valor de falso, o que sinaliza que o ajuste deverá ser feito
        posteriormente, e não na função "usar_kernel"

        Criamos novamente uma variavel filtro que indica o filtro a ser utilizado na função "aplicar_borda_ou_foco"
        o valor 1 representa que a operação a ser realizada deve ser referente ao filtro de borda

        E por ultimo criamos 2 kernels x e y conforme foi orientado no arquivo do pset, que serão utilizados na operação de bordas
        """    
        filtro = 1
        ajuste = False

        kernel_x =  [[-1, 0, 1],
                     [-2, 0, 2],
                     [-1, 0, 1]]
    
        kernel_y =  [[-1, -2, -1],
                     [ 0,  0,  0],
                     [ 1,  2,  1]]

        """
        Por fim chamamos a função "aplicar_borda_ou_foco" e retornamos seu resultado.
        """
        return self.aplicar_borda_ou_foco(kernel_x, kernel_y, ajuste, filtro)


    # Abaixo temos uma função referente a um filtro para desolocar um pixel, para testar nossa função de correlação(Questão 4)
    def deslocar(self):
        """
        Criamos a variavel de ajuste e permitimos o ajuste na propria função de correlação

        Criamos também um kernel para deslocar os pixels da imagem
        """
        ajuste = True
        kernel = [
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]
                 ]
        return self.usar_kernel(kernel, ajuste)
           

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(
            getattr(self, i) == getattr(other, i)
            for i in ("altura", "largura", "pixels")
        )

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, "rb") as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith("RGB"):
                pixels = [
                    round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
                ]
            elif img.mode == "LA":
                pixels = [p[0] for p in img_data]
            elif img.mode == "L":
                pixels = list(img_data)
            else:
                raise ValueError("Modo de imagem não suportado: %r" % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo="PNG"):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode="L", size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo="GIF")
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(
            toplevel, height=self.altura, width=self.largura, highlightthickness=0
        )
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode="L", size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize(
                (event.width, event.height), PILImage.NEAREST
            )
            buffer = BytesIO()
            nova_imagem.save(buffer, "GIF")
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind("<Configure>", ao_redimensionar)
        toplevel.bind(
            "<Configure>", lambda e: tela.configure(height=e.height, width=e.width)
        )

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol("WM_DELETE_WINDOW", tk_root.destrimage_ky)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()

    def refaz_apos():
        tcl.after(500, refaz_apos)

    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == "__main__":
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    im = Imagem.carregar('test_images/chess.png')
    im_peixe = Imagem.carregar('test_images/bluegill.png')
    im_porco = Imagem.carregar('test_images/pigbird.png')
    im_cobra = Imagem.carregar('test_images/python.png')
    im_construcao = Imagem.carregar('test_images/construct.png')
    
    resultado_borda = im.bordas()
    resultado_borrada = im.borrada(9)
    resultado_invertida = im.invertida()
    resultado_focada = im.focada(9)
    resultado_peixe = im_peixe.invertida()
    resultado_porco = im_porco.deslocar()
    resultado_cobra = im_cobra.focada(11)
    resultado_construcao = im_construcao.bordas()
    

    resultado_borda.salvar('resultados/bordas.png')
    resultado_borrada.salvar('resultados/borrada.png')
    resultado_invertida.salvar('resultados/invertida.png')
    resultado_focada.salvar('resultados/focada.png')
    resultado_peixe.salvar('questoes/pexe_invertido.png')
    resultado_porco.salvar('questoes/porco_deslocado.png')
    resultado_cobra.salvar('questoes/cobra_focada.png')
    resultado_construcao.salvar('questoes/construcao_borda.png')
    
    
    pass

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
