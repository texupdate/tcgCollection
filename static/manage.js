// Carrega dados ao iniciar
window.addEventListener('DOMContentLoaded', () => {
    loadCollections();
    loadCards();
});

// ============= COLEÇÕES =============

async function loadCollections() {
    try {
        const response = await fetch('/api/collections');
        const collections = await response.json();
        
        renderCollections(collections);
        updateCollectionSelects(collections);
    } catch (error) {
        console.error('Erro ao carregar coleções:', error);
    }
}

function renderCollections(collections) {
    const list = document.getElementById('collectionsList');
    
    if (collections.length === 0) {
        list.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">Nenhuma coleção cadastrada. Clique em "Nova Coleção" para começar!</p>';
        return;
    }
    
    list.innerHTML = collections.map(col => `
        <div class="collection-item">
            <h3>${col.name}</h3>
            <p>${col.description || 'Sem descrição'}</p>
            <p><strong>Total de cartas:</strong> ${col.total_cards}</p>
            <div class="item-actions">
                <button class="btn btn-danger" onclick="deleteCollection(${col.id}, '${col.name}')">🗑️ Deletar</button>
            </div>
        </div>
    `).join('');
}

function updateCollectionSelects(collections) {
    const selects = [
        document.getElementById('filterCollection'),
        document.getElementById('card_collection')
    ];
    
    selects.forEach(select => {
        const currentValue = select.value;
        const isFilter = select.id === 'filterCollection';
        
        select.innerHTML = isFilter ? '<option value="">Todas as coleções</option>' : '<option value="">Selecione...</option>';
        
        collections.forEach(col => {
            const option = document.createElement('option');
            option.value = col.id;
            option.textContent = col.name;
            select.appendChild(option);
        });
        
        if (currentValue) {
            select.value = currentValue;
        }
    });
}

function showAddCollectionForm() {
    document.getElementById('addCollectionForm').style.display = 'block';
}

function hideAddCollectionForm() {
    document.getElementById('addCollectionForm').style.display = 'none';
    document.getElementById('collectionForm').reset();
}

document.getElementById('collectionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        name: document.getElementById('collection_name').value,
        description: document.getElementById('collection_desc').value,
        total_cards: parseInt(document.getElementById('collection_total').value)
    };
    
    try {
        const response = await fetch('/api/collections', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            hideAddCollectionForm();
            loadCollections();
            alert('Coleção criada com sucesso!');
        } else {
            const error = await response.json();
            alert('Erro: ' + (error.message || 'Não foi possível criar a coleção'));
        }
    } catch (error) {
        console.error('Erro ao criar coleção:', error);
        alert('Erro ao criar coleção!');
    }
});

async function deleteCollection(id, name) {
    if (!confirm(`Tem certeza que deseja deletar a coleção "${name}"?\nTodas as cartas desta coleção também serão deletadas!`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/collections/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadCollections();
            loadCards();
            alert('Coleção deletada com sucesso!');
        }
    } catch (error) {
        console.error('Erro ao deletar coleção:', error);
        alert('Erro ao deletar coleção!');
    }
}

// ============= CARTAS =============

async function loadCards() {
    try {
        const response = await fetch('/api/cards');
        const cards = await response.json();
        
        renderCards(cards);
    } catch (error) {
        console.error('Erro ao carregar cartas:', error);
    }
}

function renderCards(cards) {
    const filterCollectionId = document.getElementById('filterCollection').value;
    
    let filteredCards = cards;
    if (filterCollectionId) {
        filteredCards = cards.filter(c => c.collection_id == filterCollectionId);
    }
    
    // Ordenar por coleção e número
    filteredCards.sort((a, b) => {
        if (a.collection_id !== b.collection_id) {
            return a.collection_id - b.collection_id;
        }
        return a.collection_number - b.collection_number;
    });
    
    const list = document.getElementById('cardsList');
    
    if (filteredCards.length === 0) {
        list.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">Nenhuma carta cadastrada. Clique em "Nova Carta" para adicionar!</p>';
        return;
    }
    
    list.innerHTML = filteredCards.map(card => `
        <div class="card-item ${card.quantity === 0 ? 'zero-quantity-card' : ''}">
            <div class="card-preview">
                <img src="${card.image_url || 'https://via.placeholder.com/150x210?text=No+Image'}" 
                     alt="${card.name}"
                     onerror="this.src='https://via.placeholder.com/150x210?text=Erro'">
            </div>
            <div class="card-details">
                <h3>${card.name}</h3>
                <p><strong>Coleção:</strong> ID ${card.collection_id} | <strong>Número:</strong> #${card.collection_number}</p>
                ${card.set_name ? `<p><strong>Set:</strong> ${card.set_name}</p>` : ''}
                ${card.rarity ? `<p><strong>Raridade:</strong> ${card.rarity}</p>` : ''}
                <p><strong>Quantidade:</strong> ${card.quantity}</p>
                ${card.notes ? `<p><strong>Notas:</strong> ${card.notes}</p>` : ''}
                <div class="item-actions">
                    <button class="btn btn-danger" onclick="deleteCard(${card.id}, '${card.name}')">🗑️ Deletar</button>
                </div>
            </div>
        </div>
    `).join('');
}

function filterCardsByCollection() {
    loadCards();
}

function showAddCardForm() {
    document.getElementById('addCardForm').style.display = 'block';
    document.getElementById('cardForm').scrollIntoView({ behavior: 'smooth' });
}

function hideAddCardForm() {
    document.getElementById('addCardForm').style.display = 'none';
    document.getElementById('cardForm').reset();
}

document.getElementById('cardForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        collection_id: parseInt(document.getElementById('card_collection').value),
        collection_number: parseInt(document.getElementById('collection_number').value),
        name: document.getElementById('name').value,
        image_url: document.getElementById('image_url').value,
        set_name: document.getElementById('set_name').value,
        card_number: document.getElementById('card_number').value,
        rarity: document.getElementById('rarity').value,
        quantity: parseInt(document.getElementById('quantity').value),
        condition: document.getElementById('condition').value,
        language: document.getElementById('language').value,
        notes: document.getElementById('notes').value
    };
    
    try {
        const response = await fetch('/api/cards', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            hideAddCardForm();
            loadCards();
            alert('Carta cadastrada com sucesso!');
        } else {
            const error = await response.json();
            alert('Erro: ' + (error.message || 'Não foi possível cadastrar a carta'));
        }
    } catch (error) {
        console.error('Erro ao cadastrar carta:', error);
        alert('Erro ao cadastrar carta! Verifique se a coleção e o número não estão duplicados.');
    }
});

async function deleteCard(id, name) {
    if (!confirm(`Tem certeza que deseja deletar a carta "${name}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/cards/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadCards();
            alert('Carta deletada com sucesso!');
        }
    } catch (error) {
        console.error('Erro ao deletar carta:', error);
        alert('Erro ao deletar carta!');
    }
}
