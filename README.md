# shopee-sender-messages
Desenvolvi um projeto inovador em Python, focado na automação de interações no WhatsApp, visando otimizar a comunicação com os clientes. Ao enfrentar esse desafio, deparei-me com diversas complexidades inerentes à automação em Python, tais como a integração com APIs de terceiros, tratamento de exceções, e a necessidade de manutenção contínua para acompanhar as mudanças nas plataformas.

Um dos maiores desafios encontrados foi a ausência de uma API oficial do WhatsApp, o que demandou a exploração de alternativas. Optei por utilizar a biblioteca `selenium`, que possibilita a automação de navegação em um navegador web. Isso permitiu a abertura dos links de conversas no WhatsApp diretamente a partir de uma planilha, facilitando o envio de mensagens aos clientes de forma eficiente.

Além disso, para enfrentar a complexidade da criação de uma tela de frontend, reconheci a importância de incorporar uma biblioteca como `Flask` para facilitar o desenvolvimento web em Python. A utilização de `Flask` simplifica a construção da interface do usuário, permitindo uma integração mais suave com a lógica de automação já implementada.

A automação de envio de mensagens via WhatsApp foi alcançada através da simulação de interações humanas com o navegador, utilizando métodos da biblioteca `selenium` para preencher campos de texto e clicar em botões. No entanto, é crucial destacar que tal abordagem pode ter implicações éticas e legais, uma vez que as políticas de uso do WhatsApp proíbem a automação não autorizada.

O código-fonte inclui manipulação eficiente de planilhas usando bibliotecas como `pandas` para ler os links de conversa, enquanto o `selenium` interage com o navegador para enviar mensagens. Essa combinação de tecnologias oferece uma solução robusta para automação de tarefas no WhatsApp.

É essencial ressaltar que o uso responsável e ético dessas ferramentas é crucial para garantir conformidade com as políticas de privacidade e termos de serviço das plataformas envolvidas.
