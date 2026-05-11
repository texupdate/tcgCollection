from app import app, db, Collection, Card

with app.app_context():
    mfc = Collection.query.filter_by(name='MFC').first()
    if not mfc:
        print('MFC collection not found')
        exit()
    
    print(f'MFC Collection - ID: {mfc.id}, Total Cards: {mfc.total_cards}')
    
    cards = Card.query.filter_by(collection_id=mfc.id).order_by(Card.collection_number).all()
    print(f'Cards in DB: {len(cards)}')
    
    if cards:
        print(f'Card numbers range: {cards[0].collection_number} to {cards[-1].collection_number}')
    
    print(f'\nCards 99-108:')
    cards_99_108 = [card for card in cards if 99 <= card.collection_number <= 108]
    
    if cards_99_108:
        for c in cards_99_108:
            print(f'  #{c.collection_number}: {c.name}')
    else:
        print('  No cards found in range 99-108')
    
    print(f'\nAll card numbers:')
    all_numbers = sorted([card.collection_number for card in cards])
    print(all_numbers)
