from app import app, db, Collection, Card

with app.app_context():
    collections = Collection.query.all()
    
    print('Corrigindo total_cards de todas as coleções...\n')
    
    for col in collections:
        cards = Card.query.filter_by(collection_id=col.id).all()
        
        if cards:
            min_num = min(c.collection_number for c in cards)
            max_num = max(c.collection_number for c in cards)
            correct_total = max_num - min_num + 1
            
            if col.total_cards != correct_total:
                print(f'{col.name}: {col.total_cards} -> {correct_total} (min={min_num}, max={max_num})')
                col.total_cards = correct_total
            else:
                print(f'{col.name}: {col.total_cards} ✓')
    
    db.session.commit()
    print('\n✅ Todas as coleções corrigidas!')
