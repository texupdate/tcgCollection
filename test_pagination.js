// Cálculo de paginação MFC (108 cartas, de 0 a 107)
const minCardNumber = 0;
const maxCardNumber = 107;
const CARDS_FIRST_PAGE = 9;
const CARDS_PER_PAGE = 18;

const totalCards = maxCardNumber - minCardNumber + 1; // 108
console.log('Total cards:', totalCards);

const cardsAfterFirst = Math.max(0, totalCards - CARDS_FIRST_PAGE); // 99
console.log('Cards after first:', cardsAfterFirst);

const totalPages = 1 + Math.ceil(cardsAfterFirst / CARDS_PER_PAGE); // 1 + 6 = 7
console.log('Total pages:', totalPages);

console.log('\nPaginação:');
console.log('Página 0: cartas 0-8');

for (let page = 1; page < totalPages; page++) {
    const startCard = minCardNumber + CARDS_FIRST_PAGE + ((page - 1) * CARDS_PER_PAGE);
    const endCard = Math.min(startCard + CARDS_PER_PAGE - 1, maxCardNumber);
    console.log(`Página ${page}: cartas ${startCard}-${endCard}`);
}
