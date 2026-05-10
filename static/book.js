let currentCollection = null;
let currentPage = 0;
let allCards = [];
const CARDS_PER_PAGE = 18;

// Carrega as coleções ao iniciar
window.addEventListener('DOMContentLoaded', () => {
    loadCollections();
});

// Carrega todas as coleções
async function loadCollections() {
    try {
        const response = await fetch('/api/collections');
        const collections = await response.json();
        
        const select = document.getElementById('collectionSelect');
        select.innerHTML = '<option value="">Selecione uma coleção...</option>';
        
        collections.forEach(collection => {
            const option = document.createElement('option');
            option.value = collection.id;
            option.textContent = `${collection.name} (${collection.total_cards} cartas)`;
            select.appendChild(option);
        });
        
        if (collections.length === 0) {
            showEmptyState();
        }
    } catch (error) {
        console.error('Erro ao carregar coleções:', error);
    }
}

// Muda a coleção selecionada
function changeCollection() {
    const select = document.getElementById('collectionSelect');
    currentCollection = select.value;
    currentPage = 0;
    
    if (currentCollection) {
        loadCards();
        hideEmptyState();
    } else {
        showEmptyState();
    }
}

// Carrega as cartas da coleção
async function loadCards() {
    if (!currentCollection) return;
    
    try {
        const response = await fetch(`/api/collections/${currentCollection}/cards`);
        allCards = await response.json();
        
        renderCurrentPage();
    } catch (error) {
        console.error('Erro ao carregar cartas:', error);
    }
}

// Renderiza a página atual
function renderCurrentPage() {
    const startIndex = currentPage * CARDS_PER_PAGE;
    const endIndex = startIndex + CARDS_PER_PAGE;
    
    // Obter todas as cartas da página atual
    const pageCards = [];
    for (let i = startIndex + 1; i <= endIndex; i++) {
        const card = allCards.find(c => c.collection_number === i);
        pageCards.push(card || null);
    }
    
    // Renderizar cartas nos slots (1-9 esquerda, 10-18 direita)
    for (let i = 0; i < CARDS_PER_PAGE; i++) {
        const slotNumber = i + 1;
        const cardNumber = startIndex + i + 1;
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
        
        slot.innerHTML = `
            <div class="card-content">
                <img src="${card.image_url || 'https://via.placeholder.com/200x280?text=No+Image'}" 
                     alt="${card.name}" 
                     class="card-image"
                     onerror="this.src='https://via.placeholder.com/200x280?text=Erro+ao+carregar'">
                <div class="card-info">
                    <div class="card-number">#${card.collection_number}</div>
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
    
    const startCard = currentPage * CARDS_PER_PAGE + 1;
    const endCard = Math.min((currentPage + 1) * CARDS_PER_PAGE, totalCards);
    
    document.getElementById('pageInfo').textContent = 
        `Cartas ${startCard}-${endCard} de ${totalCards}`;
    
    document.getElementById('leftPageNumber').textContent = 
        `Cartas ${startCard}-${startCard + 8}`;
    document.getElementById('rightPageNumber').textContent = 
        `Cartas ${startCard + 9}-${endCard}`;
    
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
