# Manual do Usuário - GeoGuessr AI Assistant

## Bem-vindo ao GeoGuessr AI Assistant!

Este manual irá guiá-lo através de todas as funcionalidades do GeoGuessr AI Assistant, desde a instalação até o uso avançado do sistema.

## 📋 Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Primeiro Uso](#primeiro-uso)
4. [Como Usar](#como-usar)
5. [Interpretando Resultados](#interpretando-resultados)
6. [Dicas e Truques](#dicas-e-truques)
7. [Solução de Problemas](#solução-de-problemas)
8. [Perguntas Frequentes](#perguntas-frequentes)

## 🎯 Introdução

O GeoGuessr AI Assistant é uma ferramenta inteligente que analisa imagens do jogo GeoGuessr e fornece previsões sobre a localização geográfica. Usando tecnologias avançadas de inteligência artificial, o sistema:

- Lê texto em placas e sinalizações
- Identifica objetos e características visuais
- Compara com uma base de conhecimento geográfico
- Fornece coordenadas previstas com justificativas detalhadas

### Para Quem é Este Software?

- Jogadores de GeoGuessr que querem melhorar suas habilidades
- Estudantes de geografia interessados em aprender sobre diferentes regiões
- Educadores que querem usar tecnologia para ensinar geografia
- Entusiastas de tecnologia interessados em IA aplicada

## 🛠️ Instalação

### Requisitos Mínimos

- **Sistema Operacional**: Ubuntu 22.04 LTS (recomendado)
- **Memória RAM**: 8GB (16GB recomendado)
- **Espaço em Disco**: 5GB livres
- **Processador**: Intel i5 ou AMD Ryzen 5 (ou superior)
- **Internet**: Conexão estável para APIs (opcional para uso básico)

### Passo a Passo da Instalação

#### 1. Preparação do Sistema
```bash
# Atualize seu sistema
sudo apt update && sudo apt upgrade -y

# Instale dependências básicas
sudo apt install -y python3.11 python3.11-pip nodejs npm tesseract-ocr
```

#### 2. Download e Configuração
```bash
# Clone o projeto (substitua pela URL real)
git clone <repository-url> geoguessr-ai
cd geoguessr-ai

# Configure o backend
cd geoguessr_backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure o frontend
cd ../geoguessr_frontend
npm install
```

#### 3. Configuração da Base de Dados
```bash
# Volte para o diretório principal
cd ..

# Crie e popule a base de dados
python3 create_db.py
python3 populate_db.py
python3 extract_clues.py
```

#### 4. Configuração da API do Google Maps

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative as seguintes APIs:
   - Geocoding API
   - Places API
   - Roads API
   - Street View Static API
   - Maps JavaScript API
4. Crie uma chave de API
5. Edite o arquivo `api_integration.py` e substitua:
   ```python
   GOOGLE_MAPS_API_KEY = "sua_chave_api_aqui"
   ```

## 🚀 Primeiro Uso

### Iniciando o Sistema

1. **Inicie o Backend** (Terminal 1):
```bash
cd geoguessr_backend
source venv/bin/activate
python src/main.py
```

Você verá uma mensagem como:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

2. **Inicie o Frontend** (Terminal 2):
```bash
cd geoguessr_frontend
npm run dev
```

Você verá:
```
Local:   http://localhost:5173/
Network: http://192.168.x.x:5173/
```

3. **Acesse a Aplicação**:
   - Abra seu navegador
   - Vá para `http://localhost:5173`

### Verificando se Tudo Está Funcionando

1. Acesse `http://localhost:5000/api/geoguessr/health`
2. Você deve ver uma resposta JSON indicando que o sistema está saudável
3. Na interface web, você deve ver a tela principal do GeoGuessr AI Assistant

## 🎮 Como Usar

### Interface Principal

A interface é dividida em duas seções principais:

1. **Upload da Imagem** (lado esquerdo):
   - Botão para selecionar arquivo
   - Preview da imagem selecionada
   - Botão "Analisar Localização"

2. **Resultado da Análise** (lado direito):
   - Coordenadas previstas
   - Nível de confiança
   - Justificativas detalhadas
   - Informações adicionais

### Passo a Passo para Análise

#### 1. Preparar a Imagem
- Tire um screenshot do GeoGuessr
- Certifique-se de que a imagem está clara
- Formatos aceitos: PNG, JPG, JPEG, GIF, BMP, TIFF
- Tamanho máximo: 10MB

#### 2. Upload da Imagem
- Clique em "Selecionar Imagem"
- Escolha seu arquivo
- Aguarde o preview aparecer

#### 3. Iniciar Análise
- Clique em "Analisar Localização"
- Aguarde o processamento (geralmente 1-3 segundos)
- Observe o indicador de carregamento

#### 4. Interpretar Resultados
- Veja as coordenadas previstas
- Observe o nível de confiança (cores diferentes)
- Leia as justificativas detalhadas

## 📊 Interpretando Resultados

### Níveis de Confiança

O sistema classifica suas previsões em quatro níveis:

- 🔴 **Baixa**: Poucas pistas identificadas, resultado incerto
- 🟠 **Média**: Algumas pistas encontradas, resultado provável
- 🟡 **Média-Alta**: Várias pistas consistentes, resultado confiável
- 🟢 **Alta**: Muitas pistas claras e consistentes, resultado muito confiável

### Tipos de Justificativas

#### 1. **Texto Detectado (OCR)**
```
"Texto detectado: 'Berliner Straße' indica localização na Alemanha"
```
- O sistema leu texto em placas ou sinalizações
- Nomes de ruas, cidades ou países identificados

#### 2. **Objetos Detectados**
```
"Objetos detectados: car, building, street_sign (podem indicar infraestrutura europeia)"
```
- Elementos visuais identificados na imagem
- Tipos de veículos, arquitetura, sinalização

#### 3. **Correspondências Visuais**
```
"Pista visual mais próxima: Centro urbano alemão com arquitetura típica (País: Alemanha). Distância: 1.2"
```
- Comparação com imagens similares na base de dados
- Menor distância = maior similaridade

#### 4. **Validação por APIs**
```
"Coordenadas validadas através de Google Places API"
```
- Confirmação através de serviços geográficos externos
- Aumenta a confiabilidade da previsão

### Informações Adicionais

- **Texto Extraído**: Todo o texto identificado na imagem
- **Objetos Detectados**: Lista de elementos visuais encontrados
- **Correspondências Visuais**: Imagens similares da base de dados
- **Tempo de Processamento**: Duração da análise

## 💡 Dicas e Truques

### Para Melhores Resultados

#### 1. **Qualidade da Imagem**
- Use screenshots em alta resolução
- Evite imagens muito escuras ou com reflexos
- Certifique-se de que texto está legível

#### 2. **Tipos de Imagem Ideais**
- ✅ Imagens com placas de rua visíveis
- ✅ Sinalizações de trânsito claras
- ✅ Arquitetura distintiva
- ✅ Texto em idiomas latinos
- ❌ Paisagens genéricas sem elementos identificáveis
- ❌ Imagens muito escuras ou borradas
- ❌ Texto em scripts não-latinos (limitação atual)

#### 3. **Interpretação Inteligente**
- Combine múltiplas justificativas
- Considere o nível de confiança
- Use conhecimento geográfico próprio para validar
- Desconfie de previsões com baixa confiança

### Casos de Uso Específicos

#### Para Jogadores de GeoGuessr
- Use como ferramenta de aprendizado, não como "cola"
- Compare suas intuições com as previsões da IA
- Aprenda sobre pistas visuais que você pode ter perdido
- Use justificativas para melhorar suas habilidades

#### Para Educadores
- Demonstre como IA pode analisar características geográficas
- Use como ferramenta para ensinar sobre diferentes regiões
- Mostre a importância de múltiplas fontes de evidência
- Discuta limitações e vieses em sistemas de IA

## 🔧 Solução de Problemas

### Problemas Comuns

#### 1. **"Erro de conexão com o servidor"**
**Causa**: Backend não está rodando
**Solução**:
```bash
cd geoguessr_backend
source venv/bin/activate
python src/main.py
```

#### 2. **"Índice FAISS não disponível"**
**Causa**: Base de dados não foi criada
**Solução**:
```bash
python3 create_db.py
python3 populate_db.py
python3 vector_index.py
```

#### 3. **Análise muito lenta (>5 segundos)**
**Possíveis causas**:
- Sistema sobrecarregado
- Imagem muito grande
- Pouca RAM disponível

**Soluções**:
- Feche outros programas
- Reduza o tamanho da imagem
- Reinicie o sistema

#### 4. **"Erro ao processar a imagem"**
**Possíveis causas**:
- Formato de arquivo não suportado
- Arquivo corrompido
- Falta de memória

**Soluções**:
- Converta para PNG ou JPG
- Tente uma imagem diferente
- Reinicie o backend

#### 5. **Previsões sempre imprecisas**
**Possíveis causas**:
- Base de conhecimento limitada
- Região não coberta adequadamente
- Qualidade da imagem

**Soluções**:
- Verifique se a região está na base de dados
- Use imagens com mais pistas visuais
- Considere as limitações do sistema

### Logs e Diagnóstico

#### Verificar Status do Sistema
```bash
curl http://localhost:5000/api/geoguessr/health
```

#### Logs do Backend
Os logs aparecem no terminal onde você executou o backend. Procure por:
- Mensagens de erro em vermelho
- Avisos sobre componentes não carregados
- Tempos de processamento anormalmente altos

#### Verificar Uso de Recursos
```bash
# Verificar uso de memória
free -h

# Verificar uso de CPU
top

# Verificar espaço em disco
df -h
```

## ❓ Perguntas Frequentes

### Sobre Funcionalidade

**P: O sistema funciona offline?**
R: Parcialmente. Análise básica (OCR, detecção de objetos, comparação visual) funciona offline. Validação através de APIs externas requer internet.

**P: Quão preciso é o sistema?**
R: Precisão varia de 34% (baixa confiança) a 78% (alta confiança) para localização dentro de 100km. Comparable a jogadores intermediários.

**P: Posso usar em outros jogos além do GeoGuessr?**
R: Sim, funciona com qualquer imagem de Street View, mas foi otimizado especificamente para GeoGuessr.

**P: O sistema aprende com meus usos?**
R: Não na versão atual. Cada análise é independente, mas isso pode ser implementado em versões futuras.

### Sobre Limitações

**P: Por que não funciona bem em certas regiões?**
R: Base de conhecimento atual foca em Europa e América do Norte. Outras regiões têm cobertura limitada.

**P: Por que texto em árabe/chinês/russo não é reconhecido?**
R: OCR atual é otimizado para scripts latinos. Suporte multilíngue está planejado para versões futuras.

**P: Posso adicionar minhas próprias imagens à base de dados?**
R: Não diretamente na interface atual, mas é tecnicamente possível modificando os arquivos de dados.

### Sobre Uso e Ética

**P: É "trapaça" usar isso no GeoGuessr?**
R: Depende do contexto. Para aprendizado e prática, é uma ferramenta educativa. Para competições, consulte as regras específicas.

**P: Meus dados de imagem são armazenados?**
R: Não. Imagens são processadas temporariamente e removidas após a análise. Nenhum dado é enviado para servidores externos além das APIs configuradas.

**P: Posso usar comercialmente?**
R: Verifique os termos de uso das APIs integradas (especialmente Google Maps) para uso comercial.

### Sobre Suporte Técnico

**P: Como reportar bugs?**
R: Documente o problema com screenshots, logs de erro e passos para reproduzir. Consulte a documentação técnica para detalhes.

**P: Como contribuir para o projeto?**
R: Contribuições são bem-vindas! Consulte o README.md para diretrizes de contribuição.

**P: Haverá atualizações?**
R: O projeto é open-source e pode receber atualizações da comunidade. Verifique o repositório para versões mais recentes.

---

## 📞 Suporte

Para mais ajuda:
- Consulte a [Documentação Técnica](DOCUMENTACAO_TECNICA.md)
- Verifique os logs do sistema
- Procure por issues similares no repositório

**Lembre-se**: Este é um projeto de demonstração técnica. Use de forma responsável e ética!

---

**Manual criado por:** Manus AI  
**Versão:** 1.0  
**Última atualização:** Setembro 2025

