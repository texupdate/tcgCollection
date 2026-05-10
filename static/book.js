let currentCollection = null;
let currentPage = 0;
let allCards = [];
let minCardNumber = 0; // Número mínimo da coleção (0 ou 1)
let searchTerm = ''; // Termo de busca
const CARDS_PER_PAGE = 18;

// Carrega as coleções ao iniciar
window.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Página carregada, iniciando...');
    loadCollections();
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

// Muda a coleção selecionada
function changeCollection() {
    const select = document.getElementById('collectionSelect');
    currentCollection = select.value;
    currentPage = 0;
    searchTerm = ''; // Limpar busca ao trocar coleção
    document.getElementById('searchInput').value = '';
    
    if (currentCollection) {
        loadCards();
        hideEmptyState();
    } else {
        showEmptyState();
    }
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
        const response = await fetch(`/api/collections/${currentCollection}/cards`);
        allCards = await response.json();
        
        // Detectar o número mínimo da coleção (0 ou 1)
        if (allCards.length > 0) {
            minCardNumber = Math.min(...allCards.map(c => c.collection_number));
        } else {
            minCardNumber = 0;
        }
        
        renderCurrentPage();
    } catch (error) {
        console.error('Erro ao carregar cartas:', error);
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
    
    const startCardNumber = minCardNumber + (currentPage * CARDS_PER_PAGE);
    const endCardNumber = startCardNumber + CARDS_PER_PAGE;
    
    // Obter todas as cartas da página atual
    const pageCards = [];
    for (let i = startCardNumber; i < endCardNumber; i++) {
        const card = filteredCards.find(c => c.collection_number === i);
        pageCards.push(card || null);
    }
    
    // Renderizar cartas nos slots
    for (let i = 0; i < CARDS_PER_PAGE; i++) {
        const slotNumber = i + 1;
        const cardNumber = startCardNumber + i;
        const card = pageCards[i];
        
        const slot = document.querySelector(`.card-slot[data-slot="${slotNumber}"]`);
        renderCardSlot(slot, card, cardNumber);
    }
    
    // Atualizar informações de paginação
    updatePagination();
}

// Renderiza um slot de carta
function renderCardSlot(slot, card, cardNumber) {
    slot.innerHTML = '';
    slot.className = 'card-slot';
    
    if (card) {
        // Carta existe
        const isZero = card.quantity === 0;
        if (isZero) {
            slot.classList.add('zero-quantity');
        }
        
        // Logo Konami ou texto Orica ao lado do número
        const origemHtml = card.tipoOrigem === 'Orica' 
            ? '<span class="orica-text">Orica</span>'
            : '<img src="/static/konami-logo.svg" alt="Konami" class="konami-logo" onerror="this.style.display=\'none\'">';
        
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
        // Slot vazio
        slot.classList.add('empty');
        slot.innerHTML = `
            <div style="text-align: center; color: #999;">
                <div style="font-size: 2em;">📭</div>
                <div style="font-size: 0.9em; margin-top: 10px;">Carta #${cardNumber}</div>
                <div style="font-size: 0.8em; color: #bbb;">Não cadastrada</div>
            </div>
        `;
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
        }
    } catch (error) {
        console.error('Erro ao decrementar carta:', error);
        alert('Erro ao atualizar quantidade!');
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
    const totalCards = getTotalCardsInCollection();
    const totalPages = Math.ceil(totalCards / CARDS_PER_PAGE);
    
    const startCard = minCardNumber + (currentPage * CARDS_PER_PAGE);
    const endCard = Math.min(startCard + CARDS_PER_PAGE - 1, minCardNumber + totalCards - 1);
    
    document.getElementById('pageInfo').textContent = 
        `Cartas ${startCard}-${endCard} de ${totalCards}`;
    
    const leftStart = startCard;
    const leftEnd = Math.min(startCard + 8, endCard);
    const rightStart = startCard + 9;
    const rightEnd = endCard;
    
    document.getElementById('leftPageNumber').textContent = 
        `Cartas ${leftStart}-${leftEnd}`;
    document.getElementById('rightPageNumber').textContent = 
        `Cartas ${rightStart}-${rightEnd}`;
    
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
