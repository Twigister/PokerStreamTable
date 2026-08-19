export interface CardType {
  id: number,
  rank: string,
  suit: string
};

export type PlayerType = {
  id: number,
  name: string,
  cards: CardType[],
  stack: number,
  image_url?: string | null,
  seat_number: number,
};

export type PlayerProfileUpdate = {
  id: number,
  name: string,
  image_url: string | null,
};

export type SeatedPlayerUpdate = PlayerProfileUpdate & {
  seat_number: number,
};

export type PlayerUnseatUpdate = {
  id: number,
};

export const PLAYER_DRAG_TYPE = "registered-player";