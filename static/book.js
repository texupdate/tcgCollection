let currentCollection = null;
let currentCollectionName = null;
let currentCollectionData = null;
let currentPage = 0;
let allCards = [];
let minCardNumber = 0;
let maxCardNumber = 0;
let searchTerm = '';
const CARDS_FIRST_PAGE = 9; // Primeira página (direita) tem 9 cartas
const CARDS_PER_PAGE = 18; // Páginas seguintes tem 18 cartas (9 + 9)

// Carrega as coleções ao iniciar
window.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Página carregada, iniciando...');
    loadCollections();
    
    // Verificar se tem parâmetro collection na URL
    const urlParams = new URLSearchParams(window.location.search);
    const collectionParam = urlParams.get('collection');
    if (collectionParam) {
        console.log('📦 Parâmetro de coleção detectado:', collectionParam);
        // Aguardar coleções carregarem e então selecionar
        setTimeout(() => selectCollectionByName(decodeURIComponent(collectionParam)), 500);
    }
});

// Carrega todas as coleções
async function loadCollections() {
    console.log('🔄 Carregando coleções...');
    try {
        const response = await fetch('/api/collections');
        console.log('📡 Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const collections = await response.json();
        console.log('📚 Coleções recebidas:', collections.length, collections);
        
        const select = document.getElementById('collectionSelect');
        if (!select) {
            console.error('❌ Select element não encontrado!');
            return;
        }
        
        select.innerHTML = '<option value="">Selecione uma coleção...</option>';
        
        collections.forEach(collection => {
            const option = document.createElement('option');
            option.value = collection.id;
            option.dataset.name = collection.name; // Guardar nome no dataset
            option.textContent = `${collection.name} (${collection.total_cards} cartas)`;
            select.appendChild(option);
        });
        
        console.log('✅ Coleções carregadas com sucesso!');
        
        if (collections.length === 0) {
            showEmptyState();
        }
    } catch (error) {
        console.error('❌ Erro ao carregar coleções:', error);
        alert('Erro ao carregar coleções. Verifique se o servidor está rodando.');
    }
}

// Seleciona uma coleção pelo nome (usado quando vem de URL)
function selectCollectionByName(collectionName) {
    console.log('🔍 Buscando coleção:', collectionName);
    const select = document.getElementById('collectionSelect');
    
    // Procurar a option com o nome correspondente
    const options = select.querySelectorAll('option');
    for (let option of options) {
        if (option.dataset.name === collectionName) {
            select.value = option.value;
            currentCollectionName = collectionName;
            changeCollection();
            console.log('✅ Coleção selecionada:', collectionName);
            return;
        }
    }
    
    console.warn('⚠️ Coleção não encontrada:', collectionName);
}

// Muda a coleção selecionada
function changeCollection() {
    const select = document.getElementById('collectionSelect');
    const selectedOption = select.options[select.selectedIndex];
    
    currentCollection = select.value;
    currentCollectionName = selectedOption.dataset.name;
    currentPage = 0;
    searchTerm = ''; // Limpar busca ao trocar coleção
    document.getElementById('searchInput').value = '';
    
    if (currentCollection) {
        // Atualizar URL sem recarregar a página
        if (currentCollectionName) {
            const newUrl = `${window.location.pathname}?collection=${encodeURIComponent(currentCollectionName)}`;
            window.history.pushState({collection: currentCollectionName}, '', newUrl);
            console.log('🔗 URL atualizada:', newUrl);
        }
        
        // Atualizar título e imagem da coleção
        updateCollectionHeader(currentCollectionName);
        
        loadCards();
        hideEmptyState();
    } else {
        // Limpar parâmetro da URL se desselecionar
        window.history.pushState({}, '', window.location.pathname);
        resetCollectionHeader();
        showEmptyState();
    }
}

// Atualiza o header com informações da coleção
function updateCollectionHeader(collectionName) {
    // Atualizar título
    const pageTitle = document.getElementById('pageTitle');
    pageTitle.textContent = `Coleção TCG - ${collectionName}`;
    
    // Atualizar imagem da coleção (esquerda)
    const collectionLogoImg = document.getElementById('collectionLogoImg');
    const collectionImagePath = `/static/collection_bkg/${collectionName}.png`;
    collectionLogoImg.src = collectionImagePath;
    collectionLogoImg.style.display = 'block';
    collectionLogoImg.onerror = function() {
        this.style.display = 'none';
    };
}

// Reseta o header quando nenhuma coleção está selecionada
function resetCollectionHeader() {
    const pageTitle = document.getElementById('pageTitle');
    pageTitle.textContent = 'Minha Coleção TCG';
    
    const collectionLogoImg = document.getElementById('collectionLogoImg');
    collectionLogoImg.style.display = 'none';
    
    const statsBox = document.getElementById('collectionStats');
    statsBox.style.display = 'none';
}

// Atualiza as estatísticas da coleção
function updateCollectionStats() {
    const statsBox = document.getElementById('collectionStats');
    
    if (allCards.length === 0) {
        statsBox.style.display = 'none';
        return;
    }
    
    // Calcular estatísticas
    const totalCards = allCards.length;
    const ownedCards = allCards.filter(card => card.quantity > 0).length;
    const completionRate = totalCards > 0 ? ((ownedCards / totalCards) * 100).toFixed(1) : 0;
    
    // Atualizar valores
    document.getElementById('totalCards').textContent = totalCards;
    document.getElementById('ownedCards').textContent = ownedCards;
    document.getElementById('completionRate').textContent = `${completionRate}%`;
    
    // Mostrar o box de estatísticas
    statsBox.style.display = 'block';
}

// Filtrar por busca de nome
function filterBySearch() {
    const input = document.getElementById('searchInput');
    searchTerm = input.value.toLowerCase();
    currentPage = 0; // Voltar para primeira página ao buscar
    renderCurrentPage();
}

// Define o filtro de tipo de carta
function setFilter(filter) {
    currentFilter = filter;
    currentPage = 0;
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.filter === filter) {
            btn.classList.add('active');
        }
    });
    
    renderCurrentPage();
}

