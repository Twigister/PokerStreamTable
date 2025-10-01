export interface CardType { id: number, rank: string, suit: string};
export interface PlayerType { id: number, name: string, cards: CardType[] };