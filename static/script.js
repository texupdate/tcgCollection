// Carrega as estatísticas
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        document.getElementById('totalCards').textContent = stats.total_cards;
        document.getElementById('uniqueCards').textContent = stats.unique_cards;
        document.getElementById('totalValue').textContent = `R$ ${stats.total_value.toFixed(2)}`;
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// Carrega todas as cartas
async function loadCards() {
    try {
        const response = await fetch('/api/cards');
        const cards = await response.json();
        
        const cardsList = document.getElementById('cardsList');
        
        if (cards.length === 0) {
            cardsList.innerHTML = '<p class="empty-state">Nenhuma carta cadastrada ainda. Clique em "Adicionar Carta" para começar!</p>';
            return;
        }
        
        cardsList.innerHTML = cards.map(card => `
            <div class="card-item">
                <h3>${card.name}</h3>
                ${card.set_name ? `<p class="card-info"><strong>Set:</strong> ${card.set_name}</p>` : ''}
                ${card.card_number ? `<p class="card-info"><strong>Número:</strong> ${card.card_number}</p>` : ''}
                ${card.rarity ? `<p class="card-info"><strong>Raridade:</strong> ${card.rarity}</p>` : ''}
                <p class="card-info"><strong>Quantidade:</strong> ${card.quantity}</p>
                ${card.condition ? `<p class="card-info"><strong>Condição:</strong> ${card.condition}</p>` : ''}
                ${card.language ? `<p class="card-info"><strong>Idioma:</strong> ${card.language}</p>` : ''}
                ${card.notes ? `<p class="card-info"><strong>Notas:</strong> ${card.notes}</p>` : ''}
                <div class="card-actions">
                    <button class="btn btn-danger" onclick="deleteCard(${card.id})">🗑️ Remover</button>
                </div>
            </div>
        `).join('');
        
        loadStats();
    } catch (error) {
        console.error('Erro ao carregar cartas:', error);
    }
}

// Mostra o formulário de adicionar carta
function showAddCardForm() {
    document.getElementById('addCardForm').style.display = 'block';
    document.getElementById('cardForm').scrollIntoView({ behavior: 'smooth' });
}

// Esconde o formulário de adicionar carta
function hideAddCardForm() {
    document.getElementById('addCardForm').style.display = 'none';
    document.getElementById('cardForm').reset();
}

// Adiciona uma nova carta
document.getElementById('cardForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const cardData = {
        name: document.getElementById('name').value,
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
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cardData)
        });
        
        if (response.ok) {
            hideAddCardForm();
            loadCards();
            alert('Carta adicionada com sucesso!');
        }
    } catch (error) {
        console.error('Erro ao adicionar carta:', error);
        alert('Erro ao adicionar carta!');
    }
});

// Remove uma carta
async function deleteCard(cardId) {
    if (!confirm('Tem certeza que deseja remover esta carta?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/cards/${cardId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadCards();
            alert('Carta removida com sucesso!');
        }
    } catch (error) {
        console.error('Erro ao remover carta:', error);
        alert('Erro ao remover carta!');
    }
}

// Carrega as cartas ao iniciar a página
window.addEventListener('DOMContentLoaded', () => {
    loadCards();
    loadStats();
});