// Carrega as cartas de uma coleção
async function loadCards() {
    try {
        // Buscar informações da coleção
        const collectionResponse = await fetch(`/api/collections/${currentCollection}`);
        currentCollectionData = await collectionResponse.json();
        
        // Buscar cartas
        const cardsResponse = await fetch(`/api/collections/${currentCollection}/cards`);
        allCards = await cardsResponse.json();
        
        // Detectar o número mínimo e máximo da coleção
        if (allCards.length > 0) {
            minCardNumber = Math.min(...allCards.map(c => c.collection_number));
            maxCardNumber = Math.max(...allCards.map(c => c.collection_number));
        } else {
            minCardNumber = 0;
            maxCardNumber = 0;
        }
        
        // Atualizar estatísticas na página de estatísticas
        updateStatsPage();
        
        // Carregar anotações
        loadNotes();
        
        renderCurrentPage();
    } catch (error) {
        console.error('Erro ao carregar cartas:', error);
    }
}

// Atualiza a página de estatísticas
function updateStatsPage() {
    const totalCards = allCards.length;
    const ownedCards = allCards.filter(card => card.quantity > 0).length;
    const completionRate = totalCards > 0 ? ((ownedCards / totalCards) * 100).toFixed(1) : 0;
    
    document.getElementById('totalCardsStats').textContent = totalCards;
    document.getElementById('ownedCardsStats').textContent = ownedCards;
    document.getElementById('completionRateStats').textContent = `${completionRate}%`;
    
    // Atualizar descrição da coleção
    const descriptionContent = document.getElementById('descriptionContent');
    const descriptionText = document.getElementById('collectionDescription');
    if (currentCollectionData && currentCollectionData.description) {
        descriptionText.textContent = currentCollectionData.description;
        descriptionContent.style.display = 'block';
    } else {
        descriptionContent.style.display = 'none';
    }
    
    // Mostrar a página de estatísticas
    document.getElementById('statsPage').style.display = 'flex';
}

