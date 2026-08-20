import Card from "./card/card";
import { PlayerType } from "../../types";
import styles from "./player.module.css";

export default function Player({ player }: { player: PlayerType }) {
  const cards = player.cards && player.cards.length > 0 ? player.cards : [
    { id: 1, rank: "A", suit: "h" },
    { id: 2, rank: "K", suit: "h" },
  ];

  if (!player) {
    return null;
  }

  return (
    <section className={styles.player} aria-label={`Player ${player.name}`}>
      <div className={styles.card_space} aria-label="Player cards">
        {cards.map((card) => <Card key={card.id} data={card} />)}
      </div>
      <div className={styles.info}>
        <div className={styles.text_info}>
          <strong className={styles.name}>{player.name}</strong>
          <span className={styles.chips} aria-label={`${player.stack ?? 0} chips`}>
            {player.stack ?? 0}
          </span>
        </div>
        <img
          className={styles.pic}
          src={player.image_url || "/default_avatar.webp"}
          alt={`${player.name}'s profile`}
        />
      </div>
    </section>
  );
}