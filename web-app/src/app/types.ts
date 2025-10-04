export interface CardType {
  id: number,
  rank: string,
  suit: string
};

export type PlayerType = {
  id: number,
  name: string,
  cards: CardType[],
  stack: number
};