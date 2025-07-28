# yt-dlp Hotmart Cloudfront Downloader

Uma interface de linha de comando SIMPLES para baixar vídeos da Hotmart disponibilizados pela AWS Cloudfront a partir de seu player embed (em outros sites fora dos clubs) usando yt-dlp com downloads de segmentos customizado.  

**Atenção:** O ponto deste software não é automatizar o processo de download de cursos inteiros igual o [Katomart](https://github.com/katomaro/katomart) que é a suíte completa e possui bem mais funcionalidades, ele serve apenas como forma alternativa de download manual para sites ainda nao suportados que utilizem o player da Hotmart na forma de Script (embed). Assim como o Katomart e qualquer aplicativo de download, abusar de uma conexão rápida e muitos segmentos concorrentes pode fazer o servidor rejeitar suas solicitações temporariamente, simplesmente mude de IP com alguma VPN buxa (sua identificação é atrelada no libk, mas o bloqueio acontece a níveo de IP mesmo, e não, você não está violando a lei).

**Tenha em mente que uma URL master-pkg tem duração média de 7 minutos após sua geração.**

`<Isto é um placeholder para o site com imagens>`

## Funcionalidades

- CLI interativo com loop contínuo de downloads
- Downloads de fragmentos concorrentes configuráveis para velocidades maiores (usar com cuidado)
- Acompanhamento de progresso não-verboso no terminal
- Nomeação personalizada de vídeos para cada download
- Tratamento abrangente de erros e logging
- Saída graciosa com Ctrl+C

## 📦 Instalação

### Download das Releases

Para versões compiladas e estáveis, visite a [página de releases](https://github.com/katomaro/htm-cf-embed-dl/releases) e encontre uma correspondente ao seu sistema operacional.

### (Alternativamente) Executando a partir do Código Fonte (Python 3.12)
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/yt-dlp-hotmart-downloader.git
cd yt-dlp-hotmart-downloader
```

2. Instale a dependência necessária:
```bash
pip install -r requirements.txt
```

3. Execute o script:
```bash
python main.py
```

## 🎯 Como Usar

Escolha uma das formas acima, se executando da fonte, prossiga a partir do `python main.py`, se executando a partir de uma release, execute-a (dois cliques em um .exe ou após garantir `chmod +x` em sistemas linux). Para usuários MacOS, use da fonte.

### Fluxo Interativo

1. **Configure fragmentos concorrentes** (padrão: 6)
   - Valores maiores = downloads mais rápidos mas maior uso de recursos, e maior risco de downloads sendo negados
   - Faixa recomendada: 4-16

2. **Defina pasta de salvamento**
   - O script criará o diretório se ele não existir, se você não inserir um caminho qualificado, ele irá criar a partir da pasta de execução, sempre prefira caminhos próximos à raiz do disco.

3. **Loop de download**
   - Digite o nome do vídeo (sem extensão), por exemplo "Desenhando gatos e suas caudas"
   - Cole a URL do master-pkg da Hotmart
   - (Dica: o para colar no terminal, use o botão direito do mouse)
   - O download será iniciado
   - Repita para quantos vídeos desejar

4. **Sair**
   - Pressione Ctrl+C a qualquer momento para sair graciosamente

## 📄 Licença

Este projeto é de código aberto e está disponível sob a Licença MIT. 