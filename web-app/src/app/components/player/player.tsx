import Card from "./card/card";
import { CardType, PlayerType } from "../types"
import styles from "./player.module.css"

export default function Player({player}: {player: PlayerType}) {
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
        <img className={styles.pic} src="/default_avatar.webp"></img>
      </div>
    </div>
  );
}
