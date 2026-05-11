from app import app, db, Card, Collection

with app.app_context():
    mfc = Collection.query.filter_by(name='MFC').first()
    cards = Card.query.filter_by(collection_id=mfc.id).order_by(Card.collection_number).all()
    
    # Simular lógica do viewer
    minCardNumber = min(c.collection_number for c in cards)
    maxCardNumber = max(c.collection_number for c in cards)
    
    CARDS_FIRST_PAGE = 9
    CARDS_PER_PAGE = 18
    
    totalCards = maxCardNumber - minCardNumber + 1
    cardsAfterFirst = max(0, totalCards - CARDS_FIRST_PAGE)
    totalPages = 1 + ((cardsAfterFirst + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE)
    
    print(f'Min: {minCardNumber}, Max: {maxCardNumber}')
    print(f'Total cards: {totalCards}')
    print(f'Total pages: {totalPages}')
    print()
    
    # Página 6 (última página)
    currentPage = 6
    startCardNumber = minCardNumber + CARDS_FIRST_PAGE + ((currentPage - 1) * CARDS_PER_PAGE)
    endCardNumber = startCardNumber + CARDS_PER_PAGE
    
    print(f'Página {currentPage}: cartas {startCardNumber} a {endCardNumber-1}')
    print()
    
    # Verificar quais cartas seriam renderizadas
    for i in range(CARDS_PER_PAGE):
        cardNumber = startCardNumber + i
        card = next((c for c in cards if c.collection_number == cardNumber), None)
        
        if cardNumber <= maxCardNumber:
            if card:
                print(f'  Slot {10+i}: Carta #{cardNumber} - {card.name}')
            else:
                print(f'  Slot {10+i}: Carta #{cardNumber} - (não cadastrada)')
        else:
            print(f'  Slot {10+i}: Carta #{cardNumber} - (fora do range, oculto)')