// Carrega as anotações da coleção
function loadNotes() {
    const notesTextarea = document.getElementById('collectionNotes');
    if (currentCollectionData && currentCollectionData.notes) {
        notesTextarea.value = currentCollectionData.notes;
    } else {
        notesTextarea.value = '';
    }
}

// Salva as anotações da coleção
async function saveNotes() {
    const notesTextarea = document.getElementById('collectionNotes');
    const notes = notesTextarea.value;
    
    try {
        const response = await fetch(`/api/collections/${currentCollection}/notes`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ notes: notes })
        });
        
        if (response.ok) {
            // Feedback visual
            const btn = document.querySelector('.btn-save-notes');
            const originalText = btn.textContent;
            btn.textContent = '✅ Salvo!';
            btn.style.background = 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)';
            
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            }, 2000);
        }
    } catch (error) {
        console.error('Erro ao salvar anotações:', error);
        alert('Erro ao salvar anotações!');
    }
}

// Renderiza a página atual
function renderCurrentPage() {
    // Filtrar cartas por termo de busca
    let filteredCards = allCards;
    if (searchTerm) {
        filteredCards = allCards.filter(c => 
            c.name.toLowerCase().includes(searchTerm)
        );
    }
    
    // Controlar visibilidade dos livros
    const firstBook = document.querySelector('.book-container .book:first-child');
    const nextBook = document.getElementById('nextBook');
    
    if (currentPage === 0) {
        // Primeira página: mostrar primeiro livro (estatísticas + cartas 1-9)
        if (firstBook) firstBook.style.display = 'flex';
        if (nextBook) nextBook.style.display = 'none';
        renderFirstPage(filteredCards);
    } else {
        // Páginas seguintes: esconder primeiro livro, mostrar segundo
        if (firstBook) firstBook.style.display = 'none';
        if (nextBook) nextBook.style.display = 'flex';
        renderOtherPages(filteredCards);
    }
    
    // Atualizar informações de paginação
    updatePagination();
}

// Renderiza a primeira página (cartas 1-9 no lado direito)
function renderFirstPage(filteredCards) {
    const startCardNumber = minCardNumber;
    const endCardNumber = minCardNumber + CARDS_FIRST_PAGE;
    
    // Renderizar cartas 1-9 nos slots 1-9 (lado direito)
    for (let i = 0; i < CARDS_FIRST_PAGE; i++) {
        const cardNumber = startCardNumber + i;
        const card = filteredCards.find(c => c.collection_number === cardNumber);
        const slotNumber = i + 1;
        const slot = document.querySelector(`.card-slot[data-slot="${slotNumber}"]`);
        
        if (slot) {
            if (card) {
                renderCardSlot(slot, card, cardNumber);
            } else {
                // Não mostrar se não existe carta
                if (cardNumber <= maxCardNumber) {
                    renderCardSlot(slot, null, cardNumber);
                } else {
                    slot.style.display = 'none';
                }
            }
        }
    }
}

// Renderiza páginas 2+ (18 cartas por página, 9 de cada lado)
function renderOtherPages(filteredCards) {
    // Calcular qual conjunto de 18 cartas mostrar
    // Página 1 = cartas 10-27, Página 2 = cartas 28-45, etc
    const startCardNumber = minCardNumber + CARDS_FIRST_PAGE + ((currentPage - 1) * CARDS_PER_PAGE);
    const endCardNumber = startCardNumber + CARDS_PER_PAGE;
    
    // Renderizar 18 cartas (slots 10-27)
    for (let i = 0; i < CARDS_PER_PAGE; i++) {
        const cardNumber = startCardNumber + i;
        const card = filteredCards.find(c => c.collection_number === cardNumber);
        const slotNumber = 10 + i; // Slots começam em 10
        const slot = document.querySelector(`.card-slot[data-slot="${slotNumber}"]`);
        
        if (slot) {
            if (card) {
                renderCardSlot(slot, card, cardNumber);
            } else {
                // Não mostrar se não existe carta ou passou do máximo
                if (cardNumber <= maxCardNumber) {
                    renderCardSlot(slot, null, cardNumber);
                } else {
                    slot.style.display = 'none';
                }
            }
        }
    }
}

