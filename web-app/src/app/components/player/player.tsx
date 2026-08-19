import Card from "./card/card";
import { CardType, PlayerType } from "../types"
import styles from "./player.module.css"

export default function Player({player}: {player: PlayerType | null}) {
  if (!player) {
    return (
      <div className={styles.player}>
        <span>WIP</span>
      </div>
    )
  }
  player.cards = [{id: 1, rank: "A", suit: "h"}, {id: 2, rank: "K", suit: "h"}];
  return (
    <div className={styles.player}>
      <div className={styles.card_space}>
        {player.cards.map((c: CardType) => (<Card key={c.id} data={c}/>))}
      </div>
      <div className={styles.info}>
        <div className={styles.text_info}>
          <span className={styles.name}>{player.name}</span>
          <span className={styles.chips}>{player.stack}</span>
        </div>
        <img className={styles.pic} src={player.image_url || "/default_avatar.webp"}></img>
      </div>
    </div>
  )
}