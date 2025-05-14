# Instruções para Atualização Automática de Notícias do Site de Segurança

Este guia explica como usar o script Python (`update_news.py`) para buscar automaticamente as últimas notícias de segurança da Kaspersky e Olhar Digital e atualizar o conteúdo do seu site hospedado no IIS em um Windows Server 2022.

## Pré-requisitos

1.  **Python Instalado:** Certifique-se de que o Python (versão 3.6 ou superior) está instalado no seu Windows Server 2022. Você pode baixá-lo em [python.org](https://www.python.org/downloads/windows/). Durante a instalação, marque a opção "Add Python to PATH".
2.  **Bibliotecas Python:** Você precisará das bibliotecas `requests` e `beautifulsoup4`. Abra o Prompt de Comando (CMD) ou PowerShell como administrador e instale-as com o pip:
    ```bash
    pip install requests beautifulsoup4
    ```

## Arquivos Necessários

Você precisará dos seguintes arquivos, que foram fornecidos:

1.  `update_news.py`: O script Python que busca e processa as notícias.
2.  `index.html`: O arquivo HTML base do seu site. **Este arquivo será usado como template pelo script.** O script procurará por marcadores específicos nele para inserir o conteúdo das notícias.

## Configuração e Execução do Script

1.  **Crie uma Pasta para o Script:**
    *   No seu servidor, crie uma pasta dedicada para o script e o arquivo HTML base. Por exemplo: `C:\site-updater`.
    *   Copie os arquivos `update_news.py` e `index.html` (o original que você usa como base) para esta pasta (`C:\site-updater`).

2.  **Verifique os Marcadores no `index.html` (Importante!):**
    *   Abra o arquivo `index.html` (que está em `C:\site-updater`) em um editor de texto.
    *   Localize a seção onde as notícias devem ser inseridas (geralmente dentro de `<section id="noticias">`).
    *   **Certifique-se de que os seguintes comentários (marcadores) existem exatamente como mostrado, envolvendo a área onde as notícias antigas estão ou onde as novas devem entrar:**
        ```html
        <!-- NEWS_CONTENT_START -->
        <!-- Aqui ficava o conteúdo antigo das notícias, ou pode estar vazio -->
        <!-- NEWS_CONTENT_END -->
        ```
    *   O script `update_news.py` substituirá tudo entre `<!-- NEWS_CONTENT_START -->` e `<!-- NEWS_CONTENT_END -->` pelo novo conteúdo das notícias.

3.  **Executando o Script Manualmente (para Teste Inicial):**
    *   Abra o Prompt de Comando (CMD) ou PowerShell.
    *   Navegue até a pasta onde você colocou os arquivos: `cd C:\site-updater`
    *   Execute o script:
        ```bash
        python update_news.py
        ```
    *   Se tudo correr bem, o script buscará as notícias, processará e criará um novo arquivo chamado `index_updated.html` na mesma pasta (`C:\site-updater`). Este arquivo conterá as notícias mais recentes.
    *   Verifique o console para mensagens de erro ou sucesso.

4.  **Atualizando o Site no IIS:**
    *   Após a execução bem-sucedida do script, você terá o arquivo `index_updated.html` com as notícias atualizadas.
    *   Você precisa substituir o `index.html` principal do seu site (que o IIS está servindo, por exemplo, em `C:\inetpub\wwwroot\meu-site-seguranca\index.html`) pelo conteúdo do `index_updated.html`.
    *   **Opção A (Recomendado para automação):**
        *   No seu script de automação (ver seção abaixo), após executar `python update_news.py`, adicione um comando para copiar `C:\site-updater\index_updated.html` para `C:\inetpub\wwwroot\meu-site-seguranca\index.html`, substituindo o arquivo existente.
        *   Exemplo de comando para copiar (pode ser usado em um arquivo `.bat` ou no Agendador de Tarefas):
            ```batch
            copy /Y "C:\site-updater\index_updated.html" "C:\inetpub\wwwroot\meu-site-seguranca\index.html"
            ```
    *   **Opção B (Manual):**
        *   Renomeie `C:\inetpub\wwwroot\meu-site-seguranca\index.html` para `index_old.html` (como backup).
        *   Copie `C:\site-updater\index_updated.html` para `C:\inetpub\wwwroot\meu-site-seguranca\`.
        *   Renomeie o `index_updated.html` copiado para `index.html`.

## Automatizando a Atualização com o Agendador de Tarefas do Windows

Você pode configurar o Agendador de Tarefas do Windows para executar o script `update_news.py` e o comando de cópia automaticamente em intervalos regulares (ex: diariamente).

1.  **Crie um Arquivo de Lote (.bat):**
    *   Crie um novo arquivo de texto em `C:\site-updater` e nomeie-o, por exemplo, `run_site_update.bat`.
    *   Adicione os seguintes comandos ao arquivo `.bat`:
        ```batch
        @echo off
        echo Iniciando atualizacao do site de seguranca...
        cd C:\site-updater
        python update_news.py
        
        REM Verifique se o index_updated.html foi criado antes de copiar
        IF EXIST "C:\site-updater\index_updated.html" (
            echo Copiando arquivo HTML atualizado para o diretorio do site...
            copy /Y "C:\site-updater\index_updated.html" "C:\inetpub\wwwroot\meu-site-seguranca\index.html"
            echo Atualizacao concluida!
        ) ELSE (
            echo Erro: index_updated.html nao foi encontrado apos a execucao do script.
        )
        pause
        ```
    *   **Observação:** Substitua `C:\inetpub\wwwroot\meu-site-seguranca\index.html` pelo caminho real do `index.html` do seu site no IIS.
    *   Teste este arquivo `.bat` clicando duas vezes nele para garantir que funciona como esperado.

2.  **Configure o Agendador de Tarefas:**
    *   Abra o "Agendador de Tarefas" no Windows Server.
    *   No painel Ações, clique em "Criar Tarefa Básica...".
    *   **Nome:** Dê um nome (ex: `AtualizacaoDiariaSiteSeguranca`).
    *   **Disparador:** Escolha a frequência (Diariamente, Semanalmente, etc.) e configure o horário.
    *   **Ação:** Selecione "Iniciar um programa".
        *   **Programa/script:** Navegue e selecione o arquivo `run_site_update.bat` que você criou (ex: `C:\site-updater\run_site_update.bat`).
    *   Revise e clique em "Concluir".
    *   Você pode querer ajustar as configurações da tarefa (como "Executar estando o usuário conectado ou não" e "Executar com privilégios mais altos") clicando com o botão direito na tarefa criada e selecionando "Propriedades".

## Considerações Importantes

*   **Estrutura do Site:** O script de scraping (`update_news.py`) depende da estrutura HTML dos sites da Kaspersky e Olhar Digital. Se eles mudarem o layout de seus sites, o script pode parar de funcionar corretamente e precisará de ajustes nos seletores BeautifulSoup.
*   **Bloqueio por IP:** Executar o scraping com muita frequência pode levar ao bloqueio do IP do seu servidor pelos sites de notícias. A execução diária geralmente é aceitável.
*   **Erros:** O script inclui tratamento básico de erros, mas monitore os logs ou a saída do console (se executar manualmente) para quaisquer problemas.
*   **Backup:** Mantenha backups regulares do seu `index.html` original e do script `update_news.py`.

Seguindo estas instruções, você poderá manter a seção de notícias do seu site de segurança atualizada com as informações mais recentes de forma semi-automatizada.