// Renderiza um slot de carta
function renderCardSlot(slot, card, cardNumber) {
    if (!slot) return;
    
    slot.innerHTML = '';
    slot.className = 'card-slot';
    slot.style.display = 'flex'; // Garantir que está visível por padrão
    
    if (card) {
        // Carta existe
        const isZero = card.quantity === 0;
        if (isZero) {
            slot.classList.add('zero-quantity');
        }
        
        // Logo Konami ou texto Orica ao lado do número (clicável para alternar)
        const origemHtml = card.tipoOrigem === 'Orica' 
            ? '<span class="orica-text origem-toggle" onclick="toggleCardOrigem(' + card.id + ')" title="Clique para mudar para Konami">Orica</span>'
            : '<img src="/static/konami-logo.svg" alt="Konami" class="konami-logo origem-toggle" onclick="toggleCardOrigem(' + card.id + ')" title="Clique para mudar para Orica" onerror="this.style.display=\'none\'">';
        
        // Se não tem imagem, tenta buscar via API YGOPRODeck
        let imageUrl = card.image_url;
        if (!imageUrl || imageUrl === 'None' || imageUrl === '') {
            // Tenta buscar na API YGOPRODeck para Konami e Orica
            // Limpar nome da carta para criar URL válida
            const cleanName = card.name.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '%20');
            imageUrl = `https://images.ygoprodeck.com/images/cards/${cleanName}.jpg`;
        }
        
        slot.innerHTML = `
            <div class="card-content">
                <img src="${imageUrl}" 
                     alt="${card.name}" 
                     class="card-image"
                     onerror="this.src='https://via.placeholder.com/200x280?text=${encodeURIComponent(card.name)}'">
                <div class="card-info">
                    <div class="card-header">
                        ${origemHtml}
                        <div class="card-number">#${card.collection_number}</div>
                    </div>
                    <div class="card-name" title="${card.name}">${card.name}</div>
                    <div class="card-quantity">
                        <button class="quantity-btn" onclick="decrementCard(${card.id})" ${card.quantity === 0 ? 'disabled' : ''}>−</button>
                        <span class="quantity-display">${card.quantity}</span>
                        <button class="quantity-btn" onclick="incrementCard(${card.id})">+</button>
                    </div>
                </div>
            </div>
        `;
    } else {
        // Carta não existe - deixar slot vazio mas visível
        slot.classList.add('empty');
        slot.style.display = 'none'; // Ocultar completamente
    }
}

// Incrementa a quantidade de uma carta
async function incrementCard(cardId) {
    try {
        const response = await fetch(`/api/cards/${cardId}/increment`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const updatedCard = await response.json();
            // Atualizar o card no array local
            const index = allCards.findIndex(c => c.id === cardId);
            if (index !== -1) {
                allCards[index] = updatedCard;
            }
            renderCurrentPage();
            updateStatsPage();
            updateCollectionStats();
        }
    } catch (error) {
        console.error('Erro ao incrementar carta:', error);
        alert('Erro ao atualizar quantidade!');
    }
}

// Decrementa a quantidade de uma carta
async function decrementCard(cardId) {
    try {
        const response = await fetch(`/api/cards/${cardId}/decrement`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const updatedCard = await response.json();
            // Atualizar o card no array local
            const index = allCards.findIndex(c => c.id === cardId);
            if (index !== -1) {
                allCards[index] = updatedCard;
            }
            renderCurrentPage();
            updateStatsPage();
            updateCollectionStats();
        }
    } catch (error) {
        console.error('Erro ao decrementar carta:', error);
        alert('Erro ao atualizar quantidade!');
    }
}

