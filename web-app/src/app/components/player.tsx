import Card from "./card";
import { CardType, PlayerType } from "../types"

export default function Player({player, onPlayerUpdate}: {player: PlayerType, onPlayerUpdate: (updatedPlayer: PlayerType) => void}) {
  return (
    <div>
      {player.id}:
      {player.name}
      {player.cards.map((c: CardType) => (<Card key={c.id} data={c}/>))}
    </div>
  );
}