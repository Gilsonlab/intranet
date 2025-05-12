document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll("nav a");
    const sections = document.querySelectorAll("main section");
    const quizContainer = document.getElementById("quiz-container");
    const submitButton = document.getElementById("submit-quiz");
    const resultsContainer = document.getElementById("quiz-results");

    // Conteúdo do quiz (mesmo do script anterior)
    const quizData = [
        {
            question: "Qual das seguintes é a prática mais segura para criar senhas?",
            options: [
                "Usar a mesma senha para todas as contas para facilitar a memorização.",
                "Criar senhas curtas e fáceis de lembrar, como '123456' ou 'password'.",
                "Usar uma combinação longa de letras maiúsculas, minúsculas, números e símbolos, diferente para cada conta.",
                "Anotar todas as senhas em um papel e guardar perto do computador."
            ],
            answer: "Usar uma combinação longa de letras maiúsculas, minúsculas, números e símbolos, diferente para cada conta.",
            explanation: "Senhas fortes e únicas para cada conta são cruciais. Usar a mesma senha ou senhas fracas torna você um alvo fácil para hackers. Gerenciadores de senha podem ajudar a administrar senhas complexas."
        },
        {
            question: "O que é 'Phishing'?",
            options: [
                "Um tipo de software antivírus.",
                "Uma técnica de pesca esportiva popular entre hackers.",
                "Uma tentativa de obter informações confidenciais (como nomes de usuário, senhas e detalhes de cartão de crédito) se passando por uma entidade confiável em uma comunicação eletrônica.",
                "Um método seguro de criptografar e-mails."
            ],
            answer: "Uma tentativa de obter informações confidenciais (como nomes de usuário, senhas e detalhes de cartão de crédito) se passando por uma entidade confiável em uma comunicação eletrônica.",
            explanation: "Phishing é uma ameaça comum. Sempre desconfie de e-mails ou mensagens solicitando informações pessoais e verifique a legitimidade da fonte antes de clicar em links ou fornecer dados."
        },
        {
            question: "Por que é importante manter seus softwares e sistema operacional atualizados?",
            options: [
                "Para ter acesso aos recursos mais recentes, mesmo que não sejam relacionados à segurança.",
                "Porque as atualizações geralmente corrigem vulnerabilidades de segurança que podem ser exploradas por malware.",
                "Para tornar o computador mais lento, forçando o usuário a comprar um novo.",
                "Não é importante, as atualizações são opcionais e raramente afetam a segurança."
            ],
            answer: "Porque as atualizações geralmente corrigem vulnerabilidades de segurança que podem ser exploradas por malware.",
            explanation: "Manter o software atualizado é uma das defesas mais eficazes contra malware e outras ameaças, pois as atualizações frequentemente incluem patches para falhas de segurança recém-descobertas."
        },
        {
            question: "O que é autenticação de dois fatores (2FA)?",
            options: [
                "Um sistema que requer duas senhas diferentes para a mesma conta.",
                "Um método de segurança que exige duas formas distintas de verificação para acessar uma conta (por exemplo, senha e um código enviado para o seu celular).",
                "Um tipo de firewall que bloqueia o tráfego de duas direções.",
                "Um software que verifica seus arquivos duas vezes em busca de vírus."
            ],
            answer: "Um método de segurança que exige duas formas distintas de verificação para acessar uma conta (por exemplo, senha e um código enviado para o seu celular).",
            explanation: "A 2FA adiciona uma camada significativa de segurança, tornando muito mais difícil para invasores acessarem suas contas, mesmo que eles tenham sua senha."
        }
    ];

    function displayQuiz() {
        if (!quizContainer) return;
        quizContainer.innerHTML = "";
        quizData.forEach((item, index) => {
            const questionBlock = document.createElement("div");
            questionBlock.classList.add("question-block");
            const questionText = document.createElement("p");
            questionText.textContent = `${index + 1}. ${item.question}`;
            questionBlock.appendChild(questionText);

            item.options.forEach(option => {
                const label = document.createElement("label");
                const radio = document.createElement("input");
                radio.type = "radio";
                radio.name = `question${index}`;
                radio.value = option;
                label.appendChild(radio);
                label.appendChild(document.createTextNode(option));
                questionBlock.appendChild(label);
            });
            quizContainer.appendChild(questionBlock);
        });
    }

    function showResults() {
        if (!resultsContainer || !quizContainer) return;
        resultsContainer.innerHTML = "";
        let score = 0;
        const questions = quizContainer.querySelectorAll(".question-block");

        questions.forEach((block, index) => {
            const userAnswerNode = block.querySelector(`input[name="question${index}"]:checked`);
            const resultText = document.createElement("p");
            const explanationText = document.createElement("p");
            explanationText.classList.add("explanation");

            if (userAnswerNode) {
                const userAnswer = userAnswerNode.value;
                if (userAnswer === quizData[index].answer) {
                    score++;
                    resultText.textContent = `Questão ${index + 1}: Correto!`;
                    resultText.classList.add("correct-answer");
                } else {
                    resultText.textContent = `Questão ${index + 1}: Incorreto. A resposta correta era: "${quizData[index].answer}"`;
                    resultText.classList.add("incorrect-answer");
                }
            } else {
                resultText.textContent = `Questão ${index + 1}: Não respondida. A resposta correta era: "${quizData[index].answer}"`;
                resultText.classList.add("incorrect-answer");
            }
            explanationText.textContent = quizData[index].explanation;
            resultsContainer.appendChild(resultText);
            resultsContainer.appendChild(explanationText);
        });

        const scoreHeader = document.createElement("h3");
        scoreHeader.textContent = `Seu resultado: ${score} de ${quizData.length}`;
        resultsContainer.insertBefore(scoreHeader, resultsContainer.firstChild);
        resultsContainer.style.display = "block";
    }

    // Função para mostrar a seção correta e ocultar as outras
    function showSection(targetId) {
        sections.forEach(section => {
            if (section.id === targetId) {
                section.classList.add("visible");
            } else {
                section.classList.remove("visible");
            }
        });
        // Se a seção do quiz for mostrada, renderiza o quiz
        if (targetId === "quiz" && quizContainer) {
            displayQuiz();
            if(resultsContainer) resultsContainer.innerHTML = ""; // Limpa resultados anteriores
        }
    }

    // Adiciona event listeners para os links de navegação
    navLinks.forEach(link => {
        link.addEventListener("click", (event) => {
            event.preventDefault(); // Previne o comportamento padrão do link (rolagem)
            const targetId = link.getAttribute("href").substring(1); // Remove o '#'
            showSection(targetId);
        });
    });

    // Exibe a seção inicial por padrão
    showSection("inicio");

    // Adiciona event listener para o botão de submissão do quiz
    if (submitButton) {
        submitButton.addEventListener("click", showResults);
    }

    // Carregar conteúdo das notícias (exemplo, idealmente seria mais robusto)
    const noticiasSection = document.getElementById("noticias");
    if (noticiasSection) {
        // Simula o carregamento do compiled_content.md
        // Em um cenário real, você usaria fetch() para carregar o arquivo markdown
        // e uma biblioteca como Showdown.js ou Marked.js para converter para HTML.
        // Por simplicidade, vamos adicionar alguns itens de notícia diretamente aqui.
        const newsContentPlaceholder = noticiasSection.querySelector(".news-item");
        if (newsContentPlaceholder && newsContentPlaceholder.parentNode) {
            // Remove o placeholder se existir
            // newsContentPlaceholder.parentNode.innerHTML = ''; // Limpa a área de notícias antes de adicionar novas
            
            // Adicionar notícias do compiled_content.md (simulado)
            // Esta parte precisaria de uma lógica para buscar e parsear o .md
            // Aqui, vamos apenas manter os placeholders ou adicionar conteúdo estático de exemplo
            // Se você tem o conteúdo em compiled_content.md, precisaria de uma função para inseri-lo aqui.
            // Por ora, o HTML já tem placeholders, então não vamos modificar dinamicamente aqui
            // a menos que você queira carregar o conteúdo do .md via JS.
        }
    }
});