// Alterna entre Konami e Orica
async function toggleCardOrigem(cardId) {
    try {
        const response = await fetch(`/api/cards/${cardId}/toggle-origem`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const updatedCard = await response.json();
            // Atualizar o card no array local
            const index = allCards.findIndex(c => c.id === cardId);
            if (index !== -1) {
                allCards[index] = updatedCard;
            }
            renderCurrentPage();
        }
    } catch (error) {
        console.error('Erro ao alternar origem da carta:', error);
        alert('Erro ao alternar tipo da carta!');
    }
}

// Página anterior
function previousPage() {
    if (currentPage > 0) {
        currentPage--;
        renderCurrentPage();
    }
}

// Próxima página
function nextPage() {
    const totalPages = Math.ceil(getTotalCardsInCollection() / CARDS_PER_PAGE);
    if (currentPage < totalPages - 1) {
        currentPage++;
        renderCurrentPage();
    }
}

// Obtém o total de cartas da coleção
function getTotalCardsInCollection() {
    const select = document.getElementById('collectionSelect');
    const selectedOption = select.options[select.selectedIndex];
    if (!selectedOption || !selectedOption.value) return 0;
    
    // Extrair o número do texto da opção
    const match = selectedOption.textContent.match(/\((\d+) cartas\)/);
    return match ? parseInt(match[1]) : 0;
}

// Atualiza informações de paginação
function updatePagination() {
    const totalCards = maxCardNumber - minCardNumber + 1;
    
    // Calcular total de páginas (primeira página tem 9, resto tem 18)
    const cardsAfterFirst = Math.max(0, totalCards - CARDS_FIRST_PAGE);
    const totalPages = 1 + Math.ceil(cardsAfterFirst / CARDS_PER_PAGE);
    
    // Calcular qual faixa de cartas está sendo mostrada
    let startCard, endCard, leftStart, leftEnd, rightStart, rightEnd;
    
    if (currentPage === 0) {
        // Primeira página: apenas lado direito (cartas 1-9)
        startCard = minCardNumber;
        endCard = Math.min(minCardNumber + CARDS_FIRST_PAGE - 1, maxCardNumber);
        rightStart = startCard;
        rightEnd = endCard;
        
        document.getElementById('rightPageNumber').textContent = `Cartas ${rightStart}-${rightEnd}`;
    } else {
        // Páginas seguintes: ambos os lados (18 cartas)
        startCard = minCardNumber + CARDS_FIRST_PAGE + ((currentPage - 1) * CARDS_PER_PAGE);
        endCard = Math.min(startCard + CARDS_PER_PAGE - 1, maxCardNumber);
        
        // Lado esquerdo (9 cartas)
        leftStart = startCard;
        leftEnd = Math.min(startCard + 8, maxCardNumber);
        
        // Lado direito (9 cartas)
        rightStart = startCard + 9;
        rightEnd = Math.min(startCard + 17, maxCardNumber);
        
        document.getElementById('leftPageNumber').textContent = `Cartas ${leftStart}-${leftEnd}`;
        document.getElementById('rightPageNumber2').textContent = `Cartas ${rightStart}-${rightEnd}`;
    }
    
    document.getElementById('pageInfo').textContent = 
        `Cartas ${startCard}-${endCard} de ${maxCardNumber} | Página ${currentPage + 1}/${totalPages}`;
    
    // Habilitar/desabilitar botões
    document.getElementById('prevBtn').disabled = currentPage === 0;
    document.getElementById('nextBtn').disabled = currentPage >= totalPages - 1 || totalCards === 0;
}

// Mostra estado vazio
function showEmptyState() {
    document.getElementById('bookContainer').style.display = 'none';
    document.getElementById('emptyState').style.display = 'block';
    document.querySelector('.navigation').style.display = 'none';
}

// Esconde estado vazio
function hideEmptyState() {
    document.getElementById('bookContainer').style.display = 'flex';
    document.getElementById('emptyState').style.display = 'none';
    document.querySelector('.navigation').style.display = 'flex';
}
